from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)


class MyTokenObtainPairView(TokenObtainPairView):
    pass


class MyTokenRefreshView(TokenRefreshView):
    pass
