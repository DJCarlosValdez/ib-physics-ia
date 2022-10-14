
import signal
import time
import random
import string
import argparse
import pathlib

from flask import Flask, render_template
from flask_socketio import SocketIO
import obd
import socketio


app = Flask(__name__)
socketio = SocketIO(app)

#def decodeBMS (messages):
#	return messages

#bms = OBDCommand(name: "SOC_BMS", description: "State of Charge BMS", command: b"2101", bytes: 0, header: "7E4", fast: False, decoder: decodeBMS)

#special_commands = [bms]

commands = [
	obd.commands.SPEED,
	obd.commands.THROTTLE_POS,
	obd.commands.FUEL_LEVEL,
	obd.commands.HYBRID_BATTERY_REMAINING,
	#bms
]

connection = None
file = None

def handler(signum, frame):
	if file is not None:
		file.close()
		
	msg = "Stopping OBD process"
	print(msg, end="", flush=True)
	exit(1)


def randomCode(len=4):
	choices = string.ascii_uppercase + string.digits
	return (''.join(random.choice(choices) for i in range(len)))
	

def main():
	signal.signal(signal.SIGINT, handler)
	
	parser = argparse.ArgumentParser()
	parser.add_argument("--obd-port", type=pathlib.Path, required=True)
	parser.add_argument("--refresh_rate", type=float, required=False, default=0.5)
	parser.add_argument("--baudrate", type=int, required=False, default=38400)
	args = parser.parse_args()
	
	refresh_rate = args.refresh_rate
	
	obd_port = str(args.obd_port)
	baudrate = args.baudrate
	connection = obd.OBD(obd_port, baudrate=baudrate)
	
	#for command in special_commands:
	#	connection.supported_commands.add(command)
	
	socketio.run()

	sessionID = randomCode(4)
	
	print(f"Starting OBD session: {sessionID}\n------\n")
	file = open(f"log-{sessionID}.csv","w")
	file.write("Timestamp,Command,Value\n")
		
	while True:
		for cmd in commands:
			response = connection.query(cmd)
			response_value = str(response.value)
			print(f"{cmd.name}: {response_value}")
			file.write(f"{time.time()},{cmd.name},{response_value}\n")
			
		time.sleep(refresh_rate)
	
	
if __name__ == "__main__":
	main()
	