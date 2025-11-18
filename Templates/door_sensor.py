import RPi.GPIO as GPIO
import time

# 핀 번호 정의
TRIG1 = 24
ECHO1 = 23
TRIG2 = 20
ECHO2 = 21

def setup():
    GPIO.setmode(GPIO.BCM)
    for trig, echo in [(TRIG1, ECHO1), (TRIG2, ECHO2)]:
        GPIO.setup(trig, GPIO.OUT)
        GPIO.setup(echo, GPIO.IN)
        GPIO.output(trig, GPIO.LOW)
    time.sleep(2)

def get_distance(TRIG, ECHO):
    # 초음파 송신 준비
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # Echo 신호 수신
    while GPIO.input(ECHO) == 0:
        start = time.time()
    while GPIO.input(ECHO) == 1:
        stop = time.time()
    # 거리 계산
    elapsed = stop - start
    dist = (elapsed * 34300) / 2  # cm
    return dist

def main():
    setup()
    print("시작합니다. Ctrl+C로 종료.")
    try:
        while True:
            dist1 = get_distance(TRIG1, ECHO1)
            dist2 = get_distance(TRIG2, ECHO2)
            print(f"dist1: {dist1:.2f}cm, dist2: {dist2:.2f}cm")
            # 임계값: 15cm 미만이면 감지
            if dist1 < 15 and dist2 > 15:
                print("입장 감지!")
                time.sleep(1)
            elif dist2 < 15 and dist1 > 15:
                print("퇴장 감지!")
                time.sleep(1)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("종료합니다.")
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()

