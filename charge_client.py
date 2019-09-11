import requests

PRODUCTION_URL = 'https://api.intuit.com'
SANDOBOX_URL = 'https://sandbox.api.intuit.com'

CHARGE_URL = '/quickbooks/v4/payments/charges'


class Card(object):
    name = ''
    number = ''
    exp_month = '01'
    exp_year = '2020'
    cvc = '123'

    def __init__(self, name, number, exp_month, exp_year, cvc):
        self.name = name
        self.number = number
        self.exp_month = exp_month
        self.exp_year = exp_year
        self.cvc = cvc


def add_charge(access_token,
               request_id,
               amount,
               card,
               postal_code,
               address,
               sandbox=False,):

    headers = {
        'authorization': 'Bearer {}'.format(access_token),
        'accept': 'application/json',
        'content-type': 'application/json',
        'request-id': request_id
    }
    body = {
        'currency': 'USD',
        'amount': amount,
        'context': {
            'mobile': 'false',
            'isEcommerce': 'true'
        },
        'card': {
            'name': card.name,
            'number': card.number,
            'expMonth': card.exp_month,
            'address': {
                'postalCode': postal_code,
                'streetAddress': address,
            },
            'expYear': card.exp_year,
            'cvc': card.cvc
        }
    }
    base_url = SANDOBOX_URL if sandbox else PRODUCTION_URL
    url = '{}{}'.format(base_url, CHARGE_URL)
    response = requests.post(url, headers=headers, json=body)

    response.raise_for_status()
    return response.json()