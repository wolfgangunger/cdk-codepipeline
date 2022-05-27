from aws_cdk import Stage, DefaultStackSynthesizer
from constructs import Construct

from infrastructure.ecr_stack import EcrStack
from infrastructure.lambdas.example_lambda import ExampleLambda
from infrastructure.s3bucket_stack import S3Stack
from infrastructure.batch.job_defs_stack import JobDefsStack


class AppDeployBootstrap(Stage):
    def __init__(self, scope: Construct, id: str, config: dict = None, **kwargs):
        super().__init__(scope, id, **kwargs)

        ecr_repo = EcrStack(
            self,
            "EcrRepoStack",
            config=config,
            synthesizer=DefaultStackSynthesizer(),
        )


class AppDeploy(Stage):
    def __init__(self, scope: Construct, id: str, config: dict = None, **kwargs):
        super().__init__(scope, id, **kwargs)

        # s3 bucket Stack Example
        s3bucket = S3Stack(self, "S3Stack", config=config)

        # put stage id into configuration object for use in JobDefStack
        config["stage"] = id
        # Job Definition Example
        jobdefs = JobDefsStack(
            self,
            "Job-Defs",
            "JobDefinitions",
            config,
        )

        # lambda Stack example
        example_lambda = ExampleLambda(
            self,
            "LambdaStack",
            "LambdaDesciption",
            config=config,
        )
