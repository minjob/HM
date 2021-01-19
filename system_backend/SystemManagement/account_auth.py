import json
from flask import Blueprint, render_template, request, redirect, session, url_for, flash, make_response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_login import login_required, logout_user, login_user, current_user, LoginManager
from sqlalchemy.exc import InvalidRequestError
from PIL import Image, ImageFont, ImageDraw, ImageFilter
import random
from io import BytesIO
import time
import datetime
from common.system import User
from common.MESLogger import logger
from common.BSFramwork import AlchemyEncoder
from common.Global import db_session, engine, Base
# flask_login的初始化
login_manager = LoginManager()
login_manager.db_session_protection = 'strong'
login_manager.login_view = 'login_auth.login'

login_auth = Blueprint('login_auth', __name__, template_folder='templates')


@login_auth.route('/account/userloginauthentication', methods=['GET', 'POST'])
def userloginauthentication():
    '''
    用户登陆认证
    :return:
    '''
    try:
        if request.method == 'POST':
            data = request.values
            WorkNumber = data.get('WorkNumber')
            password = data.get('password')
            # 验证账户与密码
            user = db_session.query(User).filter_by(WorkNumber=WorkNumber).first()
            resp = make_response()
            if user and (user.confirm_password(password) or user.Password == password):
                login_user(user)  # login_user(user)调用user_loader()把用户设置到db_session中
                user.session_id = str(time.time())
                user.LastLoginTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                db_session.commit()
                return {"code": "200", "message": "OK"}
            else:
                return {"code": "300", "message": "用户名密码错误"}
    except Exception as e:
        print(e)
        db_session.rollback()
        logger.error(e)
        return json.dumps([{"status": "Error:" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)
