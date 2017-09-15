import tkinter as tk
from tkinter.filedialog import askopenfilename
import time
import logging
from io import StringIO

import serial.tools.list_ports as list_ports
from tk_tools import SmartOptionMenu
from booty.util import create_serial_port, create_blt, erase_device, load_hex, verify_hex


logger = logging.getLogger('bootycontrol')
logging.basicConfig(level=logging.DEBUG)


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('bootyControl')

        # local variables
        self.hex_file_path = ''
        self.port_name = None

        self.log_string = StringIO()
        self.ch = logging.StreamHandler(self.log_string)
        logger.addHandler(self.ch)

        booty_logger = logging.getLogger('booty')
        booty_logger.addHandler(self.ch)

        # gui setup
        self.page_title = tk.Label(self, text='bootyControl', font=('Helvetica', 16))
        self.page_title.grid(row=0, column=0, columnspan=2, sticky='news')

        self.ser_port_label = tk.Label(self, text='Serial Port')
        self.ser_port_label.grid(row=1, column=0, sticky='nes')

        self.ser_port_om = SmartOptionMenu(self, list_ports.comports(), callback=self.choose_ser_port)
        self.ser_port_om.grid(row=1, column=1, sticky='nws')

        self.ser_baud_label = tk.Label(self, text='Baud Rate')
        self.ser_baud_label.grid(row=2, column=0, sticky='nes')

        self.ser_baud_entry = tk.Entry(self)
        self.ser_baud_entry.grid(row=2, column=1, sticky='nws')

        self.ser_baud_entry.insert(0, '115200')

        self.choose_hex_btn = tk.Button(self, text='Choose hex file...', command=self.choose_hex_file)
        self.choose_hex_btn.grid(row=3, column=0, columnspan=2, sticky='news')

        self.erase_btn = tk.Button(self, text="Erase Device", command=self.erase_device)
        self.erase_btn.grid(row=4, column=0, columnspan=2, sticky='news')

        self.load_btn = tk.Button(self, text="Load Device", command=self.load_device)
        self.load_btn.grid(row=5, column=0, columnspan=2, sticky='news')
        self.load_btn['state'] = 'disabled'

        self.verify_btn = tk.Button(self, text="Verify Device", command=self.verify_device)
        self.verify_btn.grid(row=6, column=0, columnspan=2, sticky='news')
        self.verify_btn['state'] = 'disabled'

        self.console_text = tk.Text(self)
        self.console_text.grid(row=7, column=0, columnspan=2, sticky='news')
        self.console_text['state'] = 'disabled'

        self.mainloop()

    def choose_hex_file(self):
        self.hex_file_path = askopenfilename(title='choose hex file', filetypes=[('hex', '*.hex')])
        self.update_console('hex file chosen: {}'.format(self.hex_file_path))

        if self.port_name:
            self.load_btn['state'] = 'normal'
            self.verify_btn['state'] = 'normal'

    def choose_ser_port(self):
        port_name = self.ser_port_om.get()
        self.port_name = port_name.split('-')[0].strip()
        self.update_console('serial port chosen: {}'.format(self.port_name))

        if self.hex_file_path:
            self.load_btn['state'] = 'normal'
            self.verify_btn['state'] = 'normal'

    def erase_device(self):
        baudrate = int(self.ser_baud_entry.get())
        sp = create_serial_port(self.port_name, baudrate)
        blt = create_blt(sp)

        self.update_console(clear=True)

        # allow time for threads and hardware to spin up
        time.sleep(0.5)

        self.update_console('loading...')
        if erase_device(blt):
            self.update_console('device erased!')
        else:
            self.update_console('device erase failed')

        blt.end_thread()
        time.sleep(0.01)
        sp.close()

    def load_device(self):
        baudrate = int(self.ser_baud_entry.get())
        sp = create_serial_port(self.port_name, baudrate)
        blt = create_blt(sp)

        self.update_console(clear=True)

        # allow time for threads and hardware to spin up

        time.sleep(0.5)

        self.update_console('loading...')
        if load_hex(blt, self.hex_file_path):
            self.update_console('device successfully loaded!')
        else:
            self.update_console('device load failed')

        blt.end_thread()
        time.sleep(0.01)
        sp.close()

    def verify_device(self):
        baudrate = int(self.ser_baud_entry.get())
        sp = create_serial_port(self.port_name, baudrate)
        blt = create_blt(sp)

        self.update_console(clear=True)

        # allow time for threads and hardware to spin up
        time.sleep(0.5)

        self.update_console('verifying...')

        if verify_hex(blt, self.hex_file_path):
            self.update_console('device verified!')
        else:
            self.update_console('device verification failed')

        blt.end_thread()
        time.sleep(0.01)
        sp.close()

    def update_console(self, string=None, clear=False):
        if string:
            logger.info(string)

        self.console_text['state'] = 'normal'

        if clear:
            self.console_text.delete(1.0, tk.END)
        self.console_text.insert(tk.END, self.log_string.getvalue().strip() + '\n')
        self.log_string.seek(0)
        self.log_string.truncate(0)

        self.console_text['state'] = 'disabled'

        self.update()


def main():
    app = Application()

if __name__ == '__main__':
    main()
