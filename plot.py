import threading
import time

import serial
from matplotlib import pyplot as plt

from file_manager import Logger

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from queue import *

import asyncio

from window.graph import Graph
from window.serial_data import SerialData
from window.text import UIText


class Plotter:
    frame = 0

    logger = None

    MESSAGE_KEY = 'message'

    def __init__(self, window):
        self.window = window
        # self.close()
        # self.open()
        self.graph = None

        if self.window.logging:
            self.logger = Logger()
        else:
            self.logger = None

        self.serial_data = SerialData()

        self.message = UIText(self.window, 'No data...', 'red')

        self.thread = None

    def show(self):
        # self.port = self.window.serial_port
        # self.open()

        self.graph = Graph(self.window)

        print('starting with serial port ', self.window.serial_port)
        self.serial_data.start(self.window.serial_port, self.update, self.show_message)

        # self.thread = threading.Thread(target=self.get_data)
        # self.thread.start()

    def hide(self):
        if self.graph is not None:
            self.graph.canvas.get_tk_widget().pack_forget()
            self.graph = None
        self.serial_data.stop()
        # self.thread.

    # def queue_message(self):
    #     time.sleep(2)
    #     if len(self.graph.y) == 0:
    #         self.window.add_element(self.MESSAGE_KEY, UIText(self.window, 'No data...', 'red'))
    #
    # def get_data(self):
    #     add_message_thread = threading.Thread(target=self.queue_message)
    #     add_message_thread.start()
    #     while True:
    #         if self.isOpen():
    #             voltage = float(self.readline().decode())
    #             data = self.weight_from_voltage(voltage)
    #             if self.MESSAGE_KEY in self.window.ui_elements:
    #                 self.window.remove(self.MESSAGE_KEY)
    #             self.update(data)
    #         else:
    #             break
    def show_message(self):
        self.message.show()

    def update(self, voltage):
        y_val = self.weight_from_voltage(voltage)

        if self.message.winfo_ismapped():
            self.message.hide()

        self.graph.add(self.frame, y_val)

        if self.logger:
            self.logger.add_line(self.frame, y_val)

        self.frame += 1

    def weight_from_voltage(self, voltage):
        val = self.window.curve_data.get_point(voltage)
        # print('voltage: ' + str(voltage) + ', output: ' + str(val))
        return val
        # cf = 19.5
        # voltage = voltage * cf
        # return voltage

