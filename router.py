from lib import route, response, request, getSys, getMem, getHtop, abort, return_Json, getPath

# 首页403
@route('/')
def index():
  return abort(403)

# 防止爬虫
@route('/robots.txt')
def robots():
	# print app.static_folder
	response.content_type = 'text/plain; charset=UTF-8'
	return '''User-agent: *
Disallow: /'''

# CPU,硬盘,系统信息
@route('/getSystem')
def getsystem():
  system = getSys()
  return return_Json(system)

# 内存,网络
@route('/getSync')
def getsync():
  mem = getMem()
  return return_Json(mem)

# 进程列表
@route('/htop')
def gethtop():
  top = getHtop()
  return return_Json(top)

# 目录获取
@route('/getPath')
def getpath():
  path = request.query.path
  default_path = '/home/sun'
  data = getPath(default_path, path)
  return data.getJson()