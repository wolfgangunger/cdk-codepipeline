from constructs import Construct
from aws_cdk import (
    Stack,
    aws_iam as iam,
    pipelines,
    aws_codebuild,
    Duration,
)
from aws_cdk.aws_codebuild import BuildEnvironment
from aws_cdk.pipelines import CodePipeline

from infrastructure.cicd.app_deploy import AppDeploy, AppDeployBootstrap
from infrastructure.cicd.toolchain_deploy import ToolchainDeploy


class PipelineStack(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        development_pipeline: bool,
        config: dict = None,
        **kwargs,
    ):
        super().__init__(scope, id, **kwargs)

        accounts = config.get("accounts")
        region: str = accounts["tooling"]["region"]
        dev_account: str = accounts["dev"]["account"]
        qa_account: str = accounts["qa"]["account"]
        toolchain_account: str = accounts["tooling"]["account"]
        prod_account: str = accounts["prod"]["account"]
        codestar_connection_arn = config.get("connection_arn")
        repo_owner = config.get("owner")
        repo = config.get("repo")

        synth_dev_account_role_arn = (
            f"arn:aws:iam::{dev_account}:role/codebuild-role-from-toolchain-account"
        )

        synth_qa_account_role_arn = (
            f"arn:aws:iam::{qa_account}:role/codebuild-role-from-toolchain-account"
        )
        synth_prod_account_role_arn = (
            f"arn:aws:iam::{prod_account}:role/codebuild-role-from-toolchain-account"
        )

        # creating the pipline with  synch action
        git_input = pipelines.CodePipelineSource.connection(
            repo_string=f"{repo_owner}/{repo}",
            # branch=branch_name,
            branch=config["development_branch"]
            if development_pipeline
            else config["production_branch"],
            connection_arn=codestar_connection_arn,
        )
        synth_step = self.get_synth_step(
            git_input,
            synth_dev_account_role_arn,
            synth_qa_account_role_arn,
            synth_prod_account_role_arn,
        )

        pipeline = CodePipeline(
            self,
            id,
            synth=synth_step,
            cross_account_keys=True,
            code_build_defaults=pipelines.CodeBuildOptions(
                build_environment=BuildEnvironment(
                    build_image=aws_codebuild.LinuxBuildImage.STANDARD_5_0,
                    privileged=True,
                )
            ),
        )

        toolchain_app = ToolchainDeploy(
            self,
            "toolchain",
            config=config,
            env={
                "account": toolchain_account,
                "region": region,
            },
        )

        toolchain_stage = pipeline.add_stage(toolchain_app)

        ## add unit tests for toolchain to run before toolchain
        infrastructure_unit_tests = self.get_infrastructure_unit_tests(git_input)
        if infrastructure_unit_tests != None:
            toolchain_stage.add_pre(infrastructure_unit_tests)

        ##  lambda tests
        lambda_tests = self.get_lambda_tests(git_input)
        if lambda_tests != None:
            toolchain_stage.add_pre(lambda_tests)

        if development_pipeline:
            # Deploy bootstrap
            dev_app_bootstrap = AppDeployBootstrap(
                self,
                "devbootstrap",
                config=config,
                env={
                    "account": dev_account,
                    "region": region,
                },
            )
            dev_bootstrap_stage = pipeline.add_stage(dev_app_bootstrap)

            # Dev deploy
            dev_app = AppDeploy(
                self,
                "dev",
                config=config,
                env={
                    "account": dev_account,
                    "region": region,
                },
            )
            ## deploy dev stack
            dev_stage = pipeline.add_stage(dev_app)

            ## integration tests
            dev_int_tests = self.get_dev_int_tests(
                git_input, region, dev_account, synth_dev_account_role_arn
            )
            if dev_int_tests != None:
                dev_stage.add_post(dev_int_tests)

            ## acceptance tests
            dev_acceptance_tests = self.get_dev_acceptance_tests(
                git_input, region, dev_account, synth_dev_account_role_arn
            )
            if dev_acceptance_tests != None:
                dev_stage.add_post(dev_acceptance_tests)

            # manual approval for QA
            dev_stage.add_post(pipelines.ManualApprovalStep("ApprovalQA"))

            ## QA boostrap deploy
            qa_app_bootstrap = AppDeployBootstrap(
                self,
                "qabootstrap",
                config=config,
                env={
                    "account": qa_account,
                    "region": region,
                },
            )
            qa_bootstrap_stage = pipeline.add_stage(qa_app_bootstrap)

            ## QA deploy
            qa_app = AppDeploy(
                self,
                "qa",
                config=config,
                env={
                    "account": qa_account,
                    "region": region,
                },
            )
            qa_stage = pipeline.add_stage(qa_app)

            ## QA acceptance tests
            qa_acceptance_tests = self.get_qa_acceptance_tests(
                git_input, qa_account, synth_qa_account_role_arn
            )
            if qa_acceptance_tests != None:
                qa_stage.add_post(qa_acceptance_tests)

            qa_stage.add_post(pipelines.ManualApprovalStep("ApprovalProd"))

        else:

            prod_bootstrap = AppDeployBootstrap(
                self,
                "prodbootstrap",
                config=config,
                env={
                    "account": prod_account,
                    "region": region,
                },
            )

            prod_bootstrap_stage = pipeline.add_stage(prod_bootstrap)

            # Deploy Prod
            prod_app = AppDeploy(
                self,
                "prod",
                config=config,
                env={
                    "account": prod_account,
                    "region": region,
                },
            )
            prod_stage = pipeline.add_stage(prod_app)

    ########## methods to be overwritten in subclass
    def get_synth_step(
        self,
        git_input,
        synth_dev_account_role_arn,
        synth_qa_account_role_arn,
        synth_prod_account_role_arn,
    ):
        synth_step = pipelines.CodeBuildStep(
            "Synth",
            input=git_input,
            commands=self.get_synth_step_commands(),
            role_policy_statements=[
                iam.PolicyStatement(
                    actions=["sts:AssumeRole"],
                    effect=iam.Effect.ALLOW,
                    resources=[
                        synth_dev_account_role_arn,
                        synth_qa_account_role_arn,
                        synth_prod_account_role_arn,
                    ],
                ),
            ],
        )
        return synth_step

    def get_synth_step_commands(self) -> list:
        commands = [
            "npm install -g aws-cdk",
            "python -m pip install -r requirements.txt",
            "cdk list && cdk synth",
        ]
        return commands

    def get_infrastructure_unit_tests(self, git_input):
        infrastructure_unit_tests = pipelines.CodeBuildStep(
            "UnitTests",
            input=git_input,
            commands=self.get_infrastructure_unit_tests_commands(),
        )
        return infrastructure_unit_tests

    def get_infrastructure_unit_tests_commands(self) -> list:
        commands = [
            "pip install -r requirements.txt && pip install -r requirements-dev.txt",
            "pytest -vvvv -s generic/infrastructure/tests",
        ]
        return commands

    ####
    def get_lambda_tests(self, git_input):
        infrastructure_unit_tests = pipelines.CodeBuildStep(
            "LambdaTests",
            input=git_input,
            commands=self.get_lambda_tests_commands(),
        )
        return infrastructure_unit_tests

    def get_lambda_tests_commands(self) -> list:
        commands = [
            "pip install -r requirements.txt && pip install -r requirements-dev.txt",
            "pytest -vvvv -s infrastructure/lambdas/tests",
        ]
        return commands

    def get_dev_int_tests(self, git_input, region, dev_account, dev_account_role_arn):
        dev_int_tests = pipelines.CodeBuildStep(
            "IntegrationTests",
            input=git_input,
            build_environment=aws_codebuild.BuildEnvironment(
                build_image=aws_codebuild.LinuxBuildImage.AMAZON_LINUX_2_3,
                privileged=True,
            ),
            commands=self.get_dev_int_tests_commands(
                region, dev_account, dev_account_role_arn
            ),
            role_policy_statements=[
                iam.PolicyStatement(
                    actions=["sts:AssumeRole"],
                    effect=iam.Effect.ALLOW,
                    resources=[dev_account_role_arn],
                )
            ],
        )
        return dev_int_tests

    def get_dev_int_tests_commands(
        self, region, dev_account, dev_account_role_arn
    ) -> list:
        ### setting temp credentials to access stage account
        commands = [
            "pip install -r requirements.txt && pip install -r requirements-dev.txt",
            "docker ps",
            f"REGION={region}",
            f"ACCOUNT_ID={dev_account}",
            f'TEMP_CREDS=$(aws sts assume-role --role-arn {dev_account_role_arn} --role-session-name "integration-test")',
            "export TEMP_CREDS",
            'export ACCESS_KEY_ID=$(echo "${TEMP_CREDS}" | jq -r ".Credentials.AccessKeyId")',
            'export SECRET_ACCESS_KEY_ID=$(echo "${TEMP_CREDS}" | jq -r ".Credentials.SecretAccessKey")',
            'export TOKEN=$(echo "${TEMP_CREDS}" | jq -r ".Credentials.SessionToken")',
            'AWS_ACCESS_KEY_ID="${ACCESS_KEY_ID}" AWS_SECRET_ACCESS_KEY="${SECRET_ACCESS_KEY_ID}" AWS_SESSION_TOKEN="${TOKEN}" pytest -vvvv -s tests/integration/',
        ]
        return commands

    def get_dev_acceptance_tests(
        self, git_input, region, dev_account, dev_account_role_arn
    ):
        tests = pipelines.CodeBuildStep(
            "AcceptanceTests",
            input=git_input,
            build_environment=aws_codebuild.BuildEnvironment(
                build_image=aws_codebuild.LinuxBuildImage.AMAZON_LINUX_2_3,
                privileged=True,
            ),
            env={"SKIP_TESTS": "0"},
            timeout=Duration.minutes(180),
            commands=self.get_dev_acceptance_tests_commands(region, dev_account),
            role_policy_statements=[
                iam.PolicyStatement(
                    actions=["sts:AssumeRole"],
                    effect=iam.Effect.ALLOW,
                    resources=[dev_account_role_arn],
                ),
                iam.PolicyStatement(
                    actions=[
                        "cloudwatch:PutMetricData",
                        "cloudwatch:GetMetricData",
                    ],
                    effect=iam.Effect.ALLOW,
                    resources=["*"],
                ),
            ],
        )
        return tests

    def get_dev_acceptance_tests_commands(self, region, dev_account) -> list:
        commands = [
            "pip install -r requirements.txt && pip install -r requirements-dev.txt",
            "chmod 777 tests/acceptance/tests.sh",
            f"tests/acceptance/tests.sh {dev_account}",
        ]
        return commands

    def get_qa_acceptance_tests(self, git_input, qa_account, qa_account_role_arn):
        tests = pipelines.CodeBuildStep(
            "AcceptanceTests",
            input=git_input,
            build_environment=aws_codebuild.BuildEnvironment(
                build_image=aws_codebuild.LinuxBuildImage.AMAZON_LINUX_2_3,
                privileged=True,
            ),
            commands=self.get_qa_acceptance_tests_commands(qa_account),
            role_policy_statements=[
                iam.PolicyStatement(
                    actions=["sts:AssumeRole"],
                    effect=iam.Effect.ALLOW,
                    resources=[qa_account_role_arn],
                ),
            ],
        )
        return tests

    def get_qa_acceptance_tests_commands(self, qa_account) -> list:
        commands = [
            "pip install -r requirements.txt && pip install -r requirements-dev.txt",
            "chmod 777 tests/acceptance/tests.sh",
            f"tests/acceptance/tests.sh {qa_account}",
        ]
        return commands
