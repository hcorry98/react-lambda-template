import json
from DecimalEncoder import DecimalEncoder
from urllib.parse import urlparse

class Validator:
    """Validates that the request comes from an allowed origin.

    Attributes:
        DEV_DOMAIN (str): the domain for the development environment
        PRD_DOMAIN (str): the domain for the production environment
        allowedDomains (list): the allowed domains for the project
    """

    DEV_DOMAIN = "rll-dev.byu.edu"
    PRD_DOMAIN = "rll.byu.edu"
    allowedDomains = [DEV_DOMAIN, PRD_DOMAIN]

    def __init__(self, sub: str) -> None:
        """Initialize Validator.

        Args:
            sub (str): the application name in all lowercase (i.e. projectname)
        """
        self.subdomain = sub

    def validate(self, event: dict) -> dict:
        """Validates that the request comes from an allowed origin.

        Args:
            event (dict): the event from the API Gateway request to Lambda

        Raises:
            Exception: the request does not come from an allowed domain or origin

        Returns:
            dict: the origin and domain of the request
        """
        print('Event:', event)

        origin = self.getOrigin(event)
        domain = self.getDomain(origin)
        if (domain is None):
            raise Exception('Request does not come from an allowed domain:', origin)
        if (not self.validateRequest(origin, domain)):
            raise Exception('Request does not come from an allowed origin:', origin)
        return {'origin': origin, 'domain': domain}
    
    def getOrigin(self, event: dict) -> str | None:
        """Gets the origin from the request headers.

        Args:
            event (dict): the event from the API Gateway request to Lambda

        Returns:
            str: the origin from the request headers
                or None if headers are None
                or None if origin is None
        """
        caseInsensitiveEvent = dict((key.lower(), event[key]) for key in event)
        headers = caseInsensitiveEvent.get('headers',{})
        if headers is None:
            return None
        
        caseInsensitiveHeaders = dict((key.lower(), headers[key]) for key in headers)
        origin = caseInsensitiveHeaders.get('origin', None)
        return origin
    
    def getDomain(self, origin: str) -> str | None:
        """Gets the domain from the origin.

        Args:
            origin (str): the origin from the request headers
        
        Returns:
            str: the domain from the origin
                or None if origin is None
                or None if hostname ends with an invalid environment domain
        """
        if (origin is None):
            print('No origin provided in request. Origin is None.')
            return None
        
        hostname = urlparse(origin).hostname

        if (hostname.endswith(self.DEV_DOMAIN)):
            return self.DEV_DOMAIN
        elif (hostname.endswith(self.PRD_DOMAIN)):
            return self.PRD_DOMAIN
        else:
            return None

    def validateRequest(self, origin: str, domain: str) -> bool:
        """Validates that the request comes from an allowed origin.

        Args:
            origin (str): the origin from the request headers
            domain (str): the domain from the origin
        
        Returns:
            bool: whether the request comes from an allowed origin
        """
        return origin == 'https://' + self.subdomain + '.' + domain
    
    def sendCorsResponse(self, response: dict, origin: str) -> dict:
        """Sends a response with CORS headers.

        Args:
            origin (str): the origin from the request headers
            response (dict): the response from the Lambda function

        Returns:
            dict: the response with CORS headers
        """
        responseMsg = {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': origin},
            'body': json.dumps(response, cls=DecimalEncoder)
        }
        print(responseMsg)
        return responseMsg
    