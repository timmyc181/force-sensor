import numpy as np

from window.TextField import TextField
from window.serial_data import SerialData
from window.text import UIText
from window.ui_button import UIButton
from scipy.optimize import curve_fit
import pickle


class CurveData:
	def __init__(self):
		self.data = {}

		self.a_opt = None
		self.b_opt = None
		# self.c_opt = None

	def calculate_curve(self):
		x_data = np.array(list(self.data.keys()))
		y_data = np.array(list(self.data.values()))
		popt, pcov = curve_fit(self.model_f, x_data, y_data)
		self.a_opt, self.b_opt = popt
		# popt, popv = curve_fit(self.model_f, self.data.keys(), self.data.values(), p0=[3, 2, -16])

	def get_point(self, voltage):
		return self.model_f(voltage, self.a_opt, self.b_opt)

	def is_valid(self):
		return self.a_opt is not None and self.b_opt is not None # and self.c_opt is not None

	@staticmethod
	def model_f(x, a, b):
		return a * (x ** b)

	def save(self, data):
		self.data = data
		self.calculate_curve()

		print(str(self.a_opt) + 'x^' + str(self.b_opt))

		with open('curve_data.pkl', 'wb') as output:
			pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)

	@staticmethod
	def load():
		try:
			with open('curve_data.pkl', 'rb') as inp:
				return pickle.load(inp)
		except IOError:
			return CurveData()


class CalibrateView:
	def __init__(self, window):
		self.data = {}

		self.window = window

		self.serial = SerialData()

		self.voltage_text = UIText(window, '--v')
		self.result_text = UIText(window, '')
		self.text_field = TextField(window)
		self.add_button = UIButton(window, 'add', self.add)

		self.done_button = UIButton(window, 'done', self.done)

	def show(self):
		self.serial.start(self.window.serial_port, self.update_voltage)
		self.voltage_text.show()
		self.text_field.show()
		self.add_button.show()
		self.done_button.show()
		self.result_text.show()

	def hide(self):
		self.serial.stop()
		self.voltage_text.hide()
		self.text_field.hide()
		self.add_button.hide()
		self.done_button.hide()
		self.result_text.show()

	def update_voltage(self, voltage):
		self.voltage_text.set(str(voltage) + 'v')

	def add(self):
		last_voltage = self.serial.data[len(self.serial.data) - 1]
		self.data[last_voltage] = self.text_field.get_float()

		self.update_result()

		self.text_field.clear()

	def update_result(self):

		text = ''
		for key in self.data.keys():
			text += str(key) + 'v: ' + str(self.data[key]) + ' N'

			text += '\n'

		if self.serial.isOpen():
			self.result_text.set(text)

	def done(self):
		if self.data:
			self.window.curve_data.save(self.data)
		self.window.form_view()
