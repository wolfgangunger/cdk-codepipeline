from aws_cdk import Stack, aws_batch as batch
from constructs import Construct
from generic.infrastructure.batch.jobdef_construct import JobDefConstruct
import aws_cdk.aws_iam as iam

### wrapper class to test a construct
class JobDefsStackTest(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        description: str,
        config: dict,
        **kwargs,
    ) -> None:

        super().__init__(scope, id, description=description, **kwargs)

        aws_region = config["accounts"][config["stage"]]["region"]
        aws_account = config["accounts"][config["stage"]]["account"]

        # the role that will be assumed by the batch job containers
        policies = [
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
            "workflow-batch-job-role",
            role_name="workflow-batch-job-role",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
            inline_policies={
                "workflow-batch-job-role-policy": iam.PolicyDocument(
                    statements=policies
                )
            },
        )

        resource_requirements = [
            batch.CfnJobDefinition.ResourceRequirementProperty(type="VCPU", value="8"),
            batch.CfnJobDefinition.ResourceRequirementProperty(
                type="MEMORY", value="16384"
            ),
            batch.CfnJobDefinition.ResourceRequirementProperty(type="GPU", value="1"),
        ]

        JobDefConstruct(
            self,
            f"test",
            image=f"{aws_account}.dkr.ecr.{aws_region}.amazonaws.com/ecr_repo",
            command=[""],
            environment=[],
            resource_requirements=resource_requirements,
            timeout=300,
            job_role_arn=self.job_role.role_arn,
        )
