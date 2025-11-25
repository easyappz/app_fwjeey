from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import AuthToken


class TokenAuthentication(BaseAuthentication):
    """Custom token authentication"""
    
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return None
        
        try:
            # Expected format: "Token <token>"
            parts = auth_header.split()
            if len(parts) != 2 or parts[0].lower() != 'token':
                raise AuthenticationFailed('Invalid token header format')
            
            token_key = parts[1]
            token = AuthToken.objects.select_related('member').get(key=token_key)
            return (token.member, token)
        except AuthToken.DoesNotExist:
            raise AuthenticationFailed('Invalid token')
        except Exception:
            raise AuthenticationFailed('Invalid token header')
