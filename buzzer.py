import RPi.GPIO as GPIO
import time
import button

makerobo_Buzzer = 29  # 有源蜂鸣器管脚定义

# GPIO设置函数
def buzzer_setup(pin):
    button.button_setup()
    global makerobo_BuzzerPin
    makerobo_BuzzerPin = pin
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(makerobo_BuzzerPin, GPIO.OUT)
    GPIO.output(makerobo_BuzzerPin, GPIO.HIGH)

# 蜂鸣器控制函数（响）
def up():
    GPIO.output(makerobo_BuzzerPin, GPIO.LOW)

# 蜂鸣器控制函数（不响）
def down():
    GPIO.output(makerobo_BuzzerPin, GPIO.HIGH)


def beep(x):
    up()
    time.sleep(x)
    down()
    time.sleep(x)

# 蜂鸣器循环函数，检测到按钮按下停止鸣叫
def buzzer_loop():
    while True:
        if button.Button == 0:
            print('Break out from buzzer loop')
            break
        else:
            print('Start beeping')
            beep(0.5)

# 清理函数
def destroy():
    GPIO.output(makerobo_BuzzerPin, GPIO.HIGH)
    GPIO.cleanup()


if __name__ == '__main__':
    buzzer_setup(makerobo_Buzzer)
    try:
        buzzer_loop()
    except KeyboardInterrupt:
        destroy()
