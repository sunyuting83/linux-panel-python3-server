import dbm
import os
import time
import json
from functools import wraps
from .bottle import request
from .utils import abort, enToken, deToken, makeMd5

'''
  说明以下
  用户key: username md5
  用户value: username, password, root_path, isadmin, uptiem, crated_at => josn.dumps(values)
  token key: username + password + root_path => (md5) -> (base64)
  token value: 用户key
'''

def getDb():
  dbpath = os.path.join(os.getcwd(), 'db/manage')
  db = dbm.open(dbpath, 'c')
  return db

def Login(username, password):
  if username != None and password != None:
    db = getDb()
    usermd5 = makeMd5(username)
    if usermd5 in db:
      value = json.loads(db[usermd5])
      password = makeMd5(password)
      if password != value['password']:
        db.close()
        return {
          'status': 1,
          'message': '密码错误'
        }
      else:
        token = value['username'] + value['password'] + value['root_path']
        token = makeMd5(token)
        db[token] = usermd5 #需要再次base64加密
        db.close()
        return {
          'status': 0,
          'message': '登陆成功',
          'token': enToken(token)
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

def getUser():
  token = request.headers.get('Authorization')
  db = getDb()
  token = token = deToken(token)
  if token in db:
    user = db[token]
    user = json.loads(db[user])
    del user['password']
    db.close()
    return {
      'status': 0,
      'message': '已登陆',
      'user': user
    }
  else:
    db.close()
    return {
      'status': 1,
      'message': '未登陆'
    }

def checkLogin(token):
  db = getDb()
  token = deToken(token)
  if token in db:
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
  user_key = makeMd5(params['username'])
  user_key = '%s%s'%('user.',user_key)
  params['password'] = makeMd5(params['password'])
  params['crated_at'] = now
  params['uptiem'] = now
  db[user_key] = json.dumps(params)
  db.close()
  return {
    'status': 0,
    'message': '添加成功'
  }

def delAdmin(username):
  if username:
    db = getDb()
    user_key = makeMd5(username)
    user_key = '%s%s'%('user.',user_key)
    if user_key in db:
      del db[user_key]
      return {
        'status': 0,
        'message': '删除成功'
      }
    return {
      'status': 1,
      'message': '管理员不存在'
    }
  return {
    'status': 1,
    'message': '用户名不能为空'
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
