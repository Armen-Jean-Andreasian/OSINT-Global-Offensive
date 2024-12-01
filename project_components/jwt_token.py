import jwt
import random
import string
from datetime import datetime, timedelta
from project_components import ServiceResponse


class JwtTokenFactory:
    _SECRET_KEY = ''.join(random.choice(string.ascii_lowercase) for _ in range(32))
    _ALGORITHM = "HS256"

    def __init__(self, secret_key: str, algorithm: str):
        """
        Not necessary to instantiate, but if you want to set your own secret key for all jwt tokens instead of random,
        and need to shift the algorithm, you can instantiate this class with your params, which will override
        the default params.
        """
        self._SECRET_KEY = secret_key
        self._ALGORITHM = algorithm

    @classmethod
    def generate(cls, data: dict = None, ttl: int = None):
        """
        :param data: the payload (highly optional)
        :param ttl: time to live in seconds (optional)
        """
        payload = {
            "data": data if data else {},
            "iat": datetime.utcnow(),  # issued at
        }

        if ttl:
            payload["exp"] = datetime.utcnow() + timedelta(seconds=ttl)

        return jwt.encode(payload, cls._SECRET_KEY, algorithm=cls._ALGORITHM)


class JwtTokenValidator(JwtTokenFactory):
    @classmethod
    def inspect(cls, token):
        return jwt.decode(token, cls._SECRET_KEY, algorithms=cls._ALGORITHM.split())

    @classmethod
    def validate(cls, token) -> ServiceResponse:
        try:
            jwt.decode(token, cls._SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return ServiceResponse(status=False, error="Token has expired")
        except jwt.InvalidTokenError:
            return ServiceResponse(status=False, error="Invalid token")
        else:
            return ServiceResponse(status=True)


class JwtToken(JwtTokenValidator):
    ...
