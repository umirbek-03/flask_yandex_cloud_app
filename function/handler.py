# function/handler.py
import os
import json

def handler(event, context):
    # event['body'] содержит тело запроса (строка)
    try:
        body = event.get('body')
        if isinstance(body, str):
            data = json.loads(body)
        else:
            data = body or {}
    except Exception:
        data = {}
    return {
        'statusCode': 200,
        'body': json.dumps({'ok': True, 'received': data})
    }