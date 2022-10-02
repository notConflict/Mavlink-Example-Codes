import signal as sig
import time

terminal_access = False

def close_call(signum, frame):
	global terminal_access
	terminal_access = True
	print('Alarm at:', time.ctime())  
	print("CTRL+C: signal > {0} | frame > {1}".format(signum, frame))

def terminate_call(signum, frame):
	global terminal_access
	terminal_access = True
	print("terminate the program.")

def stop_call(signum, frame):
	global terminal_access
	terminal_access = True
	print("stopped the program.")

sig.signal(sig.SIGINT, close_call)
sig.signal(sig.SIGTERM, terminate_call)
sig.signal(sig.SIGTSTP, stop_call)
sig.signal(sig.SIGTSTP, resume_call)

sig.alarm(3)
print('Current alarm:', time.ctime())  
sig.alarm(6)
print('done')

# try:
# 	while not terminal_access:
# #		print("printed")
# #		time.sleep(1)
# 		pass
# except Exception as e:
# 	print(e)
# finally:
# 	print("closed")
