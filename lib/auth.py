import dbm
import os
import hashlib
import time
import json
import base64
from functools import wraps
from .bottle import request
from .utils import abort

dbpath = os.path.join(os.getcwd(), 'db/manage')


'''
  说明以下
  用户key: username md5
  用户value: username, password, root_path, isadmin, uptiem, crated_at => josn.dumps(values)
  token key: username + password + root_path => (md5) -> (base64)
  token value: 用户key
'''

def getDb():
  db = dbm.open(dbpath, 'c')
  return db

def Login(username, password):
  if username != None and password != None:
    db = getDb()
    usermd5 = hashlib.md5(username.encode(encoding='UTF-8')).hexdigest()
    if usermd5 in db:
      value = json.loads(db[usermd5])
      password = hashlib.md5(password.encode(encoding='UTF-8')).hexdigest()
      if password != value['password']:
        db.close()
        return {
          'status': 1,
          'message': '密码错误'
        }
      else:
        token = value['username'] + value['password'] + value['root_path']
        token = hashlib.md5(token.encode(encoding='UTF-8')).hexdigest()
        db[token] = usermd5 #需要再次base64加密
        db.close()
        return {
          'status': 0,
          'message': '登陆成功',
          'token': str(base64.b64encode(token.encode("utf-8")), encoding = "utf8")
        }
    db.close()
    return {
      'status': 1,
      'message': '用户不存在'
    }
  return {
    'status': 1,
    'message': '用户名或密码不能为空'
  }

def checkLogin(token):
  db = getDb()
  token = str(token.replace('Bearer ', '', 1).encode("utf8"), encoding = "utf8")
  token = base64.b64decode(token).decode("utf-8")
  if token in db:
    '''
    user = db[token]
    user = json.loads(db[user])
    del user['password']
    db.close()
    return {
      'status': 0,
      'message': '已登陆',
      'user': user
    }
    '''
    db.close()
    return True
  else:
    db.close()
    return False

def login_required(func):
  @wraps(func)
  def decorated_view(*args, **kwargs):
    token = request.headers.get('Authorization')
    if token:
      if checkLogin(token):
        return func(*args, **kwargs)
      else:
        return abort(403)
    return abort(403)
  return decorated_view

def Logout():
  return True

def addAdmin(params):
  db = getDb()
  now = int(time.time())
  params = json.loads(params)
  user_key = hashlib.md5(params['username'].encode(encoding='UTF-8')).hexdigest()
  params['password'] = hashlib.md5(params['password'].encode(encoding='UTF-8')).hexdigest()
  params['crated_at'] = now
  params['uptiem'] = now
  db[user_key] = json.dumps(params)
  db.close()
  return {
    'status': 0,
    'message': '添加成功'
  }


# if __name__ == '__main__':
  # print(Login('admin','kanghong123'))
  # params = json.dumps({
  #   'username': 'admin',
  #   'password': 'kanghong123',
  #   'isadmin': True,
  #   'root_path': '/'
  # })
  # print(addAdmin(params))
  # print(checkLogin('Y2M0NDVlMTcwYTRiNTRkNWQwMDhiNTRiOGJlN2UzZTE='))
