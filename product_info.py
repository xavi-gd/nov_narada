import serial
import minimalmodbus
import time
import json

def get_product_info(number_of_active_modules):

    ser = serial.Serial('/dev/ttyUSB0')
    ser.timeout = 1

    serial_list = []
    serial_number_list = []
    model = ""
    module_39 = [0x27,0x11,0x00,0x00,0x00,0x00,0xFA,0xCF]
    module_40 = [0x28,0x11,0x00,0x00,0x00,0x00,0xFA,0x30]
    module_41 = [0x29,0x11,0x00,0x00,0x00,0x00,0xFB,0xE1]
    module_42 = [0x2A,0x11,0x00,0x00,0x00,0x00,0xFB,0xD2]
    module_43 = [0x2B,0x11,0x00,0x00,0x00,0x00,0xFA,0x03]
    module_44 = [0x2C,0x11,0x00,0x00,0x00,0x00,0xFB,0xB4]
    module_45 = [0x2D,0x11,0x00,0x00,0x00,0x00,0xFA,0x65]
    module_46 = [0x2E,0x11,0x00,0x00,0x00,0x00,0xFA,0x56]
    modules_list = [module_39, module_40, module_41, module_42, module_43, module_44, module_45, module_46]


    for module in modules_list[0:number_of_active_modules]:
        ser.reset_input_buffer()
        ser.write(serial.to_bytes(module))
        ser.flush()
        values = ser.read(54)[2:]
        print(values)
        in_ascii = values.decode("ascii")
        #print(in_ascii)
        in_ascii_list = in_ascii.split("*")
        print(in_ascii_list)

        if (in_ascii != ""):
            model = in_ascii[1:10]
            #print(model)
            serial_number = in_ascii[19:54].split("*")[1].strip()
            #print(serial_number)
            date_of_manufacture = in_ascii[19:54].split("*")[2].strip()
            #print(date_of_manufacture)
            serial_list.append([model,serial_number])
            serial_number_list.append(serial_number)
        time.sleep(0.005)
   

if __name__ == "__main__":
    
    get_product_info(2)
    
