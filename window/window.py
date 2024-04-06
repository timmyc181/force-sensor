import tkinter as tk

from plot import Plotter
from window.calibrate.calibrate_view import CalibrateView, CurveData
from window.log_button import LogButton
from window.serial_selector import SerialSelector
from window.text import UIText
from window.ui_button import UIButton


class Window(tk.Tk):
    logging = False
    serial_port = None

    def __init__(self):
        super().__init__()

        self.title('Title')

        self.config(padx=40, pady=30)

        self.curve_data = CurveData.load()

        self.port_selection_view_elements = {
            'serial_selector': SerialSelector(self),
            'log_button': LogButton(self),
            'calibrate_button': UIButton(self, 'calibrate', self.calibrate_view),
            'connect_button': UIButton(self, 'connect', self.connect)
        }
        self.calibrate_elements = {
            'calibrate_text': CalibrateView(self)
        }
        self.plot_view_elements = {
            'plotter': Plotter(self),
            'disconnect_button': UIButton(self, 'disconnect', self.disconnect),
        }

        self.form_view()

        self.mainloop()

    def set_serial_selected(self, val):
        if val and val != 'Select port':
            self.port_selection_view_elements['connect_button'].enable()
            self.port_selection_view_elements['calibrate_button'].enable()
            self.serial_port = val
        else:
            self.port_selection_view_elements['connect_button'].disable()
            self.port_selection_view_elements['calibrate_button'].disable()
            self.serial_port = None

    def connect(self):
        self.plot_view()

    def disconnect(self):
        self.form_view()

    def plot_view(self):
        self.remove(list(self.port_selection_view_elements.values()))
        self.remove(list(self.calibrate_elements.values()))

        self.add_elements(self.plot_view_elements.values())

        self.set_serial_selected(self.serial_port)

    def form_view(self):
        self.remove(list(self.plot_view_elements.values()))
        self.remove(list(self.calibrate_elements.values()))

        self.add_elements(self.port_selection_view_elements.values())

    def calibrate_view(self):
        self.remove(list(self.plot_view_elements.values()))
        self.remove(list(self.port_selection_view_elements.values()))

        self.add_elements(self.calibrate_elements.values())

    @staticmethod
    def remove(parameter):
        if type(parameter) is str:
            parameter.hide()

        elif type(parameter) is list:
            for element in parameter:
                element.hide()

    @staticmethod
    def add_elements(elements):
        for element in elements:
            element.show()








