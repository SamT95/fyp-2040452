from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_iam as iam,
    aws_secretsmanager as secretsmanager
)
from constructs import Construct

class InfraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Retrieve the Lambda Layer ARN from Secrets Manager
        # layer_arn_secret = secretsmanager.Secret.from_secret_name_v2(self, "LambdaLayerARN", "rag-layer-arn")
        # layer_arn = layer_arn_secret.secret_value.to_string()

        # Reference existing layer for lambda function
        # dependency_layer = _lambda.LayerVersion.from_layer_version_arn(
        #     self, "DependencyLayer",
        #     layer_version_arn=layer_arn
        # )

        # Define the Lambda function
        self.qa_chain_lambda = _lambda.Function(
            self, "QueryChain",
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler="lambda_handler.lambda_handler",  # File is `lambda_handler.py`, function is `lambda_handler`
            # Code comes from zipped deployment package
            code=_lambda.Code.from_asset("../backend/rag"), # Code for the RAG chain and lambda handler
            environment={
                "SAGEMAKER_EXECUTION_ROLE": "arn:aws:iam::349382198749:role/SagemakerExecutionRoleCustom"
            },
            # layers=[dependency_layer],
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

        # Define API gateway

        self.chain_api = apigw.LambdaRestApi(
            self, "QueryChainAPI",
            handler=self.qa_chain_lambda,
            proxy=False,
        )

        query_resource = self.chain_api.root.add_resource("query")
        query_resource.add_method("POST") 

