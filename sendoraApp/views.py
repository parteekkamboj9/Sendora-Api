import os
from django.shortcuts import redirect
from rest_framework import status as status_codes, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from sendoraApp import models
from sendoraApp import serializers
from sendoraApp.services import get_user_data

FRONTEND_URL = os.environ['FRONTEND_URL']


class UserDashboardView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, *args, **kwargs):
        return Response({}, status=status_codes.HTTP_201_CREATED)


class GoogleLoginApi(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        auth_serializer = serializers.GoogleAuthSerializer(data=request.GET)
        serializer = auth_serializer.is_valid()
        if not serializer:
            return redirect(FRONTEND_URL + "google-callback?error='Invalid Data Received from Google.'")

        validated_data = auth_serializer.validated_data

        user_data = get_user_data(validated_data, request)
        if not user_data.get('status'):
            return redirect(f'{FRONTEND_URL}google-callback?error={user_data.get("error")}')

        user = models.User.objects.get(email=user_data['email'])

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return redirect(
            f'{FRONTEND_URL}google-callback?token={access_token}&refresh={refresh}&email={user.email}&userId={user.id}')
