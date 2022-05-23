import hashlib

# class Packet the will be generator for the objects that will travel between the sender and the receiver.
class packet:
    msg = 0
    length = 0
    checksum = 0
    ackNo = 0
    noPacket = 0

    def construct(this, data):
        this.msg = data
        this.length = str(len(data))
        this.checksum = hashlib.sha1(data.encode()).hexdigest()
