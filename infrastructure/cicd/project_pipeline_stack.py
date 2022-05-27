from constructs import Construct
from generic.infrastructure.cicd.pipeline_stack import PipelineStack


class ProjectPipelineStack(PipelineStack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        development_pipeline: bool,
        config: dict = None,
        **kwargs,
    ):
        super().__init__(
            scope,
            id,
            development_pipeline=development_pipeline,
            config=config,
            **kwargs,
        )

    ## method overwrites
    def get_infrastructure_unit_tests_commands(self) -> list:
        ## add project specific tests to command
        commands = [
            "pip install -r requirements.txt && pip install -r requirements-dev.txt",
            "pytest -vvvv -s infrastructure/tests",
            "pytest -vvvv -s generic/infrastructure/tests",
        ]
        return commands
