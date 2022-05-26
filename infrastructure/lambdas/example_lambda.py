import json
import os
from aws_cdk import (
    Stack,
    Duration,
)
from constructs import Construct
import aws_cdk.aws_lambda as _lambda



class ExampleLambda(Stack):
    def __init__(self, 
        scope: Construct, 
        id: str,
        description: str,    
        config: dict,
        **kwargs):
        super().__init__(scope, id,description=description, **kwargs)

        example_lambda = _lambda.Function(
            self,
            id,
            function_name=id,
            description="example handler",
            handler="index.handler",
            code=_lambda.Code.from_asset("lambda_src/example"),
            runtime=_lambda.Runtime.PYTHON_3_9,
            timeout=Duration.seconds(30),
            memory_size=512,
            environment={},
        )
    