# Lambda Demo - 外部パッケージテスト

このプロジェクトは、CodePipelineのLambdaアクションを使用して外部パッケージを含むLambda関数をデプロイするテストです。

## 構成

```
lambda-demo/
├── src/
│   └── lambda_function.py    # メインのLambda関数
├── requirements.txt          # 外部パッケージ依存関係
├── buildspec.yml            # CodeBuildの設定
├── package/                 # ビルド時に生成（git除外）
└── function.zip             # S3バックアップ用
```

## 外部パッケージテスト

### 使用パッケージ
- `requests==2.31.0` - HTTP APIコール用

### テスト内容
Lambda関数は以下をテストします：
1. **パッケージインポート**: `import requests`が成功するか
2. **バージョン確認**: インストールされたrequestsのバージョン
3. **HTTP API呼び出し**: 外部API（httpbin.org）への接続テスト
4. **エラーハンドリング**: 各種エラーケースの処理

### 期待される結果

#### 成功時のレスポンス
```json
{
  "statusCode": 200,
  "body": {
    "message": "Hello from Lambda with external packages!",
    "external_package_test": "SUCCESS",
    "requests_version": "2.31.0",
    "external_data": { ... },
    "lambda_info": {
      "function_name": "demo-func-1",
      "function_version": "$LATEST",
      "memory_limit": 128
    }
  }
}
```

#### 失敗時のレスポンス
```json
{
  "statusCode": 500,
  "body": {
    "message": "External package import failed",
    "error": "No module named 'requests'",
    "external_package_test": "FAILED - IMPORT ERROR"
  }
}
```

## デプロイフロー

1. **GitHub**: ソースコードをpush
2. **CodeBuild**: 
   - 依存関係をインストール
   - zipファイルを作成してS3にバックアップ
   - ソースコードをアーティファクトとして出力
3. **CodePipeline Lambda Action**:
   - `src/`と`requirements.txt`を受け取り
   - 自動で依存関係を解決
   - Lambda関数を更新

## テスト方法

1. **デプロイ後**: Lambda関数をテスト実行
2. **CloudWatch Logs**: 詳細なログを確認
3. **レスポンス確認**: 外部パッケージが正常に動作しているか確認

## 確認ポイント

- ✅ `import requests`が成功する
- ✅ requestsのバージョンが表示される
- ✅ 外部APIへの接続が成功する
- ✅ Lambda関数の情報が取得できる

これらが全て成功すれば、CodePipelineのLambdaアクションが外部パッケージを正しく処理していることが確認できます。 
