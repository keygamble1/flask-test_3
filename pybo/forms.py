from typing import Text
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
class QuestionForm(FlaskForm):
    subject=StringField('제목',validators=[DataRequired('제목은필수')])
    # html에서 이제부터 input이어ㅑ함
    content=TextAreaField('내용',validators=[DataRequired('내용은필수')])
    # textarea
class AnswerForm(FlaskForm):
    content=TextAreaField('내용',validators=[DataRequired('내용은필수')])
# form에서 validator
class UserCreateForm(FlaskForm):
    username=StringField('사용자이름',validators=[DataRequired(),Length(min=3,max=25)])
    password1=PasswordField('비밀번호', \
        validators=[DataRequired(),EqualTo('password2','비밀번호일치x')])
    password2=PasswordField('비밀번호 확인' , \
        validators=[DataRequired()])
    email=EmailField('이메일' , \
        validators=[DataRequired(),Email()])

class UserLoginForm(FlaskForm):
    username=StringField('사용자이름',validators=[DataRequired(),Length(min=3,max=25)])
    
    password=PasswordField('비밀번호',validators=[DataRequired()])