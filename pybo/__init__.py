from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
import config
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db=SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate=Migrate()

# 순환참조방지
# 전역으로 설정하지않는다
# create_app 애플리케이션 팩토리 쓰면 환경이라든지 중간에 다넣을수있음
# 미리 앱을 생성하는게아닌 동적으로,즉 이것저것 환경을 다집어넣고 앱을 return해서 실행하게할수있음
# 더모듈화하고 블루푸린트도 사용가능
# 그런데 url매핑이 필요할때마다 계속 create_app을 해야하는 불편함, 라우팅함수추가되어야하는 복잡한함수가 되므로

# @bp 블루프린트르 실행시켜라
def create_app():
    app=Flask(__name__)
    app.config.from_object(config)
    
    # SQLALCHEMY_DATABASE_URI 이 app[SQLALCHEMY_DATABASE_URI] 을 대체함
    # 인스턴스가 나중에 만들어지게하기위해 즉시 초기화가아닌 나중 LAZY초기화로함 LAZY INITALIZATION 
    # 지연초기화
    
    #orm
    db.init_app(app)
    # start s with
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app,db,render_as_batch=True)
    else:
    # 지연방식 init_app
        migrate.init_app(app,db)
    from . import models
    # 모델안하면 migrate가안될듯?
    # 다하고 app을실행하라 db migrate 및 upgrade된고나서 app실행
    from .views import main_views,question_views,answer_views,auth_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)
    from .filter import format_time
    app.jinja_env.filters['datetime']=format_time
    # datetime에 넣어서 html에서 쓸수있음
    return app
