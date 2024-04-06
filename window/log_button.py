from tkinter import *


class LogButton(Checkbutton):
	def __init__(self, window):
		self.window = window

		self.var = IntVar()
		self.var.set(self.window.logging)

		super().__init__(
			self.window,
			text='Logging',
			variable=self.var,
			command=self.update,
			onvalue=1,
			offvalue=0
		)

	def show(self):
		self.pack(pady=(0, 10))

	def hide(self):
		self.pack_forget()

	def update(self):
		self.window.logging = self.var.get() == 1
