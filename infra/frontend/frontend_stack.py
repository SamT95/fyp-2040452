from aws_cdk import (
    Stack,
    aws_ecs as ecs,
    aws_ec2 as ec2,
    aws_ecs_patterns as patterns,
    aws_ecr as ecr,
    aws_certificatemanager as acm,
    aws_ssm as ssm,
    aws_route53 as route53,
    aws_iam as iam,
    aws_logs as logs,
    CfnOutput,
    Duration,
)
from constructs import Construct

class FrontendStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Select default VPC
        vpc = ec2.Vpc.from_lookup(self, "VPC", is_default=True)

        # Create security groups
        vpc_endpoint_sg = ec2.SecurityGroup(self, "VpcEndpointSG", vpc=vpc)
        ecs_task_sg = ec2.SecurityGroup(self, "ECSTaskSG", vpc=vpc, allow_all_outbound=True)

        vpc_endpoint_sg.add_ingress_rule(
            peer=ecs_task_sg,
            connection=ec2.Port.tcp(443),
            description="Allow HTTPS from ECS tasks"
        )

        # Create VPC endpoints for ECR, CloudWatch and S3
        # https://docs.aws.amazon.com/AmazonECS/latest/developerguide/vpc-endpoints.html
        ecr_api_endpoint = vpc.add_interface_endpoint(
            "ECREndpoint",
            service=ec2.InterfaceVpcEndpointAwsService.ECR,
            security_groups=[vpc_endpoint_sg]
        )

        ecr_docker_endpoint = vpc.add_interface_endpoint(
            "ECRDockerEndpoint",
            service=ec2.InterfaceVpcEndpointAwsService.ECR_DOCKER,
            security_groups=[vpc_endpoint_sg]
        )

        cloudwatch_logs_endpoint = vpc.add_interface_endpoint(
            "CloudWatchLogsEndpoint",
            service=ec2.InterfaceVpcEndpointAwsService.CLOUDWATCH_LOGS,
            security_groups=[vpc_endpoint_sg]
        )

        s3_gateway_endpoint = vpc.add_gateway_endpoint(
            "S3GatewayEndpoint",
            service=ec2.GatewayVpcEndpointAwsService.S3,
        )

        # Reference Route53 hosted zone
        my_hosted_zone = route53.HostedZone.from_lookup(
            self, "MyHostedZone",
            domain_name="up2040452-fyp.com"
        )

        # Create a certificate for the domain
        certificate = acm.Certificate(
            self, "SiteCertificate",
            domain_name="up2040452-fyp.com",
            validation=acm.CertificateValidation.from_dns(
                my_hosted_zone
            )
        )

        # Create ECS cluster
        ecs_cluster = ecs.Cluster(
            self, "Cluster",
            vpc=vpc
        )

        task_role = iam.Role(
            self, "ECSTaskRole",
            inline_policies={
                "ECRAndSageMakerAccess": iam.PolicyDocument(
                    statements=[
                        # ECR image pull permissions
                        iam.PolicyStatement(
                            actions=[
                                "ecr:GetAuthorizationToken",
                                "ecr:BatchCheckLayerAvailability",
                                "ecr:GetDownloadUrlForLayer",
                                "ecr:BatchGetImage",
                                "sagemaker:InvokeEndpoint"
                            ],
                            resources=["*"]
                        ),
                        # SageMaker endpoint permissions
                        iam.PolicyStatement(
                            actions=["sagemaker:DescribeEndpoint"],
                            resources=["arn:aws:sagemaker:eu-west-1:349382198749:endpoint/huggingface-rag-llm-endpoint"],
                        ),
                    ]
                )
            },
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com")
        )

        # Add Cognito managed policy to task role
        task_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonCognitoPowerUser")
        )

        # Connect to 'frontend' ECR repository
        ecr_repo = ecr.Repository.from_repository_name(
            self, "ECRRepo",
            repository_name="frontend"
        )

        # Pull image tag from context
        image_tag = self.node.try_get_context("imageTag")

        # Pull QA Chain API URL from SSM
        rag_chain_api_url = ssm.StringParameter.from_string_parameter_name(
            self, "ChainAPIURL",
            string_parameter_name="rag-chain-api-url"
        ).string_value

        # Pull Chat history API URL from SSM
        chat_history_api_url = ssm.StringParameter.from_string_parameter_name(
            self, "ChatHistoryAPIURL",
            string_parameter_name="chat-history-api-url"
        ).string_value

        # Pull Cognito User Pool ID from SSM
        cognito_user_pool_id = ssm.StringParameter.from_string_parameter_name(
            self, "CognitoUserPoolID",
            string_parameter_name="user-pool-id"
        ).string_value

        # Pull Cognito User Pool Client ID from SSM
        cognito_user_pool_client_id = ssm.StringParameter.from_string_parameter_name(
            self, "CognitoUserPoolClientID",
            string_parameter_name="user-pool-client-id"
        ).string_value

        # Create log group for ECS task
        log_group = logs.LogGroup(
            self, "FrontendLogGroup",
            log_group_name="/ecs/frontend",
            retention=logs.RetentionDays.ONE_WEEK
        )

        # Create task definition
        task_definition = ecs.FargateTaskDefinition(
            self, "TaskDef",
            task_role=task_role
        )

        task_definition.add_container(
            "FrontendContainer",
            image=ecs.ContainerImage.from_ecr_repository(ecr_repo, tag=image_tag),
            memory_limit_mib=512,
            port_mappings=[ecs.PortMapping(container_port=3000)],
            environment={
                "CHAIN_API_URL": rag_chain_api_url,
                "HISTORY_API_URL": chat_history_api_url,
                "COGNITO_USER_POOL_ID": cognito_user_pool_id,
                "COGNITO_APP_CLIENT_ID": cognito_user_pool_client_id,
                "URL": "https://up2040452-fyp.com"
            },
            logging=ecs.LogDrivers.aws_logs(
                stream_prefix="frontend",
                log_group=log_group
            ),
        )

        # Create Fargate service
        load_balanced_fargate_service = (
            patterns.ApplicationLoadBalancedFargateService(
            self, "Service",
            cluster=ecs_cluster,
            assign_public_ip=True,
            task_definition=task_definition,
            public_load_balancer=True,
            desired_count=1,
            security_groups=[ecs_task_sg],
            listener_port=443,
            certificate=certificate,
            domain_name="up2040452-fyp.com",
            domain_zone=my_hosted_zone,
        ))

        alb_target_group = load_balanced_fargate_service.target_group
        alb_target_group.configure_health_check(
            path="/api/health",
            healthy_http_codes="200",
            healthy_threshold_count=3,
            unhealthy_threshold_count=2,
            interval=Duration.seconds(60),
            timeout=Duration.seconds(5)
        )

        # Output the load balancer address
        self.lb_address = load_balanced_fargate_service.load_balancer.load_balancer_dns_name
        CfnOutput(self, "LoadBalancerDNS", value=self.lb_address)
        

