import os
import time
# import threading
from math import degrees
from pymavlink import mavutil
from dronekit import connect


os.environ["MAVLINK20"] = "1"


exit_var = False
heading_north_yaw = None

# looping
def mavlink_loop(conn, callbacks):
	interesting_messages = list(callbacks.keys())

	while not exit_var:
		conn.mav.heartbeat_send(mavutil.mavlink.MAV_TYPE_ONBOARD_CONTROLLER,
								mavutil.mavlink.MAV_AUTOPILOT_GENERIC,
								0,
								0,
								0)

		m = conn.recv_match(type=interesting_messages, timeout=1, blocking=True)

		if m is None:
			continue

		callbacks[m.get_type()](m)


# response
def att_msg_callback(value):
	print("Roll: {0:.2f}, Pitch: {1:.2f}, Yaw: {2:.2f}".format(degrees(value.roll), degrees(value.pitch), degrees(value.yaw)))

print("Connecting to flight controller...")

vehicle = mavutil.mavlink_connection(
    '/dev/ttyACM0',
    autoreconnect = True,
    source_system = 1,
    source_component = 93,
    baud=115200,
    force_connected=True,
)

print("Successfull connect flight controller...")

mavlink_callbacks = {
	'ATTITUDE': att_msg_callback,
}

# mavlink_thread = threading.Thread(target=mavlink_loop, args=(vehicle, mavlink_callbacks))
# mavlink_thread.start()

print("Start listening data")

try:
	while not exit_var:
		mavlink_loop(vehicle, mavlink_callbacks)
		time.sleep(1)
except Exception as e:
	print(e)
else:
	pass
finally:
	exit_var = False
	vehicle.close()
	print("Vehicle closed!")


