import os
BASE_DIR = os.path.dirname(__file__)
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR,'pybo.db'))
# ///는 절대경로를 뜻하며 명확하게함
SQLALCHEMY_TRACK_MODIFICATIONS = "False"
SECRET_KEY="dev"
# SQLALCKEY에 SECRETKEY를 넣어줘야 작동 CSRF