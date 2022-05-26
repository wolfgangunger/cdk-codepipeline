#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# - Standard Library Imports -------------------------------------------------------------------------------------------
import os
import sys
import unittest
import json

# - Third Party Imports ------------------------------------------------------------------------------------------------
import pytest
from aws_cdk import(
    App,
    Stack,
    DefaultStackSynthesizer
)

# - Local Application/Library Specific Imports -------------------------------------------------------------------------
FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), r"../"))
if FOLDER not in sys.path:
    sys.path.append(FOLDER)

from infrastructure.cicd.project_pipeline_stack import ProjectPipelineStack

# - Defines ------------------------------------------------------------------------------------------------------------
CDK_JSON = os.path.abspath(
    os.path.join(os.path.dirname(__file__), r"../../cdk.json")
)


# - Functions/Classes --------------------------------------------------------------------------------------------------
class TestPipelineStack(unittest.TestCase):
    def test_create_stack_ok(self):

        # GIVEN
        with open(CDK_JSON) as json_file:
            cdk_json = json.load(json_file)
        app = App()

        region: str = cdk_json["context"]["config"]["accounts"]["tooling"]["region"]
        toolchain_account: str = cdk_json["context"]["config"]["accounts"]["tooling"]["account"]

        # WHEN
        stack = ProjectPipelineStack(
            app,
            "test-pipeline-stack",
            development_pipeline=True,
            config=cdk_json["context"]["config"],
            env={"account": toolchain_account, "region": region},
            synthesizer=DefaultStackSynthesizer(),
        )

        # THEN
        stack_artifact = app.synth().get_stack_artifact(stack.artifact_id)
        stack_art_dict = stack_artifact.template

        # CHECK
        self.assertEqual(
            True, isinstance(stack, ProjectPipelineStack)
        )
        self.assertEqual(True, isinstance(stack, Stack))
        self.assertEqual(True, isinstance(stack_art_dict, dict))
        return json.dumps(stack_art_dict)


    def test_generator_stack_pipeline_created_ok(self):
        assert "AWS::CodePipeline::Pipeline" in self.test_create_stack_ok()
# - Main ---------------------------------------------------------------------------------------------------------------

# - EOF -
