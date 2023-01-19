from constructs import Construct
from aws_cdk import (
    aws_iam,
)


class BootstrapRole(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        toolchain_account: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        self.role = aws_iam.Role(
            self,
            id="codebuild-role-from-toolchain-account",
            role_name="codebuild-role-from-toolchain-account",
            assumed_by=aws_iam.AccountPrincipal(f"{toolchain_account}"),
            description="Role to grant access to stage accounts",
            ### TODO: Change to restricted policy
            managed_policies=[
                aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                    "AdministratorAccess"
                )
            ],
        )
