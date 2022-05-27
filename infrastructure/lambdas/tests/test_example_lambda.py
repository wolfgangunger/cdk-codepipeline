#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# - Standard Library Imports -------------------------------------------------------------------------------------------
from operator import index
import os, sys
import json
import unittest

# - Third Party Imports ------------------------------------------------------------------------------------------------
from aws_cdk import (
    App,
    Stack,
)

# - Local Application/Library Specific Imports -------------------------------------------------------------------------
FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), r"../"))
if FOLDER not in sys.path:
    sys.path.append(FOLDER)

from infrastructure.lambdas.example_lambda import ExampleLambda
from lambda_src.example.index import lambda_handler, multiply, sum

# - Defines ------------------------------------------------------------------------------------------------------------
CDK_JSON = os.path.abspath(
    os.path.join(os.path.dirname(__file__), r"../../../cdk.json")
)

# - Functions/Classes --------------------------------------------------------------------------------------------------
class TestLambdaStack(unittest.TestCase):

    ## Test lambda infrastructure creation
    def test_create_stack_ok(self):

        # GIVEN
        with open(CDK_JSON) as json_file:
            cdk_json = json.load(json_file)
        app = App()

        config = cdk_json["context"]["config"]

        # WHEN
        stack = ExampleLambda(
            app, "test-lambda-stack", "test-lambda-stack", config=config
        )

        # THEN
        stack_artifact = app.synth().get_stack_artifact(stack.artifact_id)
        stack_art_dict = stack_artifact.template

        # CHECK
        self.assertEqual(True, isinstance(stack, ExampleLambda))
        self.assertEqual(True, isinstance(stack, Stack))
        self.assertEqual(True, isinstance(stack_art_dict, dict))
        return json.dumps(stack_art_dict)


class LambdaFunctionTests(unittest.TestCase):

    # GIVEN
    def setUp(self):
        self.event = {"numbers": [3, 5]}
        self.a = 3
        self.b = 5

    def test_lambda_handler(self):

        # WHEN
        result = lambda_handler(self.event, "")
        # THEN
        data = json.loads(result["body"])
        expected_response = {"addition": 8, "multiplication": 15}
        # CHECK
        self.assertEqual(data, expected_response)

    def test_sum(self):

        # WHEN
        result = sum(self.a, self.b)
        # CHECK
        self.assertEqual(result, self.a + self.b)

    def test_func_multiply(self):

        # WHEN
        result = multiply(self.a, self.b)
        # CHECK
        self.assertEqual(result, self.a * self.b)


# - Main ---------------------------------------------------------------------------------------------------------------

# - EOF -
