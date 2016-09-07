#! usr/bin/python

import serial

class signboard():

    def __init__(self):
        #Open & setup serial port    
        self.sp = serial.Serial("/dev/ttyUSB0", 9600)
        self.sp.setTimeout(1)
        #self.sp.flushInput()
        #self.sp.flushOutput()

    def read_serial_response(self):
        response = ''
        while True:
            char = self.sp.read(1)
            if char == '':
                break
            response += char
        print "[MCU]:", response

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
        self.sp.flush()
        self.read_serial_response()
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
        self.sp.flush()
        self.read_serial_response()
        print ""


    def clear_all(self):
        print "Running clear all command:"
        data_input = "<D*>"
        chksum = self.create_checksum(data_input)

        print "[PC]"+"<ID01>" + data_input + "%02X<E>"%(chksum)
        self.sp.write("<ID01>" + data_input + "%02X<E>"%(chksum))
        self.sp.flush()
        self.read_serial_response()
        print ""


    def first_setup(self):
        self.configureSignID()
        self.configureRTC("16","02","07","05","10","37","00")
        self.clear_all()


    def display_message(self, message, page):
        #Page Message 13 chars max

        data = "<L1><P" + page + "><Ff><MA><WB><Ff>" + message + "<CD>"
        chksum = self.create_checksum(data)

        print "[PC]"+"<ID01>" +data+ "%02X<E>"%(chksum)
        self.sp.write("<ID01>" +data+ "%02X<E>"%(chksum))
        self.sp.flush()
        self.read_serial_response()


    def schedule(self, pages_amount):
        data = "<TA>"+"1111111111"+"9912312359"+pages_amount
        chksum = self.create_checksum(data)

        print "[PC]"+"<ID01>" +data+ "%02X<E>"%(chksum)
        self.sp.write("<ID01>" +data+ "%02X<E>"%(chksum))
        self.sp.flush()
        self.read_serial_response()

    def default_run_page(self):
        data = "<RPB>"
        chksum = self.create_checksum(data)

        print "[PC]"+"<ID01>" +data+ "%02X<E>"%(chksum)
        self.sp.write("<ID01>" +data+ "%02X<E>"%(chksum))
        self.sp.flush()
        self.read_serial_response()

    def delete_schedule(self):
        data = "<DTA>"
        chksum = self.create_checksum(data)

        print "[PC]"+"<ID01>" +data+ "%02X<E>"%(chksum)
        self.sp.write("<ID01>" +data+ "%02X<E>"%(chksum))
        self.sp.flush()
        self.read_serial_response()

       

    def display_multiple_messages(self, msgs_list=[]):
        self.delete_schedule()
        page = 'A'
        pages = ''
        #max amount = 26 but could work with 31
        for msg in msgs_list:
            self.display_message(msg, page)
            print "page:",page
            pages += page
            page = chr(ord(page) + 1)
            print "pages["+pages+"]"
            print "message:", msg
            print ""
        self.schedule(pages)
        #Have to try scheduling the messages BEFORE they're actually sent out.

if __name__ == "__main__" :

    s = signboard()
    #s.first_setup()
    s.display_multiple_messages(["...","Welcome to:", "Dataplicity", "office", "Here be","Dragons"]) #Page A has to have some sort of loading indicator bacause when longer messages are sent they take time and the diplay repeats page A until schedule kicks in.
    s.close_serial()





