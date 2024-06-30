import RPi.GPIO as GPIO

makerobo_BtnPin = 40
makerobo_Rpin = 12
makerobo_Gpin = 13
Button = 1

# 按钮初始化函数
def button_setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(makerobo_Rpin, GPIO.OUT)
    GPIO.setup(makerobo_Gpin, GPIO.OUT)
    GPIO.setup(makerobo_BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(makerobo_BtnPin, GPIO.BOTH, callback=makerobo_detect, bouncetime=200)


# 按钮检测函数，检测到按下时，打印信息
def makerobo_Print(x):
    global Button
    if x == 0:
        print("********************")
        print("* makerobo Raspberry Kit Button Pressed! *")
        print("*************************")
        Button = 0
    elif x == 1:
        print(f'Button: {Button}')
        Button = 1
        
# 按钮检测函数，对40号引脚的电平变化进行监测
def makerobo_detect(chn):
    makerobo_Print(GPIO.input(makerobo_BtnPin))
    
# 循环检测按钮状态
def makerobo_loop():
    while True:
        pass

# 清理函数   
def makerobo_destory():
    GPIO.output(makerobo_Gpin, GPIO.LOW)
    GPIO.output(makerobo_Rpin, GPIO.LOW)
    GPIO.cleanup()
    
if __name__ == "__main__":
    button_setup()
    try:
        makerobo_loop()
    except KeyboardInterrupt:
        makerobo_destory()
