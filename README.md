# 概要
[このリポジトリ](https://github.com/yukayamaguchi18/mart_portfolio_2025)と同様、D2C事業を行っている企業での実務経験を参考に、同様の業態の企業を想定して、購買データを簡易的に再現し、ダッシュボード向けのデータマートを作成してみたもののdbt版になります。
dbtでのパイプライン作成の練習として取り組みました。
データ定義やデータマートのダッシュボードへの活用案に関しては、上記リポジトリをご確認ください。
# データマート環境（PostgreSQL、dbt）
DockerでPostgeSQL環境を立ててdbtでクエリを実行することで、お手元でデータを確認できます。  
※Dockerは環境再現のために最小限の利用になります
## コンテナ起動
1. コンテナを起動
    ```bash
    docker-compose up -d
    ```

2. コンテナに入る
    ```bash
    docker-compose exec dbt /bin/sh
    ```

3. 手動で seed → run
    ```bash
    dbt seed --profiles-dir .
    dbt run --profiles-dir .
    ```

4. コンテナから出る
    ```bash
    exit
    ```

5. DB に接続して確認
    ```bash
    docker-compose exec db psql -U dbt -d dbt_demo
    ```
