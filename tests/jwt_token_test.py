import unittest
import jwt
from datetime import datetime, timedelta
import random
import string
from project_components import JwtToken



class TestJwtToken(unittest.TestCase):

    def test_generate_token_without_expiry(self):
        # Generate a token with no expiration
        token = JwtToken.generate(data={"user_id": 123})
        self.assertIsInstance(token, str)
        decoded = JwtToken.inspect(token)
        self.assertEqual(decoded['data']['user_id'], 123)
        self.assertIn('iat', decoded)
        self.assertNotIn('exp', decoded)

    def test_generate_token_with_expiry(self):
        # Generate a token with expiration time (TTL)
        token = JwtToken.generate(data={"user_id": 123}, ttl=3600)
        self.assertIsInstance(token, str)
        decoded = JwtToken.inspect(token)
        self.assertEqual(decoded['data']['user_id'], 123)
        self.assertIn('iat', decoded)
        self.assertIn('exp', decoded)

    def test_validate_valid_token(self):
        # Generate a token with payload and validate it
        token = JwtToken.generate(data={"user_id": 123}, ttl=3600)
        validation_result = JwtToken.validate(token)
        self.assertTrue(validation_result['valid'])
        self.assertEqual(validation_result['data']['data']['user_id'], 123)

    def test_validate_invalid_token(self):
        # Try validating an invalid token (wrong secret or tampered)
        invalid_token = 'invalid.token.string'
        validation_result = JwtToken.validate(invalid_token)
        self.assertFalse(validation_result.status)
        self.assertEqual(validation_result.error, 'Invalid token')

    def test_validate_expired_token(self):
        # Generate a token with an expiration and wait for it to expire
        expired_token = JwtToken.generate(data={"user_id": 123},
                                          ttl=-1)  # TTL of -1 makes the token expired immediately
        validation_result = JwtToken.validate(expired_token)
        self.assertFalse(validation_result.status)
        self.assertEqual(validation_result.error, 'Token has expired')


if __name__ == '__main__':
    unittest.main()
