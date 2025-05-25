# src/lambda_function.py

import json

def handler(event, context):
    """
    サンプル: Hello World を返す Lambda ハンドラ
    """
    print("Event:", event)        # ログ出力
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Hello from Lambda!"})
    }
