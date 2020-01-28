from lib import route, response, request, getSys, getMem, getHtop, abort, return_Json, getPath, login_required, getUser

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
@login_required
def getsystem():
  system = getSys()
  return return_Json(system)

# 内存,网络
@route('/getSync')
@login_required
def getsync():
  mem = getMem()
  return return_Json(mem)

# 进程列表
@route('/htop')
@login_required
def gethtop():
  top = getHtop()
  return return_Json(top)

# 目录获取
@route('/getPath')
@login_required
def getpath():
  path = request.query.path
  default_path = getUser()
  if default_path['status'] == 0:
    default_path = default_path['user']['root_path']
    data = getPath(default_path, path)
    return data.getJson()
  return default_path