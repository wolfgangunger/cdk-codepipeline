#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# - Standard Library Imports -------------------------------------------------------------------------------------------
from operator import index
import os, sys
import boto3

# - Third Party Imports ------------------------------------------------------------------------------------------------
from aws_cdk import (
    App,
    Stack,
)
from moto import mock_s3

# - Local Application/Library Specific Imports -------------------------------------------------------------------------
FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), r"../"))
if FOLDER not in sys.path:
    sys.path.append(FOLDER)

from infrastructure.lambdas.example_lambda import ExampleLambda
from lambda_src.example_s3.index import ExampleS3

# - Defines ------------------------------------------------------------------------------------------------------------
CDK_JSON = os.path.abspath(
    os.path.join(os.path.dirname(__file__), r"../../../cdk.json")
)


# - Functions/Classes --------------------------------------------------------------------------------------------------

## TODO: test for lambda s3 stack
# class TestLambdaS3Stack(unittest.TestCase):

#     ## Test lambda infrastructure creation
#     def test_create_stack_ok(self):

#         # GIVEN
#         with open(CDK_JSON) as json_file:
#             cdk_json = json.load(json_file)
#         app = App()

#         config = cdk_json["context"]["config"]

#         # WHEN
#         stack = ExampleS3(
#             app,
#             "test-lambda-s3-stack",
#             "test-lambda-s3-stack",
#             config=config
#         )

#         # THEN
#         stack_artifact = app.synth().get_stack_artifact(stack.artifact_id)
#         stack_art_dict = stack_artifact.template

#         # CHECK
#         self.assertEqual(
#             True, isinstance(stack, ExampleS3)
#         )
#         self.assertEqual(True, isinstance(stack, Stack))
#         self.assertEqual(True, isinstance(stack_art_dict, dict))
#         return json.dumps(stack_art_dict)


## test that mocks the response of aws s3 bucket using moto library
## TODO: format this test
@mock_s3
def test_save():
    s3 = boto3.resource("s3", region_name="us-east-1")
    s3.create_bucket(Bucket="myS3bucket")

    instance = ExampleS3("test_name", "test_value")
    instance.save()

    body = s3.Object("myS3bucket", "test_name").get()["Body"].read().decode("utf-8")

    assert body == "test_value"


# - Main ---------------------------------------------------------------------------------------------------------------

# - EOF -
