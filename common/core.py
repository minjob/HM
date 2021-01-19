
#/******************************************************************************************
# ************* STK make model usage:
# ************* version: print python3.6.3  version
# ************* make: make Python file
# ************* STK makemodel.py 1.0.0
# ************* @author Xujin
# ************* @date 2021-01-19 17:06:16
# ************* @Model 
# ******************************************************************************************/

#引入必要的类库
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine, Column,ForeignKey, Table, DateTime, Integer, String
from sqlalchemy import Column, DateTime, Float, Integer, String, Unicode,BigInteger
from sqlalchemy.dialects.mssql.base import BIT
from datetime import datetime
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash

#引入mssql数据库引擎
import pymssql
from common.Global import db_session, engine, Base





#table1_START:
class table1(Base):
	__tablename__ = "table1" 
	
	#ID:
	ID = Column(Integer, primary_key = True, autoincrement = True, nullable = False)
	
	#322:
	aa = Column(Unicode(32), primary_key = False, autoincrement = False, nullable = True)
	
	#342:
	bb = Column(Unicode(32), primary_key = False, autoincrement = False, nullable = True)
	
	#342:
	cc = Column(Unicode(32), primary_key = False, autoincrement = False, nullable = True)
	
#table1_END:

# 生成表单的执行语句_START
Base.metadata.create_all(engine)

# 生成表单的执行语句_END
