import requests as rq
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

account_sid = ""
auth_token = ""


stock_news_api_key = ""
STOCK_API_KEY = ""
stock_parameter = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

stock_response = rq.get(url=STOCK_ENDPOINT,params=stock_parameter)

data = stock_response.json()
stock_data = data["Time Series (Daily)"]
stock_data_list = [value for (key, value) in stock_data.items()]

yesterday_closing_data = stock_data_list[0]["4. close"]

day_before_yesterday_closing_data = stock_data_list[1]["4. close"]

diff = round(float(day_before_yesterday_closing_data) - float(yesterday_closing_data))
up_down = None
if diff > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

percentage_diff = diff / float(yesterday_closing_data) * 100
if abs(percentage_diff) > 1:
    news_parameter = {
        "apiKey": stock_news_api_key,
        "qInTitle":COMPANY_NAME,
    }
    news_response = rq.get(NEWS_ENDPOINT,params=news_parameter)
    articles = news_response.json()["articles"]
    three_articles = articles[:3]

    formatted_articles = [f"{STOCK_NAME}: {up_down}{percentage_diff}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]

    client = Client(account_sid, auth_token)

    for article in formatted_articles:
        message = client.messages\
                .create(
                    body= article,
                    from_='',
                    to='',
                )