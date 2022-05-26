#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# - Standard Library Imports -------------------------------------------------------------------------------------------
import os
import sys
import unittest
import json

# - Third Party Imports ------------------------------------------------------------------------------------------------
from aws_cdk import (
    App,
    Stack,
)

# - Local Application/Library Specific Imports -------------------------------------------------------------------------
FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), r"../"))
if FOLDER not in sys.path:
    sys.path.append(FOLDER)

from infrastructure.batch.job_defs_stack import JobDefsStack

# - Defines ------------------------------------------------------------------------------------------------------------
CDK_JSON = os.path.abspath(
    os.path.join(os.path.dirname(__file__), r"../../cdk.json")
)


# - Functions/Classes --------------------------------------------------------------------------------------------------
class TestJobDefsStack(unittest.TestCase):
    def test_create_stack_ok(self):

        # GIVEN
        with open(CDK_JSON) as json_file:
            cdk_json = json.load(json_file)
        app = App()

        config = cdk_json["context"]["config"]

        #set dev as a stage if no stage is informed
        config.setdefault("stage","dev")        

        # WHEN  
        stack = JobDefsStack(
            app,
            "test-jobdefs-stack",
            "test-jobdefs-stack",
            config=config,
        )
    
        # THEN
        stack_artifact = app.synth().get_stack_artifact(stack.artifact_id)
        stack_art_dict = stack_artifact.template

        # CHECK
        self.assertEqual(
            True, isinstance(stack, JobDefsStack)
        )
        self.assertEqual(True, isinstance(stack, Stack))
        self.assertEqual(True, isinstance(stack_art_dict, dict))
        return json.dumps(stack_art_dict)

    def test_ecr_repo_created_ok(self):
        assert "AWS::Batch::JobDefinition" in self.test_create_stack_ok()


# - Main ---------------------------------------------------------------------------------------------------------------

# - EOF -
