from constructs import Construct
from aws_cdk import (
    Stack,
    aws_s3 as s3,
)


class S3Stack(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        config: dict = None,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        repo = s3.Bucket(self, "bucket-cdk-pipeline-project-wu")
