from rest_framework import status as status_codes, permissions
from rest_framework.response import Response
from rest_framework.views import APIView


class UserDashboardView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, *args, **kwargs):
        return Response({}, status=status_codes.HTTP_201_CREATED)
