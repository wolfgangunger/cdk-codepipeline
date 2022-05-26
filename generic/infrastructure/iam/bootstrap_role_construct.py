from constructs import Construct
from aws_cdk import(
    aws_iam,
)

class BootstrapRole(Construct):
    def __init__(
        self, 
        scope: Construct,
        id: str,       
        **kwargs,
    ) -> None:   
        super().__init__(scope, id, **kwargs)

        self.role = aws_iam.Role(
            self,
            id="cicd-codebuild-role-from-toolchain-account",
            assumed_by= aws_iam.ServicePrincipal("codepipeline.amazonaws.com"),
            description="Role to deploy codepipeline stacks",
        ) 
        ### TODO: Change to restricted policy
        self.role.add_managed_policy(aws_iam.ManagedPolicy.from_managed_policy_name(self,id,"AdministratorAccess")) 

        