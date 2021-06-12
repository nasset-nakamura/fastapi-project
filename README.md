# FastAPI Test

## Version

- FastAPI 0.65.1
- Python 3.9.5

## Port

- FastAPI 8000

## Link

[FastAPI](http://localhost:8000)

[APIドキュメント(Swagger UI)](http://localhost:8000/docs)

[APIドキュメント(Redoc)](http://localhost:8000/redoc)

## How to Use

### Python実行環境を設定(作成済の場合)

```
# インストールされているバージョンを確認
$ pyenv versions
  system
* 3.9.1 (set by /Users/yoshi0518/.pyenv/version)
  3.9.1/envs/fastapi
  fastapi

# ローカル環境を設定
$ pyenv local fastapi

# バージョンを確認
$ pyenv local
fastapi
```

### Python実行環境を設定(未作成の場合)

```
# インストールされているバージョンを確認
$ pyenv versions
  system
* 3.9.1 (set by /Users/yoshi0518/.pyenv/version)

# 不要なバージョン・環境がある場合は削除
$ pyenv uninstall fastapi

# Pythonをインストール
$ pyenv install 3.9.1

# 作業環境を作成
$ pyenv virtualenv 3.9.1 fastapi

# 作業環境が作成されたことを確認
$ pyenv versions
  system
* 3.9.1 (set by /Users/yoshi0518/.pyenv/version)
  3.9.1/envs/fastapi
  fastapi

# ローカル環境を設定
$ pyenv local fastapi

# バージョンを確認
$ pyenv local
fastapi

$ python --version
Python 3.9.1

$ pip install --upgrade pip
$ pip --version
pip 21.1.1 from /Users/yoshi0518/.pyenv/versions/3.9.1/envs/mkdocs/lib/python3.9/site-packages/pip (python 3.9)

# パッケージをインストール
$ pip install --trusted-host pypi.python.org -r requirements.txt

$ pip freeze -l
aiofiles==0.7.0
alembic==1.6.4
aniso8601==7.0.0
astroid==2.5.6
attrs==21.2.0
autopep8==1.5.7
certifi==2020.12.5
chardet==4.0.0
click==7.1.2
fastapi==0.65.1
flake8==3.9.2
graphene==2.1.8
graphql-core==2.3.2
graphql-relay==2.0.1
greenlet==1.1.0
gunicorn==20.1.0
h11==0.12.0
idna==2.10
iniconfig==1.1.1
isort==5.8.0
lazy-object-proxy==1.6.0
Mako==1.1.4
MarkupSafe==2.0.1
mccabe==0.6.1
orjson==3.5.2
packaging==20.9
pluggy==0.13.1
promise==2.3
py==1.10.0
pycodestyle==2.7.0
pydantic==1.8.2
pyflakes==2.3.1
pylint==2.8.2
pyparsing==2.4.7
pytest==6.2.3
python-dateutil==2.8.1
python-dotenv==0.17.1
python-editor==1.0.4
python-multipart==0.0.5
requests==2.25.1
Rx==1.6.1
six==1.16.0
SQLAlchemy==1.4.12
SQLAlchemy-Utils==0.37.0
starlette==0.14.2
toml==0.10.2
typing-extensions==3.10.0.0
urllib3==1.26.4
uvicorn==0.13.4
wrapt==1.12.1
```

### 作業ブランチ作成〜削除

```
# ブランチを作成・変更
$ git switch -c dev/●●●

# ブランチを確認
$ git branch

# 開発作業・コミット

# プッシュ
$ git push -u origin dev/●●●

# Githubでプルリクエスト

# ブランチを変更
$ git switch main

# 開発作業ブランチを削除
$ git branch -d dev/●●●

# 編集内容をローカルのmainリポジトリへ取得
$ git pull
```

### FastAPI操作

```
# 開発者サーバーを起動
$ uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
