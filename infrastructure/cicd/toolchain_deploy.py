from constructs import Construct
from aws_cdk import (
    Stage,
    DefaultStackSynthesizer,
)

from infrastructure.ecr_stack import EcrStack


class ToolchainDeploy(Stage):
    def __init__(self, scope: Construct, id: str, config: dict = None, **kwargs):
        super().__init__(scope, id, **kwargs)

        ecr_repo = EcrStack(
            self,
            "EcrRepoStack",
            config=config,
            synthesizer=DefaultStackSynthesizer(),
        )
