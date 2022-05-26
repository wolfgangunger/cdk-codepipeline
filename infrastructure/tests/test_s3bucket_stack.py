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

from infrastructure.s3bucket_stack import S3Stack

# - Defines ------------------------------------------------------------------------------------------------------------
CDK_JSON = os.path.abspath(
    os.path.join(os.path.dirname(__file__), r"../../cdk.json")
)


# - Functions/Classes --------------------------------------------------------------------------------------------------
class TestEcrStack(unittest.TestCase):
    def test_create_stack_ok(self):

        # GIVEN
        with open(CDK_JSON) as json_file:
            cdk_json = json.load(json_file)
        app = App()

        # WHEN
        stack = S3Stack(
            app,
            "test-s3Bucket-stack",
        )
    
        # THEN
        stack_artifact = app.synth().get_stack_artifact(stack.artifact_id)
        stack_art_dict = stack_artifact.template

        # CHECK
        self.assertEqual(
            True, isinstance(stack, S3Stack)
        )
        self.assertEqual(True, isinstance(stack, Stack))
        self.assertEqual(True, isinstance(stack_art_dict, dict))
        return json.dumps(stack_art_dict)

    def test_ecr_repo_created_ok(self):
        assert "AWS::S3::Bucket" in self.test_create_stack_ok()


# - Main ---------------------------------------------------------------------------------------------------------------

# - EOF -
