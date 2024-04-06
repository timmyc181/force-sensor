from tkinter import *


class TextField(Entry):
	def __init__(self, window):
		super().__init__(window)
		self.window = window

	def get_float(self) -> float:
		return float(self.get())

	def show(self):
		self.pack()

	def hide(self):
		self.clear()
		self.pack_forget()

	def clear(self):
		self.delete(0, END)
