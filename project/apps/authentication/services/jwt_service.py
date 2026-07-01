from rest_framework_simplejwt.tokens import RefreshToken



        
      


class JWTService:

    @staticmethod
    def generate_tokens(user):

        refresh = RefreshToken.for_user(user)

        return {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
        }

    @staticmethod
    def refresh_tokens(refresh_token):

        refresh = RefreshToken(refresh_token)

        return {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
        }
        
        