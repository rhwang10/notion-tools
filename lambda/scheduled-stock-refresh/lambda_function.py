import os
import requests
import json

import yfinance

NOTION_TOKEN = os.environ.get("NOTION_API_TOKEN")
INVESTMENTS_DATABASE_ID = os.environ.get("INVESTMENTS_DATABASE_ID")

PAGES_API_BASE = "https://api.notion.com/v1/pages/"
DATABASE_API_BASE = "https://api.notion.com/v1/databases/"

def lambda_handler(event, context):

    headers = {
        'Authorization': 'Bearer ' + NOTION_TOKEN,
        'Notion-Version': '2021-05-13',
        'Content-Type': 'application/json'
    }

    data = {
        'filter': {
            'property': 'Ticker',
            'text': {
                'is_not_empty': True
            }
        }
    }

    r = requests.post(DATABASE_API_BASE + INVESTMENTS_DATABASE_ID + '/query',
    headers=headers, data=json.dumps(data))

    for result in json.loads(r.text)['results']:
        ticker = result['properties']['Ticker']['rich_text'][0]['plain_text']
        id = result['id']

        stock_data = yfinance.Ticker(ticker)
        history = stock_data.history()
        last_quote = round((history.tail(1)['Close'].iloc[0]), 2)

        ticker_data = {
            'properties': {
                'Price': {
                    'number': last_quote
                }
            }
        }

        p = requests.patch(PAGES_API_BASE + id, headers=headers, data=json.dumps(ticker_data))

    return {
        'statusCode': 200
    }


# for debugging purposes
if __name__ == "__main__":
    lambda_handler({}, {})
