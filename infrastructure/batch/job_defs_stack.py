from aws_cdk import (
    Stack,
    CfnOutput,
)
from constructs import Construct
import aws_cdk.aws_iam as iam

from aws_cdk import aws_batch as batch
from generic.infrastructure.batch.jobdef_construct import JobDefConstruct


class JobDefsStack(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        description: str,
        config: dict,
        **kwargs,
    ) -> None:
        """
        Stack creating the Job Definitions based on the published images:

        Stack is not generic, will contain project specific informations
        please review to use your project specific information

        """
        super().__init__(scope, id, description=description, **kwargs)

        aws_region = config["accounts"][config["stage"]]["region"]
        aws_account = config["accounts"][config["stage"]]["account"]
        current_stage = config.get("stage", None)

        # the role that will be assumed by the batch job containers
        policies = [
            iam.PolicyStatement(
                actions=[
                    "cloudwatch:PutMetricData",
                    "cloudwatch:GetMetricData",
                    "cloudwatch:PutMetricStream",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents",
                ],
                effect=iam.Effect.ALLOW,
                resources=["*"],
            ),
            iam.PolicyStatement(
                actions=[
                    "ecr:BatchGetImage",
                    "ecr:DescribeImages",
                    "ecr:GetAuthorizationToken",
                    "ecr:ListImages",
                    "ecr:DescribeRepositories",
                    "ecr:GetDownloadUrlForLayer",
                    "ecr:BatchCheckLayerAvailability",
                ],
                effect=iam.Effect.ALLOW,
                resources=["*"],
            ),
        ]

        self.job_role = iam.Role(
            self,
            "batch-job-role-uw",
            role_name="batch-job-role-wu",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
            inline_policies={
                "batch-job-role-policy": iam.PolicyDocument(statements=policies)
            },
        )

        role_export1 = CfnOutput(
            self,
            f"{id}-batch-job-role-uw",
            export_name=f"{id}-batch-job-role-uw",
            value=self.job_role.role_arn,
        )

        command = ["/bin/bash", "-c", "/home/mts/runAll.sh"]
        timeout = 300
        # replace the enviroment variables for your project
        environment = [
            batch.CfnJobDefinition.EnvironmentProperty(name="PARAM", value="VALUE"),
        ]

        resource_requirements = [
            batch.CfnJobDefinition.ResourceRequirementProperty(type="VCPU", value="8"),
            batch.CfnJobDefinition.ResourceRequirementProperty(
                type="MEMORY", value="16384"
            ),
            batch.CfnJobDefinition.ResourceRequirementProperty(type="GPU", value="1"),
        ]

        # image required, please replace with the project information
        image: str = "image"
        JobDefConstruct(
            self,
            f"{id}-projectname-{image.replace('.', '-')}",
            image=f"{aws_account}.dkr.ecr.{aws_region}.amazonaws.com/ecr-repo:{image}",
            command=command,
            environment=environment,
            resource_requirements=resource_requirements,
            timeout=timeout,
            job_role_arn=self.job_role.role_arn,
        )
