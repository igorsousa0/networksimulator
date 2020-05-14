from network.packet import Packet
from network.unreliable import UnreliableDataTransfer
from transport import checksum
import time
import random

ACK = False
Count = 0
ID = 0

class ReliableDataTransfer:

    def __init__(self, udt):
        if not isinstance(udt, UnreliableDataTransfer):
            raise Exception("udt parameter must be an instance of UnreliableDataTransfer")
        self.udt = udt

    def send(self, payload):
        global ACK,Count, ID
        packet = Packet({'payload': payload})
        packet.set_field("Pacote", ID)
        checksum.calculate_checksum(packet)
        self.udt.send(packet)
        # should wait for ACK before returning
        while(ACK == False):
            if(ACK == False):
                Count += 1
                if(ACK == True):
                    print("ACK Recebido")
                    break
                if(Count == 10):
                    print("Tempo esgotado")
                    self.udt.send(packet)
                    Count = 0
                time.sleep(1)
            else:      
                break     
        ACK = False
        ID = ID + 1    
        Count = 0     
        # if some time has passed while waiting for ACK, then it should retransmit the packet

    def receive(self):
        global ACK, Lost
        packet = self.udt.receive(timeout=100)
        if(packet is None):
            Lost = True
            print("Pacote Vazio")
            return
        else:
            # ID do Pacote Recebido
            print(packet.get_field("Pacote"))
            ACK = True
        # should wait until there's data coming from bottom layer
        valid = checksum.validate_checksum(packet)
        if valid:
            # should acknowledge sender
            return packet.get_field('payload')
        else:
            print("invalid checksum")
