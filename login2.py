new_url="https://www.google.com/?s=ok&code=200&auth_code=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkubG9naW4uZnllcnMuaW4iLCJpYXQiOjE3MTIyNDYyMDIsImV4cCI6MTcxMjI3NjIwMiwibmJmIjoxNzEyMjQ1NjAyLCJhdWQiOiJbXCJ4OjBcIiwgXCJ4OjFcIiwgXCJ4OjJcIiwgXCJkOjFcIiwgXCJkOjJcIiwgXCJ4OjFcIiwgXCJ4OjBcIl0iLCJzdWIiOiJhdXRoX2NvZGUiLCJkaXNwbGF5X25hbWUiOiJYQTA2NTQ0Iiwib21zIjoiSzEiLCJoc21fa2V5IjoiNjhlOGU2ZjkxY2Q0OTA0YzMyNDNiYzJiYzljYjI4OTQ0OWI2MzVlNzU0MTdiOGVlNTU1ZjVmNGUiLCJub25jZSI6IiIsImFwcF9pZCI6Ikw3WU5OWEpBTE0iLCJ1dWlkIjoiZmY4YTVhNGU5YzdkNGJhYzg2NDg1NWJiNDAwMzIzNTgiLCJpcEFkZHIiOiIwLjAuMC4wIiwic2NvcGUiOiIifQ.BSy5p6lf1_nQAFpqSy9zC1Lw-hQzqRIPemPquycPOZI&state=None"
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



