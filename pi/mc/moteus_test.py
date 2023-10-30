"""@package docstring
Documentation for this module

More details
"""

from MoteusException import *

# for bridge nodes sockets
import sys
import socket

from get_cpu_command import get_cpu_command
from moteus_controller import MoteusController
from send_mc_states import send_mc_states

# Get local machine name
SERVER_HOST = socket.gethostname()
CPU_SUB_SERVER_PORT = 9999
MC_SUB_SERVER_PORT = 9998


async def main(_m: MoteusController):
	# to = 3                      #0.1 seems to be the lower limit for a standalone motor. This is max torque.
	# vel = 1

	# board can sense where position 0 is via absolute encoder within 1/10 rotation this offset changes where it's zero
	# is

	# sockets:
	# 1. init socket and time out to listen to cpu_sub node
	cpu_sub_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	cpu_sub_socket.settimeout(10.0)
	# connect to server
	cpu_sub_socket.connect((SERVER_HOST, CPU_SUB_SERVER_PORT))

	# 2. inis socket and timeout to send msg to mc_sub node
	mc_sub_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	mc_sub_socket.settimeout(10.0)
	mc_sub_socket.connect((SERVER_HOST, MC_SUB_SERVER_PORT))

	# 3. init thread
	controller_task = asyncio.create_task(_m.run())
	cpu_task = asyncio.create_task(get_cpu_command(cpu_sub_socket, _m))
	mc_task = asyncio.create_task(send_mc_states(_m, mc_sub_socket))

	# # 4. run

	await asyncio.gather(controller_task, cpu_task, mc_task)

	_m.mprint(_m.get_parsed_results())


async def close_key(_m):
	await _m.close_moteus()
	_m.mprint("Moteus Closed Properly")


if __name__ == '__main__':
	m = asyncio.run(MoteusController.create(ids=[[], [], [2], [], []], simulation=False))
	try:
		asyncio.run(main(m))
	except KeyboardInterrupt:
		asyncio.run(close_key(m))
		sys.exit(0)

# to add:
# flux braking- moteus defaults to discharging voltage when braking to DC power bus
# servo.flux_brake_min_voltage and servo.flux_brake_resistance_ohm can change this
