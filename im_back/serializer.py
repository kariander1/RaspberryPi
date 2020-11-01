import serial

serial_port = 9600
serial_port_name ='/dev/ttyUSB0'

int_encode = b'2'
float_encode = b'42.3'

ser = serial.Serial(serial_port_name, serial_port)
#ser.write("CO 0 0".encode())
while 1: 
    if(ser.in_waiting >0):
        line = ser.readline()
        print(line)
    else:    
        serial_string=input("Enter serial encode: ")
        ser.write(serial_string.encode())
    