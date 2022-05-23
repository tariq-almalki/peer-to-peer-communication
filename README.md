# peer-to-peer communication

## Table of contents

-   📖 [Introduction](#introduction)
-   🐍 [Python](#python)
-   ⚙️ [Example](#example)
-   🥁 [Output](#output)
-   📌 [Conclusion](#conclusion)

---

## Introduction

In this Project I built a reliable peer-to-peer(P2P) data transfer(text files only) application using UDP protocol. Reliability ensured using checksum and acknowledgements(ACKs), for anyone that doesn’t know what are checksum or ACKs I will explain them briefly, first of let start explaining what is a checksum and what it’s used for, a checksum is a value that is used to verify the integrity of data that has been sent by the sender to the receiver, so it’s used to detect errors/changes in the file that is being transferred, now let us talk about ACKs, there is two types of ACKs, there is the positive ACK(ACK+) and there is the negative ACK(ACK-), positive ACKs is used for telling the sender that the packet has been received and negative ACKs is used for telling the sender that the packet hasn’t been received.

## Python

I tried to pick a language that is minimal, that will make it easy for me, because I got no time really, I know Three languages Java, Javascript, Python, so obviously the choice was between either Javascript or Python, I chose Python over Javascript because of the API that is used to make UDP connections, the API that comes with Node.js, is really ambiguous, and also it lacks the functions that is essential really to build reliable P2P using UDP, it was really merely designated to build UDP connections but the not reliable ones, you may ask what is Node.js, Node.js is an environment that is used to execute Javascript code in the server side, in the past Javascript was only present in the browser environment, Node.js comes with out of the box modules for writing server side apps, but we are here not for discussing what is Node.js really! Right? So the choice has to be Python. I looked up the documentation for Python and I found what I really need to build a reliable P2P app using UDP.

## Example

#### Executing `peer1.py` file

when you execute `peer1.py` file you will be get to choose between being a "Sender" or "Receiver".
![sender-or-receiver](./README%20pictures/peer_1/choosing_to_be_sender_or_Receiver.png)

then you will get to choose which "text" file you want to send.

![choosing-text-file](./README%20pictures/peer_1/peer_1_choosing_file.png)

#### Executing `peer2.py` file

here also you get to choose between being a "Sender" or "Receiver", we will choose being the "Receiver".

![sender-or-receiver](./README%20pictures/peer_2/choosing_to_be_sender_receiver.png)

now you will see that you are listening on port "5500"
and waiting for a message to receive.

![waiting-a-message](./README%20pictures/peer_2/peer_2_listening.png)

#### `connection.py` file

handling the intricacies of the connection will be delegated to this file.

it will perform two main processes.

1-checking the validity of the "checksum"
2-depending upon step 1 it will send either ACK+ or ACK- for the reasons aforementioned in the introduction.

#### `packet.py` file

this file will the contain the template of the packet object AKA "the class", blueprint you know?

I like dividing the code into modules it keeps the complexity at levels that can be controlled.

---

## Output

here is the output of what will happen if we send a text file from
peer1 as "Sender" to peer2 the "Receiver".

![pic_1](./README%20pictures/peer_1/peer_1_results.png)
![pic_2](./README%20pictures/peer_2/peer_2_results.png)

## Conclusion

throughout the process of building this project I have learned so many important concepts, for example checksums and how they work and calculated, also acknowledgments.

and also how would the receiver exploit ACKs to tell the sender that the packet is received and verified, also being able and for the first time build a reliable peer-to-peer app using User-Datagram-Protocol(UDP) with python, it was a great experience and I learned a lot.
