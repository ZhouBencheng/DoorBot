# /usr/bin/env python
import RPi.GPIO as GPIO
import PCF8591 as ADC
import time

HallPin = 11
Gpin = 13
Rpin = 12

door = False

def hall_setup():
	ADC.setup(0x48)
	GPIO.setmode(GPIO.BOARD)  # Numbers GPIOs by physical location
	GPIO.setup(Gpin, GPIO.OUT)  # Set Green Led Pin mode to output
	GPIO.setup(Rpin, GPIO.OUT)  # Set Red Led Pin mode to output
	GPIO.setup(HallPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set BtnPin'smode is input, and pull up to high level(3.3V)
	GPIO.add_event_detect(HallPin, GPIO.BOTH, callback=detect, bouncetime=200)
	# 检测到磁场时，数字输出低电平，即GPIO.input(HallPin)==0
	# 没有检测到磁场时，数字输出高电平，即GPIO.input(HallPin)==1


def Led(x):
	if x == 0:  # 检测到磁场时，亮红灯
		GPIO.output(Rpin, 1)
		GPIO.output(Gpin, 0)
	if x == 1:  # 没有检测到磁场时，亮绿灯
		GPIO.output(Rpin, 0)
		GPIO.output(Gpin, 1)


def Print1(x):
	if x == 0:  # 检测到磁场时，数字输出低电平，x==0
		print('***********************************')
		print('*   Detected magnetic materials   *')
		print('***********************************')


def detect(chn):
	Led(GPIO.input(HallPin))
	Print1(GPIO.input(HallPin))


def Print2(x):
	global door
	if x == 1:
		print('')
		print('*************')
		print('* No Magnet *')
		print('*************')
		print('')
		door = True
	if x == 0:
		print('')
		print('*************')
		print('* Detected Magnet *')
		print('*************')
		print(" ")
		door = False


def hall_loop():
	status = 0
	while True:
		tmp = 0
		res = ADC.read(0)  # 模拟输出信号A/D转换后的数字信号值
		print('Current intensity of magnetic field : ', res)
		if res < 10:  # 这里的数字输出ADC.read(0)只有两个值，0或255
			tmp = 0  # ADC.read(0)为255时没有检测到磁场
		# ADC.read(0)为 0 时检测到磁场，但有少量误差的其它，比如1或254等值偶尔出现
		if res > 150:
			tmp = 1
		if tmp != status:
			Print2(tmp)
			status = tmp
		time.sleep(0.5)


def hall_destroy():
	GPIO.output(Gpin, GPIO.LOW)  # Green led off
	GPIO.output(Rpin, GPIO.LOW)  # Red led off
	GPIO.cleanup()  # Release resource


if __name__ == '__main__':
	hall_setup()
	try:
		hall_loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() willbe executed.
		hall_destroy()
