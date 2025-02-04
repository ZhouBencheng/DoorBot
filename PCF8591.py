import smbus
import time

bus = smbus.SMBus(1)


def setup(Addr):
	global address
	address = Addr


def read(chn):
	try:
		if chn == 0:
			bus.write_byte(address, 0x40)
		if chn == 1:
			bus.write_byte(address, 0x41)
		if chn == 2:
			bus.write_byte(address, 0x42)
		if chn == 3:
			bus.write_byte(address, 0x43)
		bus.read_byte(address)
	except Exception as e:
		print(f"Address: {address}, exception: {e}")
	return bus.read_byte(address)


def write(val):
	try:
		temp = int(val)
		bus.write_byte_data(address, 0x40, temp)
	except Exception as e:
		print(f"Exception: {e}")
