from Validator import Validator

# Replace with the Filename and function name
from Function import function

# Replace with the app name
SUBDOMAIN = 'appname'

validator = Validator(SUBDOMAIN)

def handle_function(event: dict, context: dict) -> dict:
    """An example function to demostrate running a Lambda function using the API Gateway request.

    Args:
        event (dict): the event from the API Gateway request to Lambda
        context (dict): the context of the Lambda function

    Returns:
        dict: the response from starting the Lambda Function via Validator
    """
    results = validator.validate(event)
    # Replace 'function()' with the name of your lambda function
    return validator.sendCorsResponse(function(), results['origin'])
