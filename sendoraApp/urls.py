from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from sendoraApp import views

authUrlPatterns = [
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),
    path('token/blacklist/', jwt_views.TokenBlacklistView.as_view(), name='token_blacklist'),
]

userUrlPatterns = [
    path('user/dashboard/', views.UserDashboardView.as_view()),
    path('google/callback/', views.GoogleLoginCallbackApi.as_view()),
    path('google/url/', views.GoogleLoginApi.as_view()),
]


urlpatterns = authUrlPatterns + userUrlPatterns
