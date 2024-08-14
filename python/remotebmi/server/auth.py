from os import environ

from connexion.exceptions import OAuthProblem


def apikey_auth(token):
    valid_key = environ.get("BMI_API_KEY")
    if  token != valid_key:
        msg = "Invalid token"
        raise OAuthProblem(msg)
    return {"sub": "apikeyuser"}
