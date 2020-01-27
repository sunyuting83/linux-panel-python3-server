#!/usr/bin/env python
import json
import os
import subprocess
from .utils import getSize

def getSys():
	system = {}
	system['cpu'] = cpu_stat()
	system['uptime'] = uptime_stat()
	system['disk'] = disk_stat()
	system['system'] = systemInfo()
	system['dev'] = dev_info()
	return json.dumps(system)

def getMem():
	system = {}
	system['mem'] = memory_stat()
	system['net'] = net_stat()
	return json.dumps(system)

# mem
def memory_stat():
	mem = {}
	with open("/proc/meminfo", "r") as f:
		lines = f.readlines()
		for line in lines:
			if len(line) < 2: continue
			name = line.split(':')[0]
			var = line.split(':')[1].split()[0]
			if name == 'SwapTotal' or name == 'SwapFree' or name == 'MemTotal' or name == 'MemFree' or name == 'Cached' or name == 'Buffers':
				mem[name] = int(var) * 1024.0
		mem['MemUsed'] = mem['MemTotal'] - mem['MemFree']
		mem['MemPercent'] = round(float(mem['MemUsed']) / float(mem['MemTotal']) * 100, 2)
		mem['RealUsed'] = mem['MemTotal'] - mem['MemFree'] - mem['Buffers'] - mem['Cached']
		mem['RealFree'] = mem['MemTotal'] - mem['RealUsed']
		mem['RealPercent'] = round(float(mem['RealUsed']) / float(mem['MemTotal']) * 100, 2)
		mem['SwapUsed'] = mem['SwapTotal'] - mem['SwapFree']
		mem['SwapPercent'] = round(float(mem['SwapTotal'] - mem['SwapFree']) / float(mem['MemTotal']) * 100, 2)
		mem['CachedPercent'] = round(float(mem['Cached']) / float(mem['MemTotal']) * 100, 2)
		for key in mem:
			if mem[key] is not mem['CachedPercent'] and mem[key] is not mem['MemPercent'] and mem[key] is not mem['RealPercent'] and mem[key] is not mem['SwapPercent']:
				mem[key] = getSize(mem[key])
	return mem

# CPU
def cpu_stat():
	cpu = []
	cpuinfo = {}
	with open("/proc/cpuinfo", "r") as f:
		lines = f.readlines()
		for line in lines:
			if line == '\n':
				cpu.append(cpuinfo)
				cpuinfo = {}
			if len(line) < 2: continue
			name = line.split(':')[0].rstrip().replace(' ', '_')
			var = line.split(':')[1].rstrip()
			if name == 'model_name' or name == 'cpu_MHz' or name == 'cache_size' or name == 'bogomips' or name == 'cpu_cores' or name == 'core_id':
				cpuinfo[name] = var
	return cpu

# time
def uptime_stat():
	# uptime = {}
	uptime = ''
	with open("/proc/uptime", "r") as f:
		con = f.read().split()
		f.close()
		all_sec = float(con[0])
		MINUTE,HOUR,DAY = 60,3600,86400
		# uptime['day'] = int(all_sec / DAY )
		# uptime['hour'] = int((all_sec % DAY) / HOUR)
		# uptime['minute'] = int((all_sec % HOUR) / MINUTE)
		# uptime['second'] = int(all_sec % MINUTE)
		# uptime['Free rate'] = float(con[1]) / float(con[0])
		day = int(all_sec / DAY )
		hour = int((all_sec % DAY) / HOUR)
		minute = int((all_sec % HOUR) / MINUTE)
		# second = int(all_sec % MINUTE)
		uptime = '%s%s%s%s%s%s' % (day,u'天',hour,u'小时',minute,u'分钟')
	return uptime

# net
def net_stat():
	net = []
	with open("/proc/net/dev", "r") as f:
		lines = f.readlines()
		for line in lines[2:]:
			con = line.split()
			intf = dict(
				zip(
					( 'interface','Receive','Transmit','ReceiveBytes','TransmitBytes' ),
					( con[0].rstrip(":"),getSize(int(con[1])),getSize(int(con[9])),int(con[1]),int(con[9]) )
				)
			)

			net.append(intf)
	return net

#disk
def disk_stat():
	hd={}
	disk = os.statvfs("/")
	hd['available'] = getSize(disk.f_bsize * disk.f_bavail)
	hd['capacity'] = getSize(disk.f_bsize * disk.f_blocks)
	hd['used'] = getSize(disk.f_bsize * disk.f_bfree)
	hd['percent'] = round((float(disk.f_bsize * disk.f_bfree) / float(disk.f_bsize * disk.f_blocks)) * 100, 2)
	return hd

# system
def systemInfo():
	import platform
	system = {}
	system['linux'] = platform.platform()
	system['version'] = platform.version()
	system['netname'] = platform.node()
	return system

#dev
def dev_info():
	dev = subprocess.Popen(["df", "-lh"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
	out, err = dev.communicate()

	out_info = out.decode('unicode-escape')

	lines = []
	lines = out_info.split('\n')

	datas = lines[1:]
	df = []
	for line in datas:
		d = {}
		data = line.split()
		if data and 'tmpfs' not in data[0] and 'loop' not in data[0]:
			d['FileSystem'] = data[0]
			d['Size'] = data[1]
			d['Used'] = data[2]
			d['Avail'] = data[3]
			d['Use'] = data[4].rstrip('%')
			d['Mounted'] = data[5]
			df.append(d)
	return df

# if __name__ == '__main__':
# 	import json
# 	print (json.dumps(uptime_stat()))
