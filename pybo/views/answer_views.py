from ast import And
from datetime import datetime

from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from pybo.forms import AnswerForm
from pybo.models import Answer, Question
from pybo import db
from pybo.views.auth_views import login_required
# __name__ 은 직접실행시 main 다른모듈에서 import시 그 파일명이나옴
# __name__은 애플팩토리에서 시랳ㅇ되기때문에 애플팩토리모듈에서는 main_views가되어버림
bp=Blueprint('answer',__name__,url_prefix='/answer')
@bp.route('/create/<int:question_id>',methods=('POST',))
# form이 post일때만 사용
@login_required
def create(question_id):
    form=AnswerForm()
    question=Question.query.get_or_404(question_id)
    if form.validate_on_submit():
        answer=Answer(question=question,content=form.content.data,create_date=datetime.now(),user=g.user)
        db.session.add(answer)
        db.session.commit()
    
    # question.answer_set.append(answer) 해도되긴함
    # answer_{{answer_id}}
    # '{}#answer_{}'.format(
    # ,answer.id)
    
        return redirect('{}#answer_{}'.format(
            url_for('question.detail',question_id=question_id),answer.id))
    # 오류발생시 아래 리턴
    return render_template('question/question_detail.html',form=form,question=question)
@bp.route('/delete/<int:answer_id>')
@login_required
def delete(answer_id):
    answer=Answer.query.get_or_404(answer_id)
    question_id=answer.question.id
    # 이렇게안하면 answer가 지워진상태로되어서 변수할당해줘야함
    if g.user != answer.user:
        flash('삭제권한x')
    else:
        db.session.delete(answer)
        db.session.commit()
    return redirect(url_for('question.detail',question_id=question_id))
@bp.route('/modify/<int:answer_id>',methods=('GET','POST'))
# 이게 methods임
def modify(answer_id):
    answer=Answer.query.get_or_404(answer_id)
    
    form=AnswerForm()
    # question_id 검색하기
    if answer.user !=g.user:
        flash('수정권한x')
        return redirect(url_for('question.detail',question_id=answer.question.id))
    if request.method=='POST' and form.validate_on_submit():
        form.populate_obj(answer)
        answer.modify_date=datetime.now()
        db.session.commit()
        # 모델객체 ㅜ가삭제할때 add delete씀
        
    # '{}#answer_{}'.format(
    # ,answer.id)
        return redirect('{}#answer_{}'.format(
            url_for('question.detail',question_id=answer.question.id),answer.id))
    else:
        form=AnswerForm(obj=answer)
    return render_template('answer/answer_form.html',form=form)
@bp.route('/vote/<int:answer_id>')
@login_required
def vote(answer_id):
    answer=Answer.query.get_or_404(answer_id)
    if g.user == answer.user:
        flash('본인건 추천x')
    else:
        answer.voter.append(g.user)
        db.session.commit()
          # '{}#answer_{}'.format(
    # ,answer.id)
    return redirect('{}#answer_{}'.format(
        url_for('question.detail',question_id=answer.question.id),answer.id))