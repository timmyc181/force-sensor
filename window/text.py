from tkinter import *


class UIText(Label):
	def __init__(self, window, text, color=None):
		self.window = window

		self.var = StringVar()

		super().__init__(self.window, textvariable=self.var, fg=color)

		self.var.set(text)
		# self.insert(INSERT, message)

	def set(self, text):
		self.var.set(text)
		# self.update()

	def show(self):
		self.pack()

	def hide(self):
		self.pack_forget()
