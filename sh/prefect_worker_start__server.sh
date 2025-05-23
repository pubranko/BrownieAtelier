#!/bin/bash
###############################################
# local環境でprefect serverを使ったtest用
###############################################
# python仮想環境を有効化
# cd $PWD
. .venv/bin/activate
which python
echo $PWD
echo $PREFECT_HOME
echo $PREFECT_API_URL
echo $PREFECT__WORK_POOL


# prefect APIの接続先を設定
# prefect config set PREFECT_API_URL=$PREFECT_API_URL

# prefectエージェント起動前にappディレクトリへ移動
cd $PWD/app
# prefectのワークプールの環境変数に指定がなければデフォルト値を設定
if [ -z $PREFECT__WORK_POOL ]; then
    export PREFECT__WORK_POOL="default-pool"
fi
# prefectワーカー起動
prefect worker start --pool $PREFECT__WORK_POOL