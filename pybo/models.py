
from pybo import db
# import sqlalchemy as db

question_voter=db.Table(
    'question_voter',
    db.Column('user_id',db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'),primary_key=True),
    db.Column('question_id',db.Integer,db.ForeignKey('question.id',ondelete='CASCADE'),primary_key=True)
)
answer_voter=db.Table(
    'answer_voter',
    db.Column('user_id',db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'),primary_key=True),
    db.Column('answer_id',db.Integer,db.ForeignKey('answer.id',ondelete='CASCADE'),primary_key=True)
)
class Question(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    subject=db.Column(db.String(200),nullable=False)
    content=db.Column(db.Text(),nullable=False)
    create_date=db.Column(db.DateTime(),nullable=False)
    user=db.relationship('User',backref=db.backref('question_set'))
    # user1 question_set 다 1:다 이렇게 하자 가로로
    user_id=db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'),nullable=False)
    modify_date=db.Column(db.DateTime(),nullable=True)
    voter=db.relationship('User',secondary=question_voter,backref=db.backref('question_voter_set'))
    # 업그레이드 실패시  migrate 변경점이남아있기때문에 변경점을 바꿔버린다
    # 그러므로 새롭게 migrate해도 변경점이 사라지지않고 이미있따는식으로 되어버림
    # heads가 진짜고 current는 저장된후 임시 migrate이기때문에 없애야함
class Answer(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    question_id=db.Column(db.ForeignKey('question.id',ondelete='CASCADE'))
    question=db.relationship('Question',backref=db.backref('answer_set'))
    # question=ansewr_set question.answer_set 바ㅗ 이어지게 외우기
    # question->answer로 backref한다 answer_set으로
    # TODO:ㄴㄴ
    content=db.Column(db.Text(),nullable=False)
    create_date=db.Column(db.DateTime(),nullable=False)
    user=db.relationship('User',backref=db.backref('answer_set'))
    # user1 question_set 다 1:다 이렇게 하자 가로로
    user_id=db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'),nullable=False)
    modify_date=db.Column(db.DateTime(),nullable=True)
    voter=db.relationship('User',secondary=answer_voter,backref=db.backref('answer_voter_set'))
class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(150),nullable=False,unique=True)
    password=db.Column(db.String(200),nullable=False)
    email=db.Column(db.String(20),nullable=False,unique=True)

