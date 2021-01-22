import redis
from flask import Blueprint, render_template, request, make_response, send_from_directory
from sqlalchemy.ext.automap import automap_base
import json
import arrow
import calendar
import datetime
from common.MESLogger import logger,insertSyslog
from flask import render_template,request,Blueprint,redirect,url_for
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from common import MESLogger, autocode
from flask_login import current_user, LoginManager
from common.BSFramwork import AlchemyEncoder
from common.system import Organization, Factory, DepartmentManager, Role
from database import connect_db
from common.Global import db_session, engine, Base
login_manager = LoginManager()

from sqlalchemy import MetaData, desc
from io import BytesIO
metadata = MetaData()
system_set = Blueprint('system_set', __name__, template_folder='templates')

@system_set.route('/system_set/make_model', methods=['POST', 'GET'])
def make_model():
    if request.method == 'POST':
        data = request.values
        try:
            jsonstr = json.dumps(data.to_dict())
            return autocode.make_model_main(data)
        except Exception as e:
            print(e)
            logger.error(e)

def returnb(rod):
    if rod == None or rod == "" or rod == b'':
        return ""
    else:
        return rod.decode()

from sqlalchemy import Table
def getTreeChildrenMap(id, ParentCode, tableName, Name, Code):
    sz = []
    try:
        db_session.commit()
        newTable = Table(tableName, metadata, autoload=True, autoload_with=engine)
        orgs = db_session.query(newTable).filter(newTable.columns._data[ParentCode] == int(id)).all()
        dir = []
        for i in orgs:
            a = 0
            divi = {}
            for j in newTable.columns._data:
                divi[str(j)] = str(i[a])
                a = a + 1
            dir.append(divi)
        for obj in dir:
            if int(obj.get(ParentCode)) == int(id):
                sz.append(
                    {"label": obj.get(Name), "value": obj.get(Code), "children": getTreeChildrenMap(obj.get("ID"), ParentCode, tableName, Name, Code)})
        return sz
    except Exception as e:
        print(e)
        return json.dumps([{"status": "Error：" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)
@system_set.route('/selectTree')
def selectTree():
    '''查询树形结构'''
    data = request.values
    if request.method == 'GET':
        try:
            ParentCode = data.get("ParentCode")#父节点字段名
            tableName = data.get("tableName")#表名
            Name = data.get("Name")#展示的字段名
            Code = data.get("Code")#展示的字段code
            id = 0
            return json.dumps(getTreeChildrenMap(id, ParentCode, tableName, Name, Code), cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            insertSyslog("error", "查询树形结构报错Error：" + str(e), current_user.Name)
            return json.dumps([{"status": "Error：" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)



pool = redis.ConnectionPool(host=connect_db.REDIS_HOST,decode_responses=True)
redis_conn = redis.Redis(connection_pool=pool)
def selectRedisBykey(data):
    '''通过key查询增加修改Redis单个的值'''
    try:
        key = data.get("key")
        value = redis_conn.hget(connect_db.REDIS_TABLENAME, key)
        return json.dumps(value, cls=AlchemyEncoder, ensure_ascii=False)
    except Exception as e:
        print(e)
        insertSyslog("error", "通过key查询Redis单个的值报错Error：" + str(e), current_user.Name)
        return json.dumps([{"status": "Error：" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)

def addUpdateRedisBykey(data):
    '''通过key查询增加修改Redis单个的值'''
    try:
        key = data.get("key")
        value = data.get("value")
        redis_conn.hset(connect_db.REDIS_TABLENAME, key, value)
        return json.dumps("OK", cls=AlchemyEncoder, ensure_ascii=False)
    except Exception as e:
        print(e)
        insertSyslog("error", "增加redis单个值报错Error：" + str(e), current_user.Name)
        return json.dumps([{"status": "Error：" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)

def deleteRedisBykey(data):
    '''通过key查询增加修改Redis单个的值'''
    try:
        key = data.get("key")
        redis_conn.delete(key)
        return json.dumps("OK", cls=AlchemyEncoder, ensure_ascii=False)
    except Exception as e:
        print(e)
        insertSyslog("error", "删除redis单个值报错Error：" + str(e), current_user.Name)
        return json.dumps([{"status": "Error：" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)

import os
dirpath = os.path.join(system_set.root_path,'files')
@system_set.route('/ManualDownload', methods=['get'])
def ManualDownload():
    # fname = request.values.get('FileName', '')
    fname = request.values.get('FileName', '')
    print(fname)
    print(os.path.join(dirpath, fname))
    if os.path.isfile(os.path.join(dirpath, fname)):
        response = make_response(send_from_directory(dirpath, fname, as_attachment=True))
        response.headers["Content-Disposition"] = "attachment; filename={}".format(fname.encode().decode('latin-1'))
        return response
    else:
        json.dumps({"code": "200", "message": "参数错误！"})


