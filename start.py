from time import sleep

from e_drone.drone import *
from e_drone.protocol import *

###################

def beep(port):
    drone = Drone()
    drone = Drone()
    drone.open(port)   # 시리얼 포트 연결

    drone.sendBuzzer(BuzzerMode.Scale, BuzzerScale.C5.value, 500)   # 버저에 4옥타브 도 소리를 500ms 동안 내라고 명령하기
    sleep(1)              # 1초간 sleep

    drone.close()         # 시리얼 포트 닫기 및 내부 데이터 수신 스레드 종료

###################

def ping(port):
    drone = Drone(False)
    drone.open(port)

    drone.sendPing(DeviceType.Controller)

    timeStart = time.time()

    while True:
        sleep(0.01)
        dataType = drone.check()

        if dataType == DataType.Ack:
            ack = drone.getData(DataType.Ack)
            print("{0} / {1} / {2:04X}".format(ack.dataType.name, ack.systemTime, ack.crc16))
            print("T: {0}".format(time.time() - timeStart))
            break;

        # 1초 동안 응답이 없을 경우 응답 확인을 빠져나감
        if time.time() > timeStart + 1:
            print("Time Over (1)")
            break;

    drone.close()

###################

def firmware(port):

    drone = Drone(False)
    drone.open(port)

    drone.sendRequest(DeviceType.Controller, DataType.Information)

    timeStart = time.time()

    while True:
        sleep(0.01)
        dataType = drone.check()
        
        if dataType == DataType.Information:
            information = drone.getData(DataType.Information)
            print("ModeUpdate: {0}".format(information.modeUpdate))
            print("ModelNumber: {0}".format(information.modelNumber))
            print("Version: {0}.{1}.{2} / {3} / 0x{3:08X}".format(
                information.version.major,
                information.version.minor,
                information.version.build,
                information.version.v))
            print("Release Date: {0}.{1}.{2}".format(
                information.year,
                information.month,
                information.day))
            break

        if time.time() > timeStart + 1:
            break

    drone.close()
###################

def hovering(port):
    drone = Drone()
    drone.open(port)

    print("TakeOff")
    drone.sendTakeOff()
    for i in range(5, 0, -1):
        print("{0}".format(i))
        sleep(1)

    print("Hovering")
    for i in range(3, 0, -1):
        print("{0}".format(i))
        drone.sendControlWhile(0, 0, 0, 0, 1000)
        sleep(0.01)

    print("Go Front 1 meter")
    drone.sendControlPosition(1.0, 0, 0, 0.5, 0, 0)
    for i in range(5, 0, -1):
        print("{0}".format(i))
        sleep(0.01)


    print("Return Home")
    drone.sendFlightEvent(FlightEvent.Return)
    for i in range(5, 0, -1):
        print("{0}".format(i))
        sleep(1)

#
    drone.close()


def drone_main():
    port = 'COM8'
    print('Started Python')
    print('')

    beep(port)

    ping(port)
    
    print('')

    firmware(port)

    print('')

    hovering(port)


if __name__ == '__main__':
    drone_main()
