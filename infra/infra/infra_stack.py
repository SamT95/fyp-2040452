from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_iam as iam,
)
from constructs import Construct

class InfraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Define the Lambda function
        self.qa_chain_lambda = _lambda.Function(
            self, "QueryChain",
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler="lambda_handler.lambda_handler",  # File is `lambda_handler.py`, function is `lambda_handler`
            # Code comes from zipped deployment package
            code=_lambda.Code.from_asset("../backend/lambda-package.zip"), # zip containing deps, `lambda_handler.py` and other necessary python files
            environment={
                "SAGEMAKER_EXECUTION_ROLE": "arn:aws:iam::349382198749:role/SagemakerExecutionRoleCustom"
            }
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

        self.qa_chain_lambda.role.add_to_policy(secrets_manager_policy)
        self.qa_chain_lambda.role.add_to_policy(sagemaker_policy)

        # Define API gateway

        self.chain_api = apigw.LambdaRestApi(
            self, "QueryChainAPI",
            handler=self.qa_chain_lambda,
            proxy=False,
        )

        query_resource = self.chain_api.root.add_resource("query")
        query_resource.add_method("POST") 

