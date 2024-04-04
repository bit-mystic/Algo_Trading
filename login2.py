new_url="https://www.google.com/?s=ok&code=200&auth_code=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkubG9naW4uZnllcnMuaW4iLCJpYXQiOjE3MTA2NjkwNTksImV4cCI6MTcxMDY5OTA1OSwibmJmIjoxNzEwNjY4NDU5LCJhdWQiOiJbXCJ4OjBcIiwgXCJ4OjFcIiwgXCJ4OjJcIiwgXCJkOjFcIiwgXCJkOjJcIiwgXCJ4OjFcIiwgXCJ4OjBcIl0iLCJzdWIiOiJhdXRoX2NvZGUiLCJkaXNwbGF5X25hbWUiOiJYQTA2NTQ0Iiwib21zIjoiSzEiLCJoc21fa2V5IjoiMzk0ZDQ1MGU0ZTQ0ZDQwZDZkNTFmODczOWRkMzRmMmNhOWJkODhmNWNmNDZiN2M2ZmQxZjFiYzUiLCJub25jZSI6IiIsImFwcF9pZCI6Ikw3WU5OWEpBTE0iLCJ1dWlkIjoiNTViMDhiNzMzYmE0NDk0NzkxNWMzYjM1YzJkZjMwYmIiLCJpcEFkZHIiOiIwLjAuMC4wIiwic2NvcGUiOiIifQ.q_R9UnkhE4G-IEAGaDshWYuYF8YRerhGsl0nU10i5T8&state=None"
auth_code = new_url[new_url.index('auth_code=')+10:new_url.index('&state')]

from fyers_apiv3 import fyersModel

client_id="L7YNNXJALM-100"
secret_id="0H6QUDIS1F"
redirect_uri = "https://www.google.com/" 
response_type = "code" 
grant_type = "authorization_code"  

def gen_access_token():
    session = fyersModel.SessionModel(
    client_id=client_id,
    secret_key=secret_id, 
    redirect_uri=redirect_uri, 
    response_type=response_type, 
    grant_type=grant_type
    )

    session.set_token(auth_code)

    response = session.generate_token()

    response_code=response["code"]
    response_message=response["message"]
    access_token = response["access_token"]
    print(response_message)
    return access_token

access_token = gen_access_token()

f = open('acesstoken.txt', 'w')
f.write(access_token)
f.close()



