import time

import cv
import hall
from cv import cv_loop
from hall import hall_loop, hall_destroy, hall_setup
from LCD import LCD_loop
from buzzer import buzzer_loop, buzzer_setup, makerobo_Buzzer
import threading
import RPi.GPIO as GPIO

# cv.py在检测到人脸时，将人脸识别结果赋值给current_people变量
# hall.py在检测到门状态变化时，将门状态赋值给door变量
def detect_loop():
    buzzer_setup(makerobo_Buzzer)
    while True:
        people = cv.current_people
        d = hall.door
        time.sleep(0.5)
        print(f'Current person; {people}, Door status:{d}')
        if people != "zbc" and d:
            buzzer_loop()


if __name__ == '__main__':
    try:
        # 创建各个模块的线程
        GPIO.setmode(GPIO.BOARD)
        cv_thread = threading.Thread(target=cv_loop)
        hall_thread = threading.Thread(target=hall_loop)
        LCD_thread = threading.Thread(target=LCD_loop)
        detect_thread = threading.Thread(target=detect_loop)
        
        # 启动各个线程
        hall_setup()
        LCD_thread.start()
        cv_thread.start()
        hall_thread.start()
        detect_thread.start()

        # 等待线程结束
        cv_thread.join()
        LCD_thread.join()
        hall_thread.join()
        detect_thread.join()
    except KeyboardInterrupt:
        hall_destroy()
