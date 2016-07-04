#!env python

# Copyright (C) 2013-2016 JFEngels
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.




import sys, os

cpn = 48

max_proc = os.environ.get("LSB_MAX_NUM_PROCESSORS")
threads  = os.environ.get("OMP_NUM_THREADS")
hostname = os.environ.get("HOSTNAME")

# called from inside an lsf job 
if(max_proc != None and threads != None):
	cores   = int(max_proc)
	threads = int(threads)
	if (hostname[3] == "p"):
		cpn = 48
	elif (hostname[3] == "a"):
		cpn = 64
	else:
		print "Unknown host configuration"
elif (threads != None):
	print "OMP_NUM_THREADS not set!"

# called outside an lsf job
else:
	if (len(sys.argv) < 3):
		print("usage: "+sys.argv[0]+" cores threads [core per node=48]")
		sys.exit(23)
	else:
		cores   = int(sys.argv[1])
		threads = int(sys.argv[2])
		if (len(sys.argv) == 4):
			cpn = int(sys.argv[3])

	print "export OMP_NUM_THREADS="+str(threads) 


if (cores%threads != 0):
	print("Number of cores not divisible by number of threads")
	sys.exit(23)

if (cpn%threads != 0):
	print("Number of cores per node is not divisible by number of threads")
	sys.exit(23)

out = "export LSB_PJL_TASK_GEOMETRY=\"{(0"

for i in range(1,cores/threads):
	if (i%(cpn/threads) == 0):
		out = out + ") ("
	else:
		out = out + ","
	out = out + str(i)
out = out + ")}\""
print out

