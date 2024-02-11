
from fyers_apiv3 import fyersModel
import webbrowser

client_id="L7YNNXJALM-100"
secret_key="0H6QUDIS1F"
redirect_url="https://www.google.com/"
response_type = "code"  
state = "sample_state"

def get_auth_code():
    session = fyersModel.SessionModel(
        client_id=client_id,
        secret_key=secret_key,
        redirect_uri=redirect_url,
        response_type=response_type
    )
    response = session.generate_authcode()

    webbrowser.open(response)

get_auth_code()