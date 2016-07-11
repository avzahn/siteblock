import platform
import subprocess
import psutil
from shutil import copyfile

def hosts_entries(domain):

	urls = []

	prefixes = ['www','m','login','m.login']

	for prefix in prefixes:

		urls.append("%s.%s"%(prefix,domain))

	lines = []

	for url in urls:
		lines.append("127.0.0.1 %s"%(url))
		lines.append("::1 %s"%(url))

	return lines


def backup(path):
	target = "%s.backup"%(path)
	copyfile(path,target)

def restore(path):
	src = "%s.backup"%(path)
	copyfile(src,path)

def write_hosts(lines,hostspath):

	backup(hostspath)

	with open(hostspath,'a') as hostsfile:
		for line in lines:
			print >>hostsfile, line

def kill_browsers():

	names = ['chrome','safari','firefox']

	for proc in psutil.process_iter():
		for name in names:
			if name in proc.name():
				proc.kill()

def flush_dnscache():
	subprocess.call(["killall","-HUP","mDNSResponder"])
	subprocess.call(["discoveryutil","mdsnsflushcache"])
	kill_browsers()


if __name__ == '__main__':
	hostspath = '/private/etc/hosts'
	write_hosts(hosts_entries('facebook.com'),hostspath)
	flush_dnscache()