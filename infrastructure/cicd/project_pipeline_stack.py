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
        super().__init__(scope, id, development_pipeline=development_pipeline, config=config,**kwargs)

     