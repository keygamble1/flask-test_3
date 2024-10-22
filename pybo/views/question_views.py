from datetime import datetime
from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from pybo.forms import AnswerForm, QuestionForm
from pybo.models import Question,Answer,User
from pybo import db
from pybo.views.auth_views import login_required
from sqlalchemy import distinct
# __name__ 은 직접실행시 main 다른모듈에서 import시 그 파일명이나옴
# __name__은 애플팩토리에서 시랳ㅇ되기때문에 애플팩토리모듈에서는 main_views가되어버림
bp=Blueprint('question',__name__,url_prefix='/question')

@bp.route('/list/')
def _list():
    page=request.args.get('page',type=int,default=1)
    kw=request.args.get('kw',type=int,default='')
    
    # requgts.args.get 은 ?key=value값으로 딕셔너리형태ㅗㄹ접근
    # page(key)=1(value)
    # ?page=1을 기본으로 가져올것 없으면 1이다
    question_list=Question.query.order_by(Question.create_date.desc())
    if kw:
        search='%%{}%%'.format(kw)
        sub_query=db.session.query(Answer.question_id,Answer.content,User.username) \
            .join(User,Answer.user_id==User.id).subquery()
        # c는 서브쿼리 필드
        question_list=question_list \
            .join(User) \
            .outerjoin(sub_query,sub_query.c.question_id==Question.id) \
            .filter(Question.subject.ilike(search) |
            Question.content.ilike(search) |
            User.username.ilike(search) |
            sub_query.c.content.ilike(search) |
            sub_query.c.username.ilike(search)).distinct()
            
    # sub_query는 Question에 종속된 Answer만꺼냄
    # question_list는 Question User가있는것만꺼냈는데,
    # outerjoin으로 QuestionUser가 답변을 직접안달아도 나오게함
    # 즉 Answer.id에 None이어도 그외의 Answer의 User등 query필드가 다 나오게됨
    
    question_list=question_list.paginate(page=page,per_page=10)
    # paginate.items 는 속성 itmes()는 메서드인데 여기선 메서드를안씀
    # form.errors 은 메서드가 있어서 .itmes()를 실행후 쓰는듯?
    # 필드지정안할시 전체출력
    return render_template('question/question_list.html',question_list=question_list)

@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    # 이제 detail에는 AnswerForm이라는 Form과 answer.content등 다있기때문에
    # render에서 AnswerForm을 넣어줘야함그래야 유효성검사일치함
    # answer_create랑 연결되어있기때문임
    # answer.create에서 post인경우만 지금 넣어놨기때문에
    # get인경우를 쓰지않았음
    # 처음부터 ansewrForm이 틀릴순없기때문에 기본값초기화
    form=AnswerForm()
    question=Question.query.get_or_404(question_id)
    # form.errors에서 에러가 나오도록만듬// 유효성검사에서 get일경우가없기때문에 아예에러
    
    return render_template('question/question_detail.html',question=question,form=form)

@bp.route('/create/',methods=('GET','POST'))
@login_required
def create():
    form=QuestionForm()
    # form이있으면 간단하게 쓸수있으나 없으면 임시로 form.request['content]이렇게씀
    if request.method=='POST' and form.validate_on_submit():
        question=Question(subject=form.subject.data,content=form.content.data,create_date=datetime.now(),user=g.user)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html',form=form)

@bp.route('/modify/<int:question_id>',methods=('GET','POST'))
@login_required
def modify(question_id):
    question=Question.query.get_or_404(question_id)
    form=QuestionForm()
    if question.user !=g.user:
        flash('수정권한x')
        return redirect(url_for('question.detail',question_id=question_id))
    if request.method=='POST' and form.validate_on_submit():
        form.populate_obj(question)
        question.modify_date=datetime.now()
        db.session.commit()
        # 모델객체 ㅜ가삭제할때 add delete씀
        return redirect(url_for('question.detail',question_id=question_id))
    else:
        form=QuestionForm(obj=question)
    return render_template('question/question_form.html',form=form)
        
    
@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
    question=Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('삭제권한x')
        return redirect(url_for('question.detail',question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('main.index'))
@bp.route('/vote/<int:question_id>')
@login_required
def vote(question_id):
    _question=Question.query.get_or_404(question_id)
    if g.user == _question.user:
        flash('본인건 추천x')
    else:
        _question.voter.append(g.user)
        db.session.commit()
    return redirect(url_for('question.detail',question_id=question_id))
    # form = QuestionForm(obj=question)이건 get할때 채워지게하는것 
    # form.populate_obj(question) 이건 업데이트하게하는것
