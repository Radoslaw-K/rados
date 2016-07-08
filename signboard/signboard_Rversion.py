#! usr/bin/python

import serial

class signboard():

    def __init__(self):
        #Open & setup serial port    
        self.sp = serial.Serial("/dev/ttyUSB0", 9600)
        self.sp.close()
        self.sp.open()
        self.sp.setTimeout(1)
    
    def read_serial_response(self, num_of_chars_to_read):
        response = ''
        for i in range(num_of_chars_to_read):
            response += self.sp.read()
        print "[MCU]:",response

    def close_serial(self):
        self.sp.close()

    def create_checksum(self, data):
        chksum = 0
        for c in data :
            chksum ^= ord(c)
        return chksum


    def configureSignID(self):
        print "Signboard ID configuration:"
        print "[PC]"+"<ID><01><E>"
        self.sp.write("<ID><01><E>")
        self.read_serial_response(2)
        print ""


    def configureRTC(self, year, dayofweek, month, day, hour, minute, second):
        '''
        Example:
            year="16"         #2016
            dayofweek="01"    #01= monday  -> 07= sunday
            month="07"        #01= january -> 12= december
            day="04"          #01 -> 31
            hour="11"         #00 -> 23
            minute="50"       #00 -> 59
            second="00"       #00 -> 59

        notes:
            1. arguments need to be passed as strings
            2. zeros are essential e.g. "07" must be passed instead of "7"
        '''
        
        print "Real Time Clock configuration:"
        data_input = "<SC>" + year + dayofweek + month + day + hour + minute + second
        chksum = self.create_checksum(data_input)

        print "[PC]"+"<ID01>" + data_input + "%02X<E>"%(chksum)
        self.sp.write("<ID01>" + data_input + "%02X<E>"%(chksum))
        self.read_serial_response(4)
        print ""


    def clear_all(self):
        print "Running clear all command:"
        data_input = "<D*>"
        chksum = self.create_checksum(data_input)
        
        print "[PC]"+"<ID01>" + data_input + "%02X<E>"%(chksum)
        self.sp.write("<ID01>" + data_input + "%02X<E>"%(chksum))
        self.read_serial_response(4)
        print ""


    def first_setup(self):
        self.configureSignID()
        self.configureRTC("16","02","07","05","10","37","00")
        self.clear_all()
        

    def display_message(self, message):
        #Page Message 13 chars max
        
        data = "<L1><PA><Ff><MA><WB><Ff>" + message + "<CD>"
        chksum = self.create_checksum(data)

        print "[PC]"+"<ID01>" +data+ "%02X<E>"%(chksum)
        self.sp.write("<ID01>" +data+ "%02X<E>"%(chksum))
        self.read_serial_response(4)

    

if __name__ == "__main__" :
    print "I'M MAIN"
    
    s = signboard()
    s.display_message("Type message")
    s.close_serial()


