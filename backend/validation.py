import os
import jwt
import requests
from dotenv import load_dotenv
from jwt import PyJWKClient

# Load environment variables
load_dotenv()

# Constants
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")  # Optional: to verify the audience claim
OPENID_CONFIG_URL = f"https://login.microsoftonline.com/{TENANT_ID}/v2.0/.well-known/openid-configuration"


# Get the JWKS (public keys)
def get_jwks():
    openid_config = requests.get(OPENID_CONFIG_URL).json()
    jwks_uri = openid_config["jwks_uri"]
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
            issuer=f"https://login.microsoftonline.com/{TENANT_ID}/v2.0",
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
