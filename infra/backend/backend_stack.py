from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_iam as iam,
    aws_ssm as ssm,
    aws_lambda_python_alpha as _alambda
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

        # Define API gateway

        self.chain_api = apigw.LambdaRestApi(
            self, "QueryChainAPI",
            handler=self.qa_chain_lambda,
            proxy=False,
        )

        query_resource = self.chain_api.root.add_resource("query")
        query_resource.add_method("POST") 

        # Store API URL in SSM
        ssm.StringParameter(self, "QueryChainAPIURL",
            parameter_name="rag/chain-api-url",
            string_value=self.chain_api.url
        )

