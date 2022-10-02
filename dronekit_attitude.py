import time
import threading as th
from math import degrees
from dronekit import connect

connection_string 	= '/dev/ttyACM0'
connection_baud 	= 9600

print("Waiting connection...")
vehicle = connect(connection_string, baud=connection_baud, wait_ready=False)
print("Connection success")

def attitude_data(veh):
	while True:
		print("R: {0}, P: {1}, Y: {2}".format(degrees(veh.attitude.roll),
										#degrees(veh.attitude.pitch),
										#degrees(veh.attitude.yaw)))

thread_attitude = th.Thread(target=attitude_data, args=(vehicle,))
thread_attitude.start()

try:
	while True:
		time.sleep(1)
except Exception as e:
	print(e)
else:
	pass
finally:
	print("Closed the connection.")
	vehicle.close()

