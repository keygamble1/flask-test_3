from datetime import datetime
from re import A
from flask import request
from pybo import db
from pybo.models import Question, User

for i in range(300):
    q=Question(subject="테스트데이터[%03d]" % i ,content="내용무",create_date=datetime.now())
    db.session.add(q)
    
db.session.commit()
# 엔터한번더누르고 commit()
# question=q에 대입해야 question_id가 자동생성
question_list=Question.query.order_by(Question.create_date.desc())
page=request.args.get('page',default=1)
question_list=question_list.paginate(page=page,per_page=10)
question_list.has_prev
question_list.iter_pages()
question_list.page

# Question.quey outerjoin시 필드는 추가되지않고 outerjoin의 조건만 가져와서
# Question필드의 id를 기준으로 조회해버리는거
# distinct해서  Question이 중복되면 Answer도 사라지는것
from pybo.models import Question,Answer
Question.query.count()
Answer.query.count()
Question.query.join(Answer).count()
# 조인을안할경우 죄다 None됨
# 이경우 그냥 join쓰면 question과 answer의 교집합
# 즉 answer 답변이있는것만 조회되서 안됨 답변이 없는
# 질문도 포함하고싶을경우 outerjoin으로 question만있는것도 조회해야함
# Question이 들어가고 Answer은 교집합만
Question.query.outerjoin(Answer).count()
# 이럴경우 Question이 중복되니까 안됨
# Question은 한개만하고싶으면 distinct() 
# join안에있는건 교집합일뿐 필드 select에 포함되지않고
# 그전에있는것만 필드에 포함됨
Question.query.outerjoin(Answer).distinct().count()
Question.query.outerjoin(Answer).filter(
    # filter는 기본연산자
    Question.content.ilike('%1%') |
    Answer.content.ilike('%1%')
).distinct().count()
# 답변내용,질문내용은되었으니, 답변작성자도 하고싶음
# 답변작성자는 outerjoin한 Answer과 User모델 다시한번더 조인
# Answer User join해야함
# outerjoin이 아니고 join은 조건 where이라고 보자
# join은 테이블 연결을할뿐 필드를 합친다는 얘기가아님
subquery=db.session.query(Answer,User.username) \
        .join(User,Answer.user_id==User.id).subquery()
Question.query.outerjoin(subquery,subquery.c.question_id==Question.id) \
    .filter(subquery.c.content.ilike('%1%') |
            subquery.c.username.ilike('%1%')).distinct()     
