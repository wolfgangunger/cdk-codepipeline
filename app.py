#!/usr/bin/env python3
import os

from aws_cdk import (
    App,
)

from infrastructure.cicd.project_pipeline_stack import ProjectPipelineStack
from generic.infrastructure.iam.bootstrap_role_stack import BootstrapRoleStack

app = App()

# Read the config from cdk.json
config = app.node.try_get_context("config")
accounts = config.get("accounts")
region: str = accounts["tooling"]["region"]
dev_account: str = accounts["dev"]["account"]
qa_account: str = accounts["qa"]["account"]
prod_account: str = accounts["prod"]["account"]


### Bootstrap Stacks only to run in the first time.

# iam role for pipeline deploy dev enviroment stacks
BootstrapRoleStack(
    app,
    "bootstrap-dev-role-stack",
    account="dev",
    env={
        "account": dev_account,
        "region": region,
    },
)

# iam role for pipeline deploy qa enviroment stacks
BootstrapRoleStack(
    app,
    "bootstrap-qa-role-stack",
    account="dev",
    env={
        "account": qa_account,
        "region": region,
    },
)

# iam role for pipeline deploy prod enviroment stacks
BootstrapRoleStack(
    app,
    "bootstrap-prod-role-stack",
    account="dev",
    env={
        "account": prod_account,
        "region": region,
    },
)


##Pipeline Dev/QA
ProjectPipelineStack(
    app,
    "cdk-pipeline",
    development_pipeline=True,
    env=accounts.get("tooling"),
    config={**config},
)


# ## Pipeline Prod
# ProjectPipelineStack(
#     app,
#     "testExample-pipeline",
#     development_pipeline=False,
#     env=accounts.get("tooling"),
#     config={**config},
# )

app.synth()
