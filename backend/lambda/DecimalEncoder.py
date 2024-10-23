from decimal import Decimal
import json

class DecimalEncoder(json.JSONEncoder):
    """Custom JSON encoder for Decimal objects."""

    def default(self, o: object) -> object:
        """Converts Decimal objects to strings to maintain accuracy and allow for json serialization.

        Args:
            o (object): the object to encode

        Returns:
            object: if the object is a Decimal it will be converted to a string
                        else, the object will remain the same
        """
        if isinstance(o, Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)