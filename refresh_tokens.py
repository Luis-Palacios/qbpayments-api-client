"""refresh_tokens modules hold the refresh token wrapper around
auth client from inituit
"""
from intuitlib.client import AuthClient


class RefreshTokenResponse():
    """Class thar represent the return type from the refresh token auth client
    """
    refresh_token = ''
    refresh_token_expires_in = 0
    access_token = ''
    expires_in = 0

    def __init__(self, refresh_token, refresh_token_expires_in, access_token,
                 expires_in):
        self.refresh_token = refresh_token
        self.refresh_token_expires_in = refresh_token_expires_in
        self.access_token = access_token
        self.expires_in = expires_in


def get_refreshed_tokens(refresh_token,
                         client_id,
                         client_secret,
                         sandbox=False):
    enviroment = 'sandbox' if sandbox else 'production'
    auth_client = AuthClient(client_id, client_secret, '', enviroment)
    auth_client.refresh(refresh_token=refresh_token)
    return RefreshTokenResponse(
        auth_client.refresh_token,
        auth_client.x_refresh_token_expires_in,
        auth_client.access_token,
        auth_client.expires_in,
    )
