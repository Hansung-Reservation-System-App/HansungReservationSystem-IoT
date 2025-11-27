import RPi.GPIO as GPIO
import time

# 핀 번호 정의
TRIG1 = 24  # 입장 센서
ECHO1 = 23
TRIG2 = 20  # 퇴장 센서
ECHO2 = 21

def setup():
    GPIO.setmode(GPIO.BCM)
    for trig, echo in [(TRIG1, ECHO1), (TRIG2, ECHO2)]:
        GPIO.setup(trig, GPIO.OUT)
        GPIO.setup(echo, GPIO.IN)
        GPIO.output(trig, GPIO.LOW)
    time.sleep(2)

def get_distance(TRIG, ECHO):
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    start = time.time()
    stop = time.time()
    timeout = time.time() + 1
    while GPIO.input(ECHO) == 0:
        start = time.time()
        if time.time() > timeout:
            return 999  # 아주 먼 거리로 반환
    while GPIO.input(ECHO) == 1:
        stop = time.time()
        if time.time() > timeout:
            return 999
    elapsed = stop - start
    dist = (elapsed * 34300) / 2  # cm
    return dist

def main():
    setup()
    print("시작합니다. Ctrl+C로 종료.")
    count = 0

    try:
        while True:
            dist1 = get_distance(TRIG1, ECHO1)
            dist2 = get_distance(TRIG2, ECHO2)

            # 입장: 센서1에 물체가 접근(거리 15cm 이하)
            if dist1 < 10:
                count += 1
                print(f"입장 감지! 현재 혼잡도(인원): {count}")
                time.sleep(1)  # 중복입장 방지

            # 퇴장: 센서2에 물체가 접근(거리 15cm 이하)
            if dist2 < 15:
                count = max(0, count - 1)
                print(f"퇴장 감지! 현재 혼잡도(인원): {count}")
                time.sleep(1)  # 중복퇴장 방지

            time.sleep(0.1)
    except KeyboardInterrupt:
        print("종료합니다.")
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()

