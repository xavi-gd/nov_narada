import serial
import minimalmodbus
from time import time
import json
import socket


class Module:

    def __init__(self, module_id, module_values):
        VOLT = 0
        CURRENT = 1
        REMAIN_CAPACITY = 2
        AVG_TEMP_CELL = 3
        ENV_TEMP = 4
        WARNING_FLAG = 5
        PROTECTION_FLAG = 6
        FAULT_STATUS = 7
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
        CELL_UV_STATE = 50
        
        self.time = int(time())
        self.id = module_id
        self.volt = module_values[VOLT]
        self.current = module_values[CURRENT]
        self.remain_capacity = module_values[REMAIN_CAPACITY]
        self.avg_cell_temp = module_values[AVG_TEMP_CELL]
        self.env_temp = module_values[ENV_TEMP]
        self.warning_flag = module_values[WARNING_FLAG]
        self.protection_flag = module_values[PROTECTION_FLAG]
        self.fault_status = module_values[FAULT_STATUS]
        self.soc = module_values[SOC] * 100
        self.soh = module_values[SOH] * 100
        self.pcb_temp = module_values[PCB_TEMP]
        self.cell_volt = module_values[FIRST_CELL_VOLT:LAST_CELL_VOLT + 1]
        self.cell_temp = module_values[FIRST_CELL_TEMP:LAST_CELL_TEMP + 1]
        self.full_capacity = module_values[FULL_CAPACITY]
        self.charge_time = module_values[CHARGE_TIME] / 60
        self.discharge_time = module_values[DISCHARGE_TIME] / 60
        self.cell_uv_state = module_values[CELL_UV_STATE]
        self.model = ""
        self.version = ""
        self.serial_number = ""
        self.manufacture_date = ""
        
    def set_avg_values(self, num_modules):
        self.volt /= num_modules
        self.remain_capacity /= num_modules
        self.avg_cell_temp /= num_modules
        self.env_temp /= num_modules
        self.soc /= num_modules
        self.soh /= num_modules
        self.pcb_temp /= num_modules
        self.full_capacity /= num_modules
        self.charge_time /= num_modules
        self.discharge_time /= num_modules
            
    def set_product_info(self, module_info):
        self.model = module_info[0]
        self.version = module_info[1]
        self.serial_number = module_info[2]
        self.manufacture_date = module_info[3]


def get_analog_values():
    numbers = [39, 40, 41, 42, 43, 44, 45, 46]
    modules = []
    lista_avg = [0] * 51
               
    scale_factor_values = [0.0100, 0.1000, 0.1000, 0.1000, 0.1000, 1.0000, 1.0000, 1.0000, 0.0001, 1.0000, 0.0001, 0.1000, 10.0000, 1.0000, 0.0010, 0.0010, 0.0010, 0.0010, 0.0010, 0.0010, 0.0010, 0.0010, 0.0010, 0.0010, 0.0010, 0.0010, 0.0010, 0.0010, 0.0010, 0.0010, 1.0000, 0.1000, 0.1000, 0.1000, 0.1000, 0.1000, 0.1000, 0.1000, 0.1000, 0.1000, 0.1000, 0.1000, 0.1000, 0.1000, 0.1000, 0.1000, 0.1000, 0.1000, 1.0000, 1.0000, 1.0000]
    offset_values = [0.0, -10000.0, 0.0, -400.0, -400.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -400.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -400.0, -400.0, -400.0, -400.0, -400.0, -400.0, -400.0, -400.0, -400.0, -400.0, -400.0, -400.0, -400.0, -400.0, -400.0, -400.0, 0.0, 0.0, 0.0, 0.0]
    

    for number in numbers:
        battery_module = minimalmodbus.Instrument('/dev/ttyUSB0', number)  # port name, slave address (in decimal)
        battery_module.serial.baudrate = "9600"
        battery_module.serial.timeout = 0.5
    
        try:
            analog_values = battery_module.read_registers(4095, 51, 4)
            lista_suma = [0] * 51
            lista_multi = [0] * 51
            
            for i in range(51):
                lista_suma[i] = analog_values[i] + offset_values[i]
                lista_multi[i] = round(lista_suma[i] * scale_factor_values[i], 2)
                lista_avg[i] = lista_multi[i] + lista_avg[i]
                
            modules.append(Module(number, lista_multi))
         
        except:
            pass
    
    num_modules = len(modules)
    modules.append(Module(37, lista_avg))
    avg_module = modules[-1]
    avg_module.set_avg_values(num_modules)

    return modules


def set_module_format(module, index):
    
    if index != 0:
        module[0] = "48NPFC100"
        module[1] = "01.11.02.00"
        module[2] = "14810082011906030010"
        module[3] = "20190603"
    else: 
        module[0] = "48NPFC100-R"
        module[1] = "01.11.02.00"
        module[2] = "148100R2002008150103"
        module[3] = "20200815"
    
    module = module[:4]
    return module   
    

def get_product_info(modules, num_modules):
    
    module_39 = [0x27,0x11,0x00,0x00,0x00,0x00,0xFA,0xCF]
    module_40 = [0x28,0x11,0x00,0x00,0x00,0x00,0xFA,0x30]
    module_41 = [0x29,0x11,0x00,0x00,0x00,0x00,0xFB,0xE1]
    module_42 = [0x2A,0x11,0x00,0x00,0x00,0x00,0xFB,0xD2]
    module_43 = [0x2B,0x11,0x00,0x00,0x00,0x00,0xFA,0x03]
    module_44 = [0x2C,0x11,0x00,0x00,0x00,0x00,0xFB,0xB4]
    module_45 = [0x2D,0x11,0x00,0x00,0x00,0x00,0xFA,0x65]
    module_46 = [0x2E,0x11,0x00,0x00,0x00,0x00,0xFA,0x56]
    modules_list = [module_39, module_40, module_41, module_42, module_43, module_44, module_45, module_46]

    module_info = []
    ser = serial.Serial('/dev/ttyUSB0')
    ser.timeout = 1
    
    index = 0
    for module in modules_list[0:num_modules - 1]:
        ser.reset_input_buffer()
        ser.write(serial.to_bytes(module))
        ser.flush()
        hexa_values = ser.read(54)
        ascii_values = hexa_values.decode("ascii")
        module = ascii_values.split("*")
        module = set_module_format(module, index)
        modules[index].set_product_info(module)
        index += 1
        
    return modules


if __name__ == "__main__":
    
    modules = get_analog_values()
    modules = get_product_info(modules, len(modules))
    
    json_string_modules = json.dumps([module.__dict__ for module in modules])
    
    print(json_string_modules)
    
