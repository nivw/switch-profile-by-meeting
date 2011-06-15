import os,time

#if os.path.exists("/tmp/switch.debug"):
if True:
    enable_logging = True
else:
    enable_logging = False

if enable_logging and not 'fd' in locals():
    fd = open('/tmp/switch.log','w+')
else:
    fd = None

def debug(*input):
    if enable_logging:
		now = str(time.time())
		print now+str(input)
		print >>fd,now+str(input)
		fd.flush()

