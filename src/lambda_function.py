import json
import requests  # 外部パッケージをテスト

def handler(event, context):
    """
    外部パッケージを使用するテスト Lambda ハンドラ
    """
    print("=== Lambda Function Started ===")
    print("Event:", event)
    
    try:
        # requestsライブラリのバージョン確認
        print(f"Requests version: {requests.__version__}")
        
        # 外部APIを呼び出してテスト
        print("Testing external package: requests")
        response = requests.get('https://httpbin.org/json', timeout=10)
        external_data = response.json()
        
        print("External API call successful")
        print(f"Response status: {response.status_code}")
        
        result = {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Hello from Lambda with external packages!",
                "external_package_test": "SUCCESS",
                "requests_version": requests.__version__,
                "external_data": external_data,
                "lambda_info": {
                    "function_name": context.function_name,
                    "function_version": context.function_version,
                    "memory_limit": context.memory_limit_in_mb
                }
            })
        }
        
        print("=== Lambda Function Completed Successfully ===")
        return result
        
    except ImportError as e:
        error_msg = f"Import error: {e}"
        print(error_msg)
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "External package import failed",
                "error": str(e),
                "external_package_test": "FAILED - IMPORT ERROR"
            })
        }
    except requests.exceptions.RequestException as e:
        error_msg = f"HTTP request error: {e}"
        print(error_msg)
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "External API call failed",
                "error": str(e),
                "external_package_test": "FAILED - HTTP ERROR"
            })
        }
    except Exception as e:
        error_msg = f"Unexpected error: {e}"
        print(error_msg)
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Unexpected error occurred",
                "error": str(e),
                "external_package_test": "FAILED - RUNTIME ERROR"
            })
        } 
