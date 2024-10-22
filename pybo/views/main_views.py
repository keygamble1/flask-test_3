from flask import Blueprint, redirect, render_template, url_for

# __name__ 은 직접실행시 main 다른모듈에서 import시 그 파일명이나옴
# __name__은 애플팩토리에서 시랳ㅇ되기때문에 애플팩토리모듈에서는 main_views가되어버림
bp=Blueprint('main',__name__,url_prefix='/')

@bp.route('/')
def index():

    # 필드지정안할시 전체출력
    return redirect(url_for('question._list'))


