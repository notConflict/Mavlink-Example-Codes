from apscheduler.schedulers.background import BackgroundScheduler

counter = 0
scheduler_time_second = 1

def test_scheduler_out():
	global counter
	counter += 1
	print("Counting: {0}".format(counter))


# inisialisasi scheduler
test_scheduler = BackgroundScheduler()

# tambah item scheduler
test_scheduler.add_job(test_scheduler_out, 'interval', seconds = scheduler_time_second)
test_scheduler.start()

print("INFO: Sending VISION_POSITION_ESTIMATE messages to FCU")

try:
	while True:
		pass
except Exception as e:
	print(e)