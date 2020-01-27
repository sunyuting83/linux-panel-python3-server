import json
import os
import datetime
import time
from .utils import getSize, abort, return_Json
from .getImage import getImg

class getPath:

	def __init__(self, path, this_path):
		self.data = json.dumps({'status': 0})
		default_path = path
		rootlen = len(default_path)
		thispath = this_path
		root_path = path
		isroot = 'isroot'
		thisname = None

		if thispath is not None:
			if '../' in thispath:
				self.data = abort(403)
			if os.path.exists(default_path + thispath) is True:
				root_path = default_path + thispath
				# print(root_path)
				isroot = 'nope'
				thisname = thispath.split('/')
				# thisurl = getThisUrl(thispath)
				# print(thisname,thisurl)
			else:
				self.data = abort(403)
		self.rootpath = root_path
		self.root = {}
		self.rootlen = rootlen
		status = json.loads(self.data)['status']
		if status != 1:
			self.createDict()
			path = json.loads(json.dumps(self.root))
			self.data =  {
				'pagename': 'thispath',
				'path': path,
				'isroot': isroot,
				'thisname': thisname,
				'thispath': thispath
			}

	'''迭代生成目录树，用dict保存'''
	def createDict(self):
		rootpath = self.rootpath
		root = self.root
		pathList = os.listdir(rootpath)
		# hasData = getAllData(path)

		# print (pathList)
		for item in pathList:
			self.item = item
			if self.isDir(self.getJoinPath()):
				if not item.startswith('.'):
					root[item] = {}
					self.path = self.getJoinPath()
					root[item]['thispath'] = self.path[self.rootlen:]
					root[item]['picture'] = getImg('path')
					root[item]['filetime'] = self.TimeStampToTime(os.path.getmtime(self.path))
					root[item]['isdir'] = True
					# createDict(path, root[item])
					self.path = '/'.join(self.path.split('/')[:-1])
			else:
				if not item.startswith('.'):
					root[item] = {}
					self.allpath = self.rootpath + item
					filepath = self.rootpath[self.rootlen:]
					# state = getState('%s%s%s' %(path, '/', item), hasData)
					self.realPath = '%s%s%s' %(self.rootpath, '/', item)
					filesize = getSize(os.path.getsize(self.realPath))
					filetime = self.TimeStampToTime(os.path.getmtime(self.realPath))

					root[item]['thispath'] = '%s%s%s' %(filepath, '/', item)
					root[item]['picture'] = self.file_extension()
					root[item]['filesize'] = filesize
					root[item]['filetime'] = filetime
					root[item]['isdir'] = False


	'''合并路径和目录，返回完整路径'''
	def getJoinPath(self):
		return os.path.join(self.rootpath, self.item)


	'''判断是否为目录'''
	def isDir(self, path):
		if os.path.isdir(path):
			return True
		return False

	'''返回json格式数据'''
	def getJson(self):
		return return_Json(self.data)

	def file_extension(self):
		extension = os.path.splitext(self.allpath)[1]
		return getImg(extension)

	def TimeStampToTime(self,path):
		timeStruct = time.localtime(path)
		return time.strftime('%Y-%m-%d %H:%M:%S',timeStruct)
