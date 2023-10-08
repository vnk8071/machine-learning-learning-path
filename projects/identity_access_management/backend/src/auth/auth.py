import json
from flask import request, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from ..logger import Logger

AUTH0_DOMAIN = 'dev-t1o1gxv473b4dc8o.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'http://localhost:5000/login'
logger = Logger.get_logger(__name__)
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

    def __str__(self):
        return f'Get {self.error}: {self.status_code}'

    def __repr__(self) -> str:
        return f'AuthError({self.error}, {self.status_code})'


def get_token_auth_header():
    '''
    Obtains the Access Token from the Authorization Header

    Returns:
        str: Token part of the Authorization Header

    Raises:
        AuthError 401: If no header is present
        AuthError 401: If the header is malformed
        AuthError 401: If the Token is not found in the header
        AuthError 401: If the header is not bearer token
    '''
    logger.info('Get token from Authorization header')
    header = request.headers.get('Authorization', None)
    if not header:
        raise AuthError(
            error={
                'code': 'authorization_header_missing',
                'description': 'Authorization header is expected.'
            },
            status_code=401
        )
    logger.info(f'Authorization header: {header}')
    token = header.split()
    if token[0].lower() != 'bearer':
        raise AuthError(
            error={
                'code': 'invalid_header',
                'description': 'Authorization header must start with "Bearer".'
            },
            status_code=401
        )
    elif len(token) == 1:
        raise AuthError(
            error={
                'code': 'invalid_header',
                'description': 'Token not found.'
            },
            status_code=401
        )
    elif len(token) > 2:
        raise AuthError(
            error={
                'code': 'invalid_header',
                'description': 'Authorization header must be bearer token.'
            },
            status_code=401
        )
    return token[1]


def check_permissions(permission, payload):
    '''
    Check if the payload contains the permission

    Args:
        permission (str): Permission (i.e. 'post:drink')
        payload (dict): Decoded JWT payload

    Returns:
        bool: True if the permission is in the payload, otherwise False

    Raises:
        AuthError 400: If the permission is not in the payload
        AuthError 403: If the permission is not found in the payload
    '''
    if 'permissions' not in payload:
        raise AuthError(
            error={
                'code': 'invalid_claims',
                'description': 'Permissions not included in JWT.'
            },
            status_code=400
        )

    if permission not in payload['permissions']:
        raise AuthError(
            error={
                'code': 'unauthorized',
                'description': 'Permission not found.'
            },
            status_code=403
        )
    return True


def verify_decode_jwt(token):
    '''
    Verify and decode the JWT

    Args:
        token (str): JWT token

    Returns:
        dict: Decoded JWT payload

    Raises:
        AuthError 401: If the token is expired
        AuthError 401: If the token is invalid
        AuthError 401: If the token is malformed
        AuthError 400: If the token is not found
        AuthError 400: If the key is not found
    '''
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    unverified_header = jwt.get_unverified_header(token)

    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError(
            error={
                'code': 'invalid_header',
                'description': 'Authorization malformed.'
            },
            status_code=401
        )

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    if rsa_key:
        try:
            payload = jwt.decode(
                token=token,
                key=rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError(
                error={
                    'code': 'token_expired',
                    'description': 'Token expired.'
                },
                status_code=401
            )

        except jwt.JWTClaimsError:
            raise AuthError(
                error={
                    'code': 'invalid_claims',
                    'description': 'Incorrect claims. Please, check the audience and issuer.'},
                status_code=401)
        except Exception:
            raise AuthError(
                error={
                    'code': 'invalid_header',
                    'description': 'Unable to parse authentication token.'
                },
                status_code=400
            )
    raise AuthError(
        error={
            'code': 'invalid_header',
            'description': 'Unable to find the appropriate key.'
        },
        status_code=403
    )


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(wrapped=f)
        def wrapper(*args, **kwargs):
            try:
                token = get_token_auth_header()
                payload = verify_decode_jwt(token=token)
                check_permissions(permission=permission, payload=payload)
            except AuthError as e:
                logger.error(e)
                abort(code=e.status_code)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator
