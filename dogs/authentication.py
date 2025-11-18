from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.conf import settings
from supabase import create_client
import os

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return None
            
        try:
            token = auth_header.split(' ')[1]  # Bearer <token>
            # Aquí implementarías la validación del token JWT
            # Por simplicidad, asumimos que el token es válido
            return (None, None)  # User object y token
        except IndexError:
            raise AuthenticationFailed('Token prefix missing')
        except Exception:
            raise AuthenticationFailed('Invalid token')