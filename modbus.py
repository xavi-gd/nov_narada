import serial
import minimalmodbus
import time
import json


class Module:

    def __init__(self, module_id, module_values):
        VOLT = 0
        CURRENT = 1
        REMAIN_CAPACITY = 2
        AVG_TEMP_CELL = 3
        ENV_TEMP = 4
        SOC = 8
        SOH = 10
        PCB_TEMP = 11
        FIRST_CELL_VOLT = 14
        LAST_CELL_VOLT = 29
        FIRST_CELL_TEMP = 31
        LAST_CELL_TEMP = 46
        FULL_CAPACITY = 47
        CHARGE_TIME = 48
        DISCHARGE_TIME = 49

        self.id = module_id
        self.volt = module_values[VOLT]
        self.current = module_values[CURRENT]
        self.remain_capacity = module_values[REMAIN_CAPACITY]
        self.avg_cell_temp = module_values[AVG_TEMP_CELL]
        self.env_temp = module_values[ENV_TEMP]
        self.soc = module_values[SOC]
        self.soh = module_values[SOH]
        self.pcb_temp = module_values[PCB_TEMP]
        self.cell_volt = module_values[FIRST_CELL_VOLT:LAST_CELL_VOLT + 1]
        self.cell_temp = module_values[FIRST_CELL_TEMP:LAST_CELL_TEMP + 1]
        self.full_capacity = module_values[FULL_CAPACITY]
        self.charge_time = module_values[CHARGE_TIME]
        self.discharge_time = module_values[DISCHARGE_TIME]

    def parse_values(self):
        self.id = 34
        print("my id = " + str(self.id))


def get_module_list():
    numbers = [39, 40]
    for number in numbers:
        battery_module = minimalmodbus.Instrument('/dev/ttyUSB0', number)  # port name, slave address (in decimal)
        battery_module.serial.baudrate = "9600"
        battery_module.serial.timeout = 0.5
        modules = []
    
        scale_factor_values = [0.0100, 0.1000, 0.1000, 0.1000, 0.1000, 1.0000, 1.0000, 1.0000, 0.0001, 1.0000, 0.0001, 0.1000, 10.0000, 1.0000, 0.0010, 0.0010, 0.0010, 0.0010, 0.0010, 0.0010, 0.0010, 0.0010, 0.0010, 0.0010, 0.0010, 0.0010, 0.0010, 0.0010, 0.0010, 0.0010, 1.0000, 0.1000, 0.1000, 0.1000, 0.1000, 0.1000, 0.1000, 0.1000, 0.1000, 0.1000, 0.1000, 0.1000, 0.1000, 0.1000, 0.1000, 0.1000, 0.1000, 0.1000, 1.0000, 1.0000, 1.0000]
        offset_values = [0.0, -10000.0, 0.0, -400.0, -400.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -400.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -400.0, -400.0, -400.0, -400.0, -400.0, -400.0, -400.0, -400.0, -400.0, -400.0, -400.0, -400.0, -400.0, -400.0, -400.0, -400.0, 0.0, 0.0, 0.0, 0.0]

        analog_values = battery_module.read_registers(4095, 51, 4)
        print(analog_values)
    
        lista_suma = []
        lista_multi = []

        for i in range(len(analog_values)):
            lista_suma.append(analog_values[i] + offset_values[i])
            lista_multi.append(lista_suma[i] * scale_factor_values[i])
            
            
        modules.append(Module(number, lista_multi))
        
        return modules


if __name__ == "__main__":
    modules = get_module_list()
    print(modules[0].volt)
