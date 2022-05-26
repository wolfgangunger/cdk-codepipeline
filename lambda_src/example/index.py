import json


def lambda_handler(event, context):
    numbers = event['numbers']
    response = json.dumps({"addition":sum(numbers[0],numbers[1]), "multiplication":multiply(numbers[0],numbers[1])})
    return {
        "statusCode": 200,
        "body": response,
    }

def sum(a,b):
    return a+b

def multiply(a,b):
    return a * b

