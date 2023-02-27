import jwt
import requests
from django.contrib.auth.models import User
from django.conf import settings



def authenticate_user(request):
    access_token = request.headers.get('Authorization')
    if not access_token:
        return None

    # Make a request to the users microservice to validate the access token
    url = 'http://127.0.0.1:8001/api/auth/signin'
    headers = {'Authorization': access_token}
    response = requests.post(url, headers=headers)

    # Debugging statements)

    token = access_token.split()[1]
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = payload['user_id']
        user = User.objects.get(id=user_id)
        return user_id
    except jwt.exceptions.DecodeError:
        return None
    except User.DoesNotExist:
        return None