from django.utils.deprecation import MiddlewareMixin
import jwt
from django.conf import settings
from django.utils import timezone

from app.models import Author
def encode_jwt(payload):
    """Encode payload into a JWT token."""
    # jwt.encode automatically handles header creation and base64url encoding
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')  # No need to manually pass headers

def decode_jwt(token):
    """Decode JWT token and return payload."""
    try:
        # Decode the token and verify its signature
        return jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    except jwt.InvalidTokenError:
        return None  # Invalid token


#
def getCurrentUser(request):
    token = request.COOKIES.get('jwt')

    print(token)
    if token:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            return payload.get('user_id'), None # return user object

        except jwt.ExpiredSignatureError:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'], options={"verify_exp": False})

            new_token = encode_jwt({'user_id': payload.get('user_id')})
            return payload.get('user_id'), new_token # return user object and new token

        except jwt.InvalidTokenError:
            print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
            return None, None # user isn't authorised
    return None, None

def revalidateToken(request, response):
    token = getCurrentUser(request)[1] # only get token
    if token is not None:
        response.set_cookie('jwt', token, httponly=True, secure=True)



def CanEdit(request, author_id):
    # decode the token
    user_id, token = getCurrentUser(request) # token will be passed down in case it expired

    # logic to check if user is allowed to edit (if they are editing their own profile)
    return int(author_id) == user_id, token

