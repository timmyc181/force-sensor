import threading
import time

import serial


class SerialData(serial.Serial):
	def __init__(self):
		super().__init__(None, 9600)

		self.data = []

		self.thread = None
		self.message_callback = None
		self.callback = None

	def start(self, port, callback, message_callback=None):
		# self.port = port
		self.setPort(port)
		self.open()

		self.message_callback = message_callback
		self.callback = callback

		self.thread = threading.Thread(target=self.get_data)
		self.thread.start()

	def stop(self):
		if self.isOpen():
			self.flush()
		self.close()

	def queue_message(self):
		time.sleep(2)
		if len(self.data) == 0 and self.message_callback is not None:
			self.message_callback()

	def get_data(self):
		add_message_thread = threading.Thread(target=self.queue_message)
		add_message_thread.start()
		while True:
			if self.isOpen():
				voltage = float(self.readline().decode())
				self.data.append(voltage)
				self.callback(voltage)
			else:
				break


