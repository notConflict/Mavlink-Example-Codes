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

        if m == None:
            continue

        callbacks[m.get_type()](m)

def attitude_msg(value):
    print("Roll: {0}, Pitch: {0}, Yaw: {0}".format(value.roll, value.pitch, value.yaw))


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
    'ATTITUDE': attitude_msg,
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


