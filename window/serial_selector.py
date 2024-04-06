import glob
import sys
import serial
import tkinter as tk


class SerialSelector(tk.OptionMenu):
    def __init__(self, main):

        self.window = main

        self.options = []

        self.get_serial_ports()
        self.serial_port = tk.StringVar(value='Select port')

        super().__init__(self.window, self.serial_port, *self.options, command=self.select)
        # self.menu = tk.OptionMenu(self.main, self.var, *self.options)

    def show(self):
        self.pack(pady=(0, 60))
        self.select(self.serial_port.get())

    def hide(self):
        self.pack_forget()

    def options_changed(self):
        print('options changed')
        self.serial_port.set('')
        self['menu'].delete(0, 'end')
        for choice in self.options:
            self['menu'].add_command(label=choice, command=tk._setit(self.serial_port, choice, self.select))

    def select(self, val):
        self.window.set_serial_selected(val)
        print('selecting ', val)

    def get_serial_ports(self):
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass

        self.options = result
