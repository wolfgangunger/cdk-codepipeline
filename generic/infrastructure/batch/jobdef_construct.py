from aws_cdk import (
    Stack,
    CfnOutput,
    Duration,
)
from constructs import Construct
import aws_cdk.aws_iam as iam

from aws_cdk import aws_batch as batch


class JobDefConstruct(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        image: str,
        command,
        environment,
        resource_requirements,
        timeout: int,
        job_role_arn,
        **kwargs,
    ) -> None:
        """
        Stack creating a single Job Definitions based on the parameters:

        Stack is  generic
        """
        super().__init__(scope, id, **kwargs)

        self.jobdefinition = batch.CfnJobDefinition(
            self,
            id=f"{id}-job-definition",
            type="container",
            container_properties=batch.CfnJobDefinition.ContainerPropertiesProperty(
                image=image,
                command=command,
                resource_requirements=resource_requirements,
                job_role_arn=job_role_arn,
                execution_role_arn=job_role_arn,
                privileged=True,
                environment=environment,
            ),
            job_definition_name=f"{id}-job-definition",
            platform_capabilities=["EC2"],
            timeout=Duration.seconds(timeout),
        )

        jobdef_export = CfnOutput(
            self,
            f"{id}-job-definition-name",
            export_name=f"{id}-job-definition-name",
            value=self.jobdefinition.job_definition_name,
        )
