import os
import select
import subprocess
import fcntl

def humanSize(bytes):
	for x in ['bytes','KB','MB','GB','TB']:
		if bytes < 1024.0:
			return "%3.1f%s" % (bytes, x)
		bytes /= 1024.0
	return 0


x = subprocess.Popen(["dd","if=/dev/zero","of=/dev/null"], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
print x.pid

outfile = x.stderr
outfd = outfile.fileno()
file_flags = fcntl.fcntl(outfd, fcntl.F_GETFL)
fcntl.fcntl(outfd, fcntl.F_SETFL, file_flags | os.O_NOFOLLOW)

while x.poll() == None:
	ready = select.select([outfd],[],[],.2) # wait for input
	
	if len(ready[0]) == 0:
		os.system("kill -USR1 %s" % x.pid)
	else:
		tmp = outfile.readline()[:-1]
		if len(tmp.split()) > 3:
			print humanSize(tmp)
	
