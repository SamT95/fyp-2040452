from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_iam as iam,
    aws_ssm as ssm,
    aws_lambda_python_alpha as _alambda,
    aws_logs as logs,
    aws_dynamodb as dynamodb,
    aws_cognito as cognito,
)
from constructs import Construct

class BackendStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.qa_chain_lambda = _alambda.PythonFunction(
            self,
            "QueryChain",
            entry="../backend/rag",
            index="lambda_handler.py",
            handler="lambda_handler",
            runtime=_lambda.Runtime.PYTHON_3_10,
        )

        # Define policy statement to allow lambda to access secrets manager
        secrets_manager_policy = iam.PolicyStatement(
            actions=["secretsmanager:GetSecretValue"],
            effect=iam.Effect.ALLOW,
            resources=["*"]
        )

        # Define policy statement to allow lambda to invoke sagemaker endpoints
        sagemaker_policy = iam.PolicyStatement(
            actions=["sagemaker:InvokeEndpoint"],
            effect=iam.Effect.ALLOW,
            resources=["arn:aws:sagemaker:*:*:endpoint/*"]
        )

        s3_policy = iam.PolicyStatement(
            actions=["s3:*"],
            effect=iam.Effect.ALLOW,
            resources=[
                "arn:aws:s3:::sagemaker-eu-west-1-349382198749",
                "arn:aws:s3:::sagemaker-eu-west-1-349382198749/*"
                ]
        )

        self.qa_chain_lambda.role.add_to_policy(secrets_manager_policy)
        self.qa_chain_lambda.role.add_to_policy(sagemaker_policy)
        self.qa_chain_lambda.role.add_to_policy(s3_policy)

        # Create CloudWatch Log group for API gateway
        log_group = logs.LogGroup(self, "QueryChainApiLogGroup",
            log_group_name="/aws/api-gateway/rag-chain-api"
        )

        # Define REST API gateway
        self.chain_api = apigw.LambdaRestApi(
            self, "QueryChainAPI",
            handler=self.qa_chain_lambda,
            proxy=False,
            cloud_watch_role=True,
            deploy_options=apigw.StageOptions(
                access_log_destination=apigw.LogGroupLogDestination(log_group),
                access_log_format=apigw.AccessLogFormat.clf(),
            )
        )

        query_resource = self.chain_api.root.add_resource("query")
        query_resource.add_method("POST") 

        # Store API URL in SSM
        ssm.StringParameter(self, "QueryChainAPIURL",
            parameter_name="rag-chain-api-url",
            string_value=self.chain_api.url
        )

        # Create DynamoDB table to store chat history
        self.chat_history_table = dynamodb.Table(
            self, "ChatHistoryTable",
            partition_key=dynamodb.Attribute(
                name="user_id",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="timestamp",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
        )

        # Create Cognito user pool for authentication
        self.user_pool = cognito.UserPool(
            self, "UserPool",
            self_sign_up_enabled=True,
            sign_in_aliases=cognito.SignInAliases(
                email=True,
                username=True,
            ),
            auto_verify=cognito.AutoVerifiedAttrs(
                email=True
            ),
            standard_attributes=cognito.StandardAttributes(
                email=cognito.StandardAttribute(required=True, mutable=True),
            ),
            mfa=cognito.Mfa.OPTIONAL,
            mfa_second_factor=cognito.MfaSecondFactor(otp=True,),
            password_policy=cognito.PasswordPolicy(
                min_length=8,
                require_digits=True,
                require_lowercase=True,
                require_uppercase=True,
                require_symbols=True,
            ),
            account_recovery=cognito.AccountRecovery.EMAIL_ONLY,
        )

        # Create Cognito user pool client
        self.user_pool_client = self.user_pool.add_client(
            "UserPoolClient",
            generate_secret=False, # Client secret is not needed for our use case
            auth_flows=cognito.AuthFlow(
                admin_user_password=True,
                user_password=True,
                user_srp=True
            ),
            prevent_user_existence_errors=True,
            
        )

