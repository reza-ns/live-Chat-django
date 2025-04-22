from channels.auth import BaseMiddleware
from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import AccessToken


class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        access_token = self.get_token_from_scope(scope)

        if access_token is not None:
            user_id = await self.get_user_from_token(access_token)
            if user_id:
                scope['user_id'] = user_id
            else:
                scope['error'] = "Invalid token"
        elif access_token is None:
            scope['error'] = "You need token to authenticate"
        return await super().__call__(scope, receive, send)

    def get_token_from_scope(self, scope):
        headers = dict(scope.get('headers', []))
        auth_header = headers.get(b'authorization', b'').decode('utf-8')
        if auth_header.startswith('Bearer'):
            return auth_header.split(' ')[1]
        else:
            return None

    @database_sync_to_async
    def get_user_from_token(self, token):
        try:
            access_token = AccessToken(token)
            return access_token['user_id']
        except:
            return None