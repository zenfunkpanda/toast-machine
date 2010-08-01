import os
import select
import subprocess

import select
import fcntl

x = subprocess.Popen(["dd","if=/dev/zero","of=/dev/null"], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
print x.pid

outfile = x.stderr
outfd = outfile.fileno()
file_flags = fcntl.fcntl(outfd, fcntl.F_GETFL)
fcntl.fcntl(outfd, fcntl.F_SETFL, file_flags | os.O_NDELAY)

while x.poll:
	ready = select.select([outfd],[],[],5) # wait for input
	
	if len(ready[0]) == 0:
		print "timeout... continua"
	else:
		print len(ready[0])

x.kill()
	
