from .bottle import response
import json
import base64
import hashlib

application_json = 'application/json; charset=utf-8'

# size
def getSize(size):
	if size < 1024:
		return '%s%s' %(size, 'B')
	elif size < float(1024*1024):
		size = size/float(1024)
		return '%s%s' %(round(size,2), 'K')
	elif size < float(1024*1024*1024):
		size = size/float(1024*1024)
		return '%s%s' %(round(size,2), 'M')
	else:
		size = size/float(1024*1024*1024)
		return '%s%s' %(round(size,2), 'GB')

def abort(status):
	if status == 403:
		response.status = 403
		response.content_type = application_json
		return json.dumps({'status': 1, 'message': '403'})

def return_Json(data):
	response.content_type = application_json
	return data

# base64解码 Token
def deToken(token):
  token = str(token.replace('Bearer ', '', 1).encode("utf8"), encoding = "utf8")
  token = base64.b64decode(token).decode("utf-8")
  return token
# base64编码 Token return str
def enToken(token):
	return str(base64.b64encode(token.encode("utf-8")), encoding = "utf8")
# md5加密
def makeMd5(string):
  md5 = hashlib.md5(string.encode(encoding='UTF-8')).hexdigest()
  return md5