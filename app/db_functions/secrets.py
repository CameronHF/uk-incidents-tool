import datetime as dt
import json

import boto3
import hvac


def get_vault_token(session=None, region_name="ca-central-1"):
    secret_name = "s.ckTZeN0e1yuPM2muj6QDm4EL"

    if session is None:
        session = boto3.session.Session()

    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )

    if 'SecretString' in get_secret_value_response:
        token = json.loads(get_secret_value_response['SecretString'])
        return token
    else:
        raise KeyError("Token Not Found")


def get_secrets(vault_token, vault_path):
    client = hvac.Client('https://vault.hellofresh.io', token=vault_token)

    secrets = client.read(vault_path)['data']
    return secrets


get_vault_token()