from .bottle import response
import json

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