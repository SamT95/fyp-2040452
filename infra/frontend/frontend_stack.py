from aws_cdk import (
    Stack,
    aws_ecs as ecs,
    aws_ec2 as ec2,
    aws_ecs_patterns as patterns,
    aws_ecr as ecr,
    CfnOutput,
)
from constructs import Construct

class FrontendStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Select default VPC - might need to change this
        vpc = ec2.Vpc.from_lookup(self, "VPC", is_default=True)

        # Create ECS cluster
        ecs_cluster = ecs.Cluster(
            self, "Cluster",
            vpc=vpc
        )

        # Connect to 'frontend' ECR repository
        ecr_repo = ecr.Repository.from_repository_name(
            self, "ECRRepo",
            repository_name="frontend"
        )

        # Create task definition
        task_definition = ecs.FargateTaskDefinition(
            self, "TaskDef"
        )
        task_definition.add_container(
            "FrontendContainer",
            image=ecs.ContainerImage.from_ecr_repository(ecr_repo),
            memory_limit_mib=512,
            port_mappings=[ecs.PortMapping(container_port=3000)]
        )

        # Create Fargate service
        load_balanced_fargate_service = patterns.ApplicationLoadBalancedFargateService(
            self, "Service",
            cluster=ecs_cluster,
            task_definition=task_definition,
            public_load_balancer=True,
            desired_count=1
        )

        # Output the load balancer address
        self.lb_address = load_balanced_fargate_service.load_balancer.load_balancer_dns_name
        CfnOutput(self, "LoadBalancerDNS", value=self.lb_address)



        # Old - Cloudfront and S3
        # site_bucket = s3.Bucket(
        #     self, "SiteBucket",
        #     website_index_document="index.html",
        #     public_read_access=False
        # )

        # s3deploy.BucketDeployment(
        #     self, "DeployFrontend",
        #     sources=[s3deploy.Source.asset("../frontend/dist")],
        #     destination_bucket=site_bucket,
        # )

        # # Create an OAI so that the CloudFront distribution can access the private S3 bucket
        # site_oai = cloudfront.OriginAccessIdentity(self, "SiteOAI")

        # # Create a CloudFront distribution
        # distribution = cloudfront.CloudFrontWebDistribution(
        #     self, "FrontendDistribution",
        #     origin_configs=[
        #         cloudfront.SourceConfiguration(
        #             s3_origin_source=cloudfront.S3OriginConfig(
        #                 s3_bucket_source=site_bucket,
        #                 origin_access_identity=site_oai
        #             ),
        #             behaviors=[cloudfront.Behavior(is_default_behavior=True)]
        #         )
        #     ]
        # )

        # # Output the CloudFront domain name
        # self.cf_domain = distribution.distribution_domain_name
        # CfnOutput(self, "CloudFrontDomain", value=self.cf_domain)
        

