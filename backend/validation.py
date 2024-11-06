import os
import jwt
import requests
from dotenv import load_dotenv
from jwt import PyJWKClient

# Load environment variables
load_dotenv()

# Constants
TENANT_ID = os.getenv('TENANT_ID')
CLIENT_ID = os.getenv("CLIENT_ID")  # Optional: to verify the audience claim
OPENID_CONFIG_URL = f'https://login.microsoftonline.com/{TENANT_ID}/v2.0/.well-known/openid-configuration'

# Get the JWKS (public keys)
def get_jwks():
    openid_config = requests.get(OPENID_CONFIG_URL).json()
    jwks_uri = openid_config['jwks_uri']
    jwks_client = PyJWKClient(jwks_uri)
    return jwks_client

# Function to validate token
def validate_token(token):
    jwks_client = get_jwks()
    signing_key = jwks_client.get_signing_key_from_jwt(token)

    try:
        # Decode and verify the token
        decoded_token = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience=CLIENT_ID,
            issuer=f"https://login.microsoftonline.com/{TENANT_ID}/v2.0"
        )
        return decoded_token  # Token is valid
    except jwt.ExpiredSignatureError:
        print("Token has expired")
    except jwt.InvalidAudienceError:
        print("Invalid audience")
    except jwt.InvalidIssuerError:
        print("Invalid issuer")
    except jwt.PyJWTError as e:
        print(f"Token validation error: {e}")
    return None

# Example usage
# token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IjNQYUs0RWZ5Qk5RdTNDdGpZc2EzWW1oUTVFMCJ9.eyJhdWQiOiI5MDBlZjM0My04YjY2LTRmZjUtYjUwYi0wNGFlZjkyNzYzZWQiLCJpc3MiOiJodHRwczovL2xvZ2luLm1pY3Jvc29mdG9ubGluZS5jb20vNzBhMjg1MjItOTY5Yi00NTFmLWJkYjItYWJmZWEzYWFhNWJmL3YyLjAiLCJpYXQiOjE3MzA4MTY4NjksIm5iZiI6MTczMDgxNjg2OSwiZXhwIjoxNzMwODIwNzY5LCJuYW1lIjoi0J_QtdGC0YDRltCyINCS0L7Qu9C-0LTQuNC80LjRgCIsIm5vbmNlIjoiMjExMTJkNmMtNDM0MS00YzMwLWE2MzItMWNiNTk3OGZmNjRjIiwib2lkIjoiYzU1MTBjZDItYTYyNy00MWVmLThiNmYtY2E4ODJiZjNjM2NiIiwicHJlZmVycmVkX3VzZXJuYW1lIjoiVk9MT0RZTVlSLlBFVFJJVkBsbnUuZWR1LnVhIiwicmgiOiIxLkFYUUFJb1dpY0p1V0gwVzlzcXYtbzZxbHYwUHpEcEJtaV9WUHRRc0VydmtuWS0xMEFPWjBBQS4iLCJzdWIiOiJnUU9nT3NLTzY5c05tRy1nLWEyOTFwR3BXMnBldHhlS0JtTTBfckwyajNzIiwidGlkIjoiNzBhMjg1MjItOTY5Yi00NTFmLWJkYjItYWJmZWEzYWFhNWJmIiwidXRpIjoibjhyb1Q0VUpyRU9uRzBnXy03eWxBQSIsInZlciI6IjIuMCJ9.Iz94NX6CLMQUUfsG28piVrru_nMQnoiX_GDSHnS9H5OPBtM5mkf8yO5Q57Cf7mYH0JBhy3yxs9uvx8V4BnBkI3kNGX6GnpcafRaIpd-imZBzuZpOMHMkrhraDvN7CAMaC1K0ycTDxfImSub8XEnDNZEzrnu35NhK_lsHFbaZK7dIC_ZPcqolBRJ6IG5O2yniVFmcffCE714-s5I0NHU2hUdZkKFH3LcLurjpGdj3FU4uwGz65TxqJVsoMTP4paAHv0ytEmkUaIdiTbEff7Nz7YevV55Lc0Hp9_l3vhV1GhFgGSpk1LxGYYjJdfTQROXZUC4qDPjkpidnsn3JX2ktKg"
# decoded = validate_token(token)
# if decoded:
#     print("Token is valid:", decoded)
# else:
#     print("Token is invalid")
