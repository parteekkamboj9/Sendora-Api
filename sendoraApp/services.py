# services.py
import os
from django.core.exceptions import ValidationError
from typing import Dict, Any
import requests
from requests import RequestException
from sendoraApp.models import User
import urllib.parse


GOOGLE_ACCESS_TOKEN_OBTAIN_URL = 'https://oauth2.googleapis.com/token'
GOOGLE_AUTH_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
GOOGLE_USER_INFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'
LOGIN_URL = f"{os.getenv('FRONTEND_URL')}login"
GCP_CLIENT_ID = os.environ['GCP_CLIENT_ID']
GCP_REDIRECT_URI = os.environ['GCP_REDIRECT_URI']
SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile'
]


# Exchange authorization token with access token
def google_get_access_token(code: str) -> str:
    # Prepare the payload for the POST request
    data = {
        'code': code,
        'client_id': os.getenv('GCP_CLIENT_ID'),
        'client_secret': os.getenv('GCP_CLIENT_SECRET'),
        'redirect_uri': GCP_REDIRECT_URI,
        'grant_type': 'authorization_code'
    }

    try:
        # Send POST request to get the access token
        response = requests.post(GOOGLE_ACCESS_TOKEN_OBTAIN_URL, data=data)

        # Check if the response is successful
        response.raise_for_status()

        # Parse the access token from the response
        access_token = response.json().get('access_token')

        # If access token is missing in the response, raise an error
        if not access_token:
            raise ValidationError('Access token is missing in the response from Google.')

        return access_token

    except RequestException as e:
        # Handle any kind of HTTP or request-related error
        raise ValidationError(f'Error while requesting access token: {str(e)}')

    except ValueError:
        # Handle JSON parsing error
        raise ValidationError('Invalid JSON response while retrieving access token.')


# Get user info from google
def google_get_user_info(access_token: str) -> Dict[str, Any]:
    response = requests.get(
        GOOGLE_USER_INFO_URL,
        params={'access_token': access_token}
    )

    # Return if any error in request
    if not response.ok:
        raise ValidationError('Could not get user info from Google.')
    return response.json()


def get_user_data(validated_data, request):
    code = validated_data.get('code')
    error = validated_data.get('error')

    # Early return if there is an error or missing code
    if error or not code:
        return {'error': error, 'status': False}

    # Fetch the access token using the code and redirect URI
    access_token = google_get_access_token(code=code)

    # Get user data from Google
    user_data = google_get_user_info(access_token=access_token)

    # Check if the user already exists in the database with the same email
    # existing_user = User.objects.filter(username=user_data['email'], email=user_data['email']).first()
    #
    # if existing_user:
    #     return {'status': False, 'error': 'User exists with another login method.'}

    # Create the user in the database if it's their first time logging in
    user, create = User.objects.get_or_create(
        username=user_data['email'],
        email=user_data['email']
    )

    # Add names is new user created
    if create:
        user.first_name = user_data.get('given_name', ''),
        user.last_name = user_data.get('family_name', ''),

    # Prepare the response profile data
    profile_data = {
        'email': user_data['email'],
        'first_name': user_data.get('given_name', ''),
        'last_name': user_data.get('family_name', ''),
        'status': True
    }

    return profile_data


def get_login_url():
    params = {
        'response_type': 'code',
        'client_id': GCP_CLIENT_ID,
        'redirect_uri': GCP_REDIRECT_URI,
        'prompt': 'select_account',
        'access_type': 'offline',
        'scope': ' '.join(SCOPE)
    }

    # Construct the URL with the query parameters
    url_params = urllib.parse.urlencode(params)
    redirect_url = f'{GOOGLE_AUTH_URL}?{url_params}'

    # You can return the redirect_url
    return redirect_url
