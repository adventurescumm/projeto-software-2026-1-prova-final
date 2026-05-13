import jwt
import json
from functools import wraps
from flask import Flask, request, jsonify
from urllib.request import urlopen

AUTH0_DOMAIN = 'dev-7ss74shg5ie3a0l5.us.auth0.com'
API_AUDIENCE = 'https://dev-7ss74shg5ie3a0l5.us.auth0.com/api/v2/'
ALGORITHMS = ["RS256"]
jwks_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
jwks_client = jwt.PyJWKClient(jwks_url)

def token_required(required_role):
    def wrapper(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            header = request.headers.get('Authorization', None)

            if not header:
                return jsonify(
                    {
                        'message': 'Não há token'
                    }
                ), 401
            
            parts = header.split()
            token = parts[1]

            try:
                signing_key = jwks_client.get_signing_key_from_jwt(token)
                payload = jwt.decode(
                    token,
                    signing_key.key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer=f'https://{AUTH0_DOMAIN}/'
                )
                user_role = payload.get("https://social-insper.com/roles")

                print(user_role)
                print(user_role[0])
                print(required_role)

                if required_role != user_role[0] and required_role is not None:
                    return jsonify(
                        {
                            'message': f"Acesso negado! Somente {required_role} é permitido!"
                        }
                    ), 403
            except Exception as e:
                return jsonify(
                    {
                        'message': str(e)
                    }
                ), 401
            return f(*args, **kwargs)
        return decorator
    return wrapper