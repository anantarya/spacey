# views.py

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class ObtainTokenPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer  # Use the default serializer

obtain_token_pair_view = ObtainTokenPairView.as_view()
