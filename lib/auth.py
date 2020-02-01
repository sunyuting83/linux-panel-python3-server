import dbm
import os
import time
import json
from functools import wraps
from .bottle import request
from .utils import abort, enToken, deToken, makeMd5
from config import Conf

'''
  说明以下
  用户key: username md5
  用户value: username, password, root_path, isadmin, uptiem, crated_at => josn.dumps(values)
  token key: username + password + root_path => (md5) -> (base64)
  token value: 用户key
'''

secret_key =Conf.SECRET_KEY

def getDb():
  dbpath = os.path.join(os.getcwd(), 'db/manage')
  db = dbm.open(dbpath, 'c')
  return db

def Login(username, password):
  if username != None and password != None:
    db = getDb()
    usermd5 = '%s%s'%('user.',makeMd5(username + secret_key))
    if usermd5 in db:
      password = makeMd5(password + secret_key)
      value = json.loads(db[usermd5])
      if password != value['password']:
        db.close()
        return {
          'status': 1,
          'message': '密码错误'
        }
      else:
        token = value['username'] + value['root_path'] + secret_key + value['password']
        token = makeMd5(token)
        if token not in db:
          db[token] = usermd5
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
  token = deToken(token)
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
  db = getDb()
  token = request.headers.get('Authorization')
  token = deToken(token)
  if token in db:
    del db[token]
    db.close()
    return {
      'status': 0,
      'message': '已登出'
    }
  else:
    db.close()
    return {
      'status': 1,
      'message': '未登陆'
    }

def addAdmin(params):
  db = getDb()
  now = int(time.time())
  user_key = makeMd5(params['username'] + secret_key)
  user_key = '%s%s'%('user.',user_key)
  if user_key in db:
    db.close()
    return {
      'status': 1,
      'message': '用户已存在'
    }
  else:
    params['password'] = makeMd5(params['password'] + secret_key)
    params['crated_at'] = now
    params['uptiem'] = now
    token = params['username'] + params['root_path'] + secret_key + params['password']
    token = makeMd5(token)
    params['token'] = token
    db[user_key] = json.dumps(params)
    db.close()
    return {
      'status': 0,
      'message': '添加成功'
    }

def delAdmin(username):
  if username:
    user = getUser()
    if user['user']['isadmin']:
      db = getDb()
      user_key = makeMd5(username + secret_key)
      user_key = '%s%s'%('user.',user_key)
      if user_key in db:
        deluser = json.loads(db[user_key])
        if username != deluser['username']:
          token = deluser['token']
          del db[user_key]
          if token in db:
            del db[token]
          db.close()
          return {
            'status': 0,
            'message': '删除成功'
          }
        db.close()
        return {
          'status': 1,
          'message': '无法删除自己'
        }
      db.close()
      return {
        'status': 1,
        'message': '管理员不存在'
      }
    db.close()
    return abort(403)
  return {
    'status': 1,
    'message': '用户名不能为空'
  }

def getAdminList():
  user = getUser()
  if user['user']['isadmin']:
    db = getDb()
    admin_list = []
    for key in db.keys():
      if 'user.' in str(key, encoding = "utf8"):
        admin_list.append(json.loads(db[key]))
    db.close()
    return {
      'status': 0,
      'message': 'list',
      'data': admin_list
    }
  return abort(403)