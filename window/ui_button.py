from tkinter import *


class UIButton(Button):
	def __init__(self, window, name, action):
		super().__init__(window, text=name, command=action)

	def show(self):
		self.pack(pady=0)

	def hide(self):
		self.pack_forget()

	def enable(self):
		self['state'] = 'normal'

	def disable(self):
		self['state'] = 'disabled'
