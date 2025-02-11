# services.py
import os
from django.core.exceptions import ValidationError
from typing import Dict, Any
import requests
from sendoraApp.models import User

GOOGLE_ACCESS_TOKEN_OBTAIN_URL = 'https://oauth2.googleapis.com/token'
GOOGLE_USER_INFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'
LOGIN_URL = f"{os.getenv('FRONTEND_URL')}login"


# Exchange authorization token with access token
def google_get_access_token(code: str, redirect_uri: str) -> str:
    data = {
        'code': code,
        'client_id': os.getenv('GCP_CLIENT_ID'),
        'client_secret': os.getenv('GCP_CLIENT_SECRET'),
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }

    response = requests.post(GOOGLE_ACCESS_TOKEN_OBTAIN_URL, data=data)

    if not response.ok:
        raise ValidationError('Could not get access token from Google.')

    access_token = response.json()['access_token']

    return access_token


# Get user info from google
def google_get_user_info(access_token: str) -> Dict[str, Any]:
    response = requests.get(
        GOOGLE_USER_INFO_URL,
        params={'access_token': access_token}
    )

    if not response.ok:
        raise ValidationError('Could not get user info from Google.')

    return response.json()


def get_user_data(validated_data, request):
    domain = request.build_absolute_uri('/')
    redirect_uri = f'{domain}api/google/login/callback/'

    code = validated_data.get('code')
    error = validated_data.get('error')

    if error or not code:
        return {'error': error, 'status': False}

    access_token = google_get_access_token(code=code, redirect_uri=redirect_uri)
    user_data = google_get_user_info(access_token=access_token)

    existing_user = User.objects.filter(
            username=user_data['email'],
            email=user_data['email'],
            by_google=False
    ).first()
    if existing_user:
        return {'status': False, 'error': 'User exist with another login method.'}

    # Creates user in DB if first time login
    User.objects.get_or_create(
        username=user_data['email'],
        email=user_data['email'],
        first_name=user_data.get('given_name', ''),
        last_name=user_data.get('family_name', ''),
        by_google=True
    )

    profile_data = {
        'email': user_data['email'],
        'first_name': user_data.get('given_name', ''),
        'last_name': user_data.get('family_name', ''),
        'status': True
    }
    return profile_data
