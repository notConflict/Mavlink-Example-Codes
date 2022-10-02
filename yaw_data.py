import time
import math as m
from pymavlink import mavutil
from dronekit import connect

def mavlink_loop(conn, callbacks):
    interesting_messages = list(callbacks.keys())

    while True:
        conn.mav.heartbeat_send(mavutil.mavlink.MAV_TYPE_ONBOARD_CONTROLLER,
                                mavutil.mavlink.MAV_AUTOPILOT_GENERIC,
                                0,
                                0,
                                0)

        m = conn.recv_match(type=interesting_messages, timeout=1, blocking=True)

        callbacks[m.get_type()](m)

def att_msg_callback(value):
    global heading_north_yaw
    if heading_north_yaw is None:
        heading_north_yaw = value.yaw
        print("INFO: Received first ATTITUDE message with heading yaw %.2f degrees" % m.degrees(heading_north_yaw))


print("Connecting to flight controller...")

vehicle = mavutil.mavlink_connection(
    '/dev/ttyACM',
    autoreconnect = True,
    source_system = 1,
    source_component = 93,
    baud=9600,
    force_connected=True,
)

print("Successfull connect flight controller...")

mavlink_callbacks = {
    'ATTITUDE': att_msg_callback,
}

try:
	while True:
		mavlink_loop(vehicle, mavlink_callbacks)
except Exception as e:
	print(e)
else:
	pass
finally:
	vehicle.close()
	print("Vehicle closed!")


