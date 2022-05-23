import socket
import connection
import time
from packet import packet

# server address and server port
serverAddress = "localhost"
serverPort = 5500
serverInfo = (serverAddress, serverPort)

# Delimiter
delimiter = "|:|:|"

def Sender():
    # AF_INET means it's for IPv4 addresses and it's in a pair like this (host, port)
    peer2Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # creating the socket. 
    # Set a timeout on blocking socket operations.
    peer2Socket.settimeout(10)
    close = 0
    part = 1
    # Connection Trials == ct
    ct = 0
    while True:
        # try:
            fileName = input("\nselect file name to send: ") # blocking operation
            with open(f"./peer2File/{fileName}.txt", "rb") as senderFile:
                bytes = senderFile.read(30) # read arbitrary number of bytes until you reach EOF "End Of File"
                pkt = packet()  # creating an Object from Packet class
                pkt.construct(bytes) # instanitating the object
                constructedPacket = str(pkt.checksum) + delimiter + str(pkt.ackNo) + delimiter + str(pkt.length) + delimiter + pkt.msg + delimiter + str(pkt.noPacket)
                peer2Socket.sendto(constructedPacket.encode(), serverInfo)
                close+=1
                while True:
                    print((f"Sending Part {part} of %s") % fileName)
                    # Receive indefinitely
                    print("\nWaiting to receive ACK\n")
                    try:
                        data, server = peer2Socket.recvfrom(550) # waiting to receive an acknowledgement
                        time.sleep(0.5) # stop the execution for half a second 
                        ct = 0
                        ackNo = data.decode().split(delimiter)[1] # ackNo, if 1 then ack+ if 0 then ack-
                        if(int(ackNo) == 1):
                            print("ACK+ received, continue...")
                            choice = False
                        else:
                            print("ACK- received, resending")
                            choice = True
                        bytes = bytes if choice else senderFile.read(30)
                        if not choice:
                            part +=1
                        if not bytes:
                            print("all data has been sent!")
                            pkt = packet()
                            pkt.construct("")
                            pkt.noPacket = 1
                            constructedPacket = str(pkt.checksum) + delimiter + str(pkt.ackNo) + delimiter + str(pkt.length) + delimiter + pkt.msg + delimiter + str(pkt.noPacket)
                            peer2Socket.sendto(constructedPacket.encode(), server if close >= 1 else serverInfo)
                            break
                        pkt = packet()
                        pkt.construct(bytes)
                        constructedPacket = str(pkt.checksum) + delimiter + str(pkt.ackNo) + delimiter + str(pkt.length) + delimiter + pkt.msg + delimiter + str(pkt.noPacket)
                        peer2Socket.sendto(constructedPacket.encode(), server if close >= 1 else serverInfo)
                    except:
                        ct+=1
                        if ct < 3:
                            print("\nConnection Timeout, retrying...")
                            continue
                        else:
                            print("Maximum Connection Trials Reached, Exiting...")
                            break
            print("Closing socket")
            peer2Socket.close() # closing the socket after we done
            break


def Receiver():
    # Starting Connection
    peer2Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # creating the socket. 
    peer2Socket.settimeout(10)
    # Bind the socket to the port
    print("Starting up on %s port %s" % serverInfo)
    peer2Socket.bind(serverInfo) # binding the socket with the address and the port in serverInfo variable

    # Listening for requests indefinitely
    while True:
        print("Waiting to receive a message")
        try:
            data, address = peer2Socket.recvfrom(550)   # blocking operation - waiting to receive a packet 
            print("Received %s bytes from %s" % (len(data.decode()), address))
            connection.connection(data.decode(), address, "peer2File", "text2") # turning the wheel of control to connection method
            choice = onOrOff() # after handling the connection do you want the server to continue to listen.
            if choice == "yes":
                continue
            print("peer2 exited...")
            break
        except Exception as e:
            print(e)
            print('Connection Timeout, retrying...')
            continue

def onOrOff():
    while True:
        choice = input("\nDo You Want to Continue listening?(yes/no) ")
        match choice.lower():
            case "yes":
                return "yes"
            case "no":
                return "no"
            case _:
                print("Please Enter yes or no")

# choosing the Role, either a sender or receiver.
while True:
    
    answer = input("Enter S --> Sender or R --> Receiver: ")
    match answer.lower():
        case "s":
            Sender()
            print("peer2 exited...")
            break
        case "r":
            Receiver()
            break
        case _:
            print('Enter S or R (only!)')