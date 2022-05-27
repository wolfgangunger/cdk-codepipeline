#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# - Standard Library Imports -------------------------------------------------------------------------------------------
import os
import sys
import unittest
import json

# - Third Party Imports ------------------------------------------------------------------------------------------------
from aws_cdk import Stack, App, assertions


# - Local Application/Library Specific Imports -------------------------------------------------------------------------
FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), r"../"))
if FOLDER not in sys.path:
    sys.path.append(FOLDER)


import test_wrapper.jobdef_construct_stack

# - Defines ------------------------------------------------------------------------------------------------------------
CDK_JSON = os.path.abspath(
    os.path.join(os.path.dirname(__file__), r"../../../cdk.json")
)

## test to test a construct using a wrapper calls ( s stack creating the construct)
### problem importing the wrapper stack class inside this package
class TestJobDefsConstruct(unittest.TestCase):
    def test_create_job_defs_construct_ok(self):

        # GIVEN
        with open(CDK_JSON) as json_file:
            cdk_json = json.load(json_file)
        app = App()

        # WHEN
        config = cdk_json["context"]["config"]

        # set dev as a stage if no stage is informed
        config.setdefault("stage", "dev")

        # create a dummy stack to test
        stack = test_wrapper.jobdef_construct_stack.JobDefsStackTest(
            app, "Test-Job-defs-Stack", "Test-Job-Defs-Stack", config
        )

        # THEN
        stack_artifact = app.synth().get_stack_artifact(stack.artifact_id)
        stack_art_dict = stack_artifact.template

        # CHECK
        self.assertEqual(
            True,
            isinstance(stack, test_wrapper.jobdef_construct_stack.JobDefsStackTest),
        )
        self.assertEqual(True, isinstance(stack, Stack))
        self.assertEqual(True, isinstance(stack_art_dict, dict))
        return json.dumps(stack_art_dict)
