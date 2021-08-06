import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

news_parameters = {
    'q': COMPANY_NAME,
    'apiKey': "___your_key____",
}
stock_parameters = {
    'function': "TIME_SERIES_DAILY",
    'symbol': STOCK_NAME,
    'interval': "5min",
    'apikey': "__your__key__"
}

response_stock = requests.get(STOCK_ENDPOINT, params=stock_parameters)
file = response_stock.json()
data = file["Time Series (Daily)"]
closing_stock = [value for (key, value) in data.items()]
yesterday_closing = closing_stock[0]["4. close"]
before_yesterday_close = closing_stock[1]["4. close"]
difference = float(yesterday_closing) - float(before_yesterday_close)
up_down = None
if difference > 0:
    up_down = "⬆"
else:
    up_down = "⬇"

percentage = round((difference / float(yesterday_closing)) * 100)
if abs(percentage) > 5:
    news_response = requests.get(NEWS_ENDPOINT, params=news_parameters)
    news_response.raise_for_status()
    news_data = news_response.json()["articles"][:3]

    news = [f"\n{STOCK_NAME}: {up_down}{percentage}%\nHeadline: {h['title']} \n\nBrief: {h['description']}\n" for h in news_data]

    account_sid = "AC6c0da82ec61ec7285319b95547028e5b"
    auth_token = "68a3035ae33b5b6df0add6650e5ccdbf"
    client = Client(account_sid, auth_token)
    for h in news:
        message = client.messages \
            .create(
            body=h,
            from_='+15712902611',
            to=''
        )
        print(message.status)

