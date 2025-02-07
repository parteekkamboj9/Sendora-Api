from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, *args, **kwargs):
        token_pair = super().validate(*args, **kwargs)
        token_pair['user'] = {
            'id': self.user.id,
            'email': self.user.email
        }
        return token_pair
