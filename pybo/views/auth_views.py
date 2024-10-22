from datetime import datetime
import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from pybo.forms import AnswerForm, QuestionForm, UserCreateForm, UserLoginForm
from pybo.models import Question, User
from werkzeug.security import *
from pybo import db
# __name__ 은 직접실행시 main 다른모듈에서 import시 그 파일명이나옴
# __name__은 애플팩토리에서 시랳ㅇ되기때문에 애플팩토리모듈에서는 main_views가되어버림
bp=Blueprint('auth',__name__,url_prefix='/auth')
@bp.route('/signup/',methods=('GET','POST'))
def signup():
    form=UserCreateForm()
    if request.method=='POST' and form.validate_on_submit():
        # filter_by=키워드인자 orm연산자 filter=논리연산자
        user=User.query.filter_by(username=form.username.data).first()
        if not user:
            user=User(username=form.username.data, \
            password=generate_password_hash(form.password1.data) ,\
            email=form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자')
    return render_template('auth/signup.html',form=form)

@bp.route('/login',methods=('GET','POST'))
def login():
    # 빈것과 채우는것동시에해야함
    # get,post 둘다
    form=UserLoginForm()
    if request.method=='POST' and form.validate_on_submit():
        error=None
        user=User.query.filter_by(username=form.username.data).first()
        if not user:
            error='존재안함'
        elif not check_password_hash(user.password,form.password.data):
            error='비밀번호일치x'
        if error is None:
            session.clear()
            session['user_id']=user.id
            # 정보남아있는걸 배제하기위해
            # 쿼리스트링추가부터함
            _next=request.args.get('next','')
            # next가없으면 기본 login/이라는뜻
            if _next:
                return redirect(_next)
            else:
            
                return redirect(url_for('main.index'))
        flash(error)
        # 웹->서버요청 
        # 서버는 일단 웹에 쿠키먼저 보내고
        # 웹은 쿠키 저장
        # 이후
    return render_template('auth/login.html',form=form)
def login_required(view):
    @functools.wraps(view)
    def wrapped_views(*args, **kwargs):
        if g.user is None:
            _next=request.url if request.method=='GET' else ''
            return redirect(url_for('auth.login',next=_next))
            # /다음에 next 파라미터 를 전달 login에서는 이제 request.args.get으로 쿼리파라미터 로 쓸수있음
            # redirect로 next를 쿼리스트리으로씀
        return view(*args,**kwargs)
        # view리턴
        # @app.route
        # wrapped views
        # def view:
        # 여러 view에 전달될 인자들을 wrapped의 가변인자를 통해서 쓰임
        # wrapped views에 인자를 넣고 그담에 view에 넣음
    return wrapped_views


@bp.before_app_request
def load_logged_in_user():
    user_id=session.get('user_id')
    if user_id is None:
        g.user=None
    else:
        g.user=User.query.get(user_id)
# 작동안되면 @bp가안되어있어서 블루프린트를 못넘기는것
        # id가있으면 get keyward로 조건을 찾을때는 filter_by로씀
@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))


    


