"""Expose client to use quickbooks charge client with retry
"""
import uuid
from charge_client import add_charge, TokenExpiredException
from refresh_tokens import get_refreshed_tokens


class TooManyAttemptsToAuthorize(Exception):
    pass


class QuickbooksChargeClient():
    """QuickbooksChargeClient exposes method to add a charge
    with retry in case the access token expires.
    It also able to indicates if the tokens were updated
    check tokens_updated property
    """
    access_token = ''
    refresh_token = ''
    client_id = ''
    client_secret = ''
    tokens_updated = False
    sandbox = True

    def __init__(self,
                 access_token,
                 refresh_token,
                 client_id,
                 client_secret,
                 sandbox=True):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.client_id = client_id
        self.client_secret = client_secret
        self.sandbox = sandbox

    def charge_card(self, amount, card, postal_code, address):
        """Try to add a charge and retry if the token has expired
            it internally call update_tokens if needed
        Arguments:
            amount {number} -- [description]
            card {Card} -- [description]
            postal_code {string} -- [description]
            address {string} -- [description]

        Raises:
            TooManyAttemptsToAuthorize: When unable to authorize with
            the given settings

        Returns:
            [charge_object] -- [https://developer.intuit.com/app/developer/qbpayments/docs/api/resources/all-entities/charges]
        """
        request_id = str(uuid.uuid4())
        safety_check = 1
        while safety_check <= 3:
            try:
                charge_data = add_charge(self.access_token,
                                         request_id,
                                         amount,
                                         card,
                                         postal_code,
                                         address,
                                         sandbox=self.sandbox)
                # We got all the way here we are ok
                return charge_data
            except TokenExpiredException:
                safety_check = safety_check + 1
                self.update_tokens()

        raise TooManyAttemptsToAuthorize('Unable to get a valid access token')

    def update_tokens(self):
        tokens_response = get_refreshed_tokens(self.refresh_token,
                                               self.client_id,
                                               self.client_secret,
                                               sandbox=self.sandbox)
        self.access_token = tokens_response.access_token
        self.refresh_token = tokens_response.refresh_token
        self.tokens_updated = True
