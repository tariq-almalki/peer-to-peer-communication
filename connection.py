import socket
import datetime
import random
from packet import packet
import hashlib
import time

# Delimiter
delimiter = "|:|:|"
# plp -> packet lose percentage


def connection(data, address, nameOfFolder, nameOfFile):
    plp = 0.2
    print("Request started at: " + str(datetime.datetime.now()))
    connectionSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    connectionSocket.settimeout(10)
    part = 1
    while True:
        randomPlp = random.random()
        if plp < randomPlp:
            if data.split(delimiter)[0] == hashlib.sha1(data.split(delimiter)[3].encode()).hexdigest():  # checking checksum
                with open(f"./{nameOfFolder}/{nameOfFile}.txt", "a") as ReceiverFile:
                    ReceiverFile.write(data.split(delimiter)[3])
                    print(f"part {part} Received!")
                    part += 1
                    pkt = packet()
                    pkt.construct("")
                    pkt.ackNo = 1
                    constructedPacket = str(pkt.checksum) + delimiter + str(pkt.ackNo) + delimiter + str(pkt.length) + delimiter + pkt.msg + delimiter + str(pkt.noPacket)
                    connectionSocket.sendto(constructedPacket.encode(), address)
                    print("------------> Sending ACK+ -------------\n")
                    try:
                        newData, server = connectionSocket.recvfrom(550)
                        time.sleep(0.5)
                        data = newData.decode()
                        address = server
                        if int(data.split(delimiter)[4]) == 1:
                            print("all data has been received!")
                            print("Closing Connection")
                            connectionSocket.close()
                            break
                    except:
                        print("Connection Timed out")
                        break
            else:
                print("---------------> Checksum Mismatch ---------> Sending ACK- --------------------\n")
                pkt = packet()
                pkt.construct("checksum mismatch")
                constructedPacket = str(pkt.checksum) + delimiter + str(pkt.ackNo) + delimiter + str(pkt.length) + delimiter + pkt.msg + delimiter + str(pkt.noPacket)
                connectionSocket.sendto(constructedPacket.encode(), address)
                newData, server = connectionSocket.recvfrom(550)
                data = newData.decode()
                address = server
        else:
            print("---------------> Dropped Packet ---------> Sending ACK- --------------------\n")
            pkt = packet()
            pkt.construct("dropped packet")
            constructedPacket = str(pkt.checksum) + delimiter + str(pkt.ackNo) + delimiter + str(pkt.length) + delimiter + pkt.msg + delimiter + str(pkt.noPacket)
            connectionSocket.sendto(constructedPacket.encode(), address)
            newData, server = connectionSocket.recvfrom(550)
            data = newData.decode()
            address = server
