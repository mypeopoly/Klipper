import time

class PrinterLoadCellDigitalOut:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.pin_control = self.printer.lookup_object('pins')
        self.reset_pin = config.get('pin')
        self.gcode = self.printer.lookup_object('gcode')
        self.load_cell_reset_pin = None
        self.gcode.register_command('LC28', self.cmd_clear_load_cell)
        self.gcode.register_command('LL28', self.cmd_set_pin_low)
        self.gcode.register_command('LH28', self.cmd_set_pin_high)
        self.load_cell_reset_pin = self.pin_control.setup_pin('digital_out', self.reset_pin)
        if self.load_cell_reset_pin is not None:
            self.load_cell_reset_pin.setup_max_duration(0) 
            self.load_cell_reset_pin.setup_start_value(1,1,False)
            self.gcode.respond_info("init magneto load cell")
            self.gcode.respond_info(self.reset_pin)
        else:
            self.gcode.respond_info("init magneto load cell failed!!")


    def cmd_set_pin_high(self, gcmd):
        if self.load_cell_reset_pin is not None:
            current_time = self.printer.get_reactor().monotonic()+0.1
            print_time = self.load_cell_reset_pin.get_mcu().estimated_print_time(current_time)
            self.load_cell_reset_pin.set_digital(print_time, 1)
            # self.load_cell_reset_pin(current_time, 1)


    def cmd_set_pin_low(self, gcmd):
        if self.load_cell_reset_pin is not None:
            current_time = self.printer.get_reactor().monotonic()+0.1
            print_time = self.load_cell_reset_pin.get_mcu().estimated_print_time(current_time)
            self.load_cell_reset_pin.set_digital(print_time, 0)

    def cmd_clear_load_cell(self, gcmd):
        self.clear_load_cell()

    def set_cell(self, printime, value):
        if self.load_cell_reset_pin is not None:
            self.load_cell_reset_pin.set_digital(printime, value)
    

    def clear_load_cell(self):
        if self.load_cell_reset_pin is not None:
            current_time = self.printer.get_reactor().monotonic()+0.1
            print_time = self.load_cell_reset_pin.get_mcu().estimated_print_time(current_time)
            self.load_cell_reset_pin.set_digital(print_time, 0)
            # est_time = self.load_cell_reset_pin.get_mcu().estimated_print_time(current_time)
            # next_cmd_time = est_time + 0.2
            # current_time = self.printer.get_reactor().monotonic()
            # self.load_cell_reset_pin.set_digital(next_cmd_time, 1)
            # self.gcode.respond_info("clear load cell value")

            current_time = self.printer.get_reactor().monotonic()+0.5
            print_time = self.load_cell_reset_pin.get_mcu().estimated_print_time(current_time)
            self.load_cell_reset_pin.set_digital(print_time, 1)



def load_config(config):
    return PrinterLoadCellDigitalOut(config)


        # load_cell = self.printer.lookup_object('magneto_load_cell')
        # if load_cell is not None:
        #     load_cell.clear_load_cell()
        #     toolhead.dwell(1.)
