# Code by Pedro Henrique
# 11/05/2016
#
# Handshake Serial Port Monitor/Scanner
# After a successful connection it works as a one-way - computer to device or device to computer - terminal too
#
# v1.1 alpha
#

import sys
import time
import glob
import serial
from array import array

def serial_ports():
	# lists serial port names for both win32 and linux operating systems
	#
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
		# this excludes your current terminal "/dev/tty"
		#
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('*** UNSUPPORTED PLATFORM!')

    result = []
    for port in ports:
        try:
            ser = serial.Serial(port)
            ser.close()
            result.append(port)
        except:
            pass
    return result


def run():
	connected = False
	port_id = ""
	interaction_mode = ""
	baud_rate = ""
	handshake_char = ""
	# set interaction mode with the serial port
	#
	while interaction_mode is not "0" and interaction_mode is not "1":
		interaction_mode = raw_input("\n0 - RECEIVE-ONLY\n1 - TRANSMIT-ONLY\n> ")
	# set device baud rate here
	#
	while not baud_rate.isdigit():
		baud_rate = raw_input("\nBAUD RATE\n> ")
	# set the handshake char here
	#
	handshake_char = raw_input("\nHANDSHAKE CHARACTER\n> ")

	print("\nScanning . . ")
	# infinite loop runs the program forever
	#
	while True:
		# if there is no device connected the program will retry for connection each second, listing all avaiable serial ports
		# raises exception on any connection interruption and makes the program retry device discovering
		#
		# the program will connect to all the available waiting for the assignature handshaking byte
		# raises exception on each failed avaiable serial port handshaking trying the same thing with the next avaiable serial port of the list and/or begin all the process again
		#
		while not connected:
			time.sleep(1)
			print(".")
			for port in serial_ports():
				if not connected:
					try:
						ser = serial.Serial(port, int(baud_rate))
						char = ser.read()
						if (char == handshake_char):
							print("*** CONNECTED ***\n(at "+port+" port)\n")
							if interaction_mode == "0":
								print("\nINPUT RECEIVED\n")
							elif interaction_mode == "1":
								print("\nTYPE INPUT\n")
							connected = True
							port_id = port
					except:
						pass
		try:
			while connected:
				if interaction_mode == "0":
					s = ser.read()
					sys.stdout.write(s)
				elif interaction_mode == "1":
					# here we can set any kind of input to be streamed to the serial port
					#
					s = raw_input()
					ser.write(array("B",s))
		except:
			connected = False
			port_id = ""
			ser.close()
			print("*** DISCONNECTED ***\nScanning . . ")




if __name__ == '__main__':
	run()