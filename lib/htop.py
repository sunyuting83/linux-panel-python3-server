# coding:utf-8
import subprocess
import json

def getHtop():
	top_info = subprocess.Popen(["top", "-b", "-n", "1"], stdout=subprocess.PIPE,stderr=subprocess.STDOUT, close_fds=True)
	out, err = top_info.communicate()

	out_info = out.decode('unicode-escape')

	lines = []
	lines = out_info.split('\n')

	data = lines[7:]
	top_list = []
	for i in range(len(data)):
		if len(data[i]) > 0:
			top = data[i].split()
			if 'top' not in top:
				top_list.append([top[11], top[1], top[8], top[0], top[5], top[6]])
	return json.dumps(top_list, ensure_ascii=False)