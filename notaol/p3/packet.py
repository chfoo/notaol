'''Message format.'''
import struct
import enum
from notaol.p3.init import InitData


HEADER_FORMAT = '!cHHBBB'
PACKET_START = b'\x5a'
PACKET_END = b'\r'


class PacketType(enum.IntEnum):
    init = 0x23
    '''Force initialization of communication. Send by client.'''

    ack = 0x24
    '''Null message.'''

    ss = 0x21
    '''Request an SSR.'''

    ssr = 0x22
    '''Response to an SS. Reply with missing messages.'''

    nak = 0x25
    '''Bad message was received.'''

    data = 0x20
    '''Message packet.'''

    heartbeat = 0x26
    '''Heartbeat. Reply with ACK.'''


class Packet(object):
    '''A message in the P3 protocol.

    This class handles messages with the 8-byte header.

    Attributes:
        sync (bytes): 1 byte. Indicates start of packet.
        crc (int): 2 bytes. 16 bit CRC.
        length (int): 2 bytes. Size of the data.
        tx_seq (int): 1 byte. The transmission sequence number.
        rx_seq (int): 1 byte. The receive sequence number.
        type_flag (int): 1 byte. The type of this message packet. The most
            significant bit is always set.
        data (bytes): The data which the packet encapsulates.
        stop (bytes): 1 byte. The end of the packet.
        type (int): The actual value of the :attr:`type_flag`
        payload: Object representing the :attr:`data`.
    '''
    header_struct = struct.Struct(HEADER_FORMAT)

    def __init__(self):
        self.sync = PACKET_START
        self.crc = None
        self.length = None
        self.tx_seq = None
        self.rx_seq = None
        self.type_flag = None
        self.data = None
        self.stop = PACKET_END
        self.payload = None

    @property
    def type(self):
        return self.type_flag & 0x7F

    @type.setter
    def type(self, type_val):
        self.type_flag = type_val | 0x80

    def __str__(self):
        return '<Packet at {obj_id} Len={length} Tx={tx} Rx={rx} Type={type}>'\
               .format(obj_id=id(self), length=self.length,
                       tx=self.tx_seq, rx=self.rx_seq,
                       type=self.type)

    def parse_header(self, data):
        '''Parse the 8-byte header.'''
        results = self.header_struct.unpack(data)
        self.sync = results[0]
        self.crc = results[1]
        self.length = results[2]
        self.tx_seq = results[3]
        self.rx_seq = results[4]
        self.type = results[5]

    def parse(self, data):
        self.parse_header(data[:8])
        self.data = data[8:-1]
        self.stop = data[-1:]
        self.data_to_payload()

    def header_to_bytes(self):
        '''Return the 12-byte header.'''
        return self.header_struct.pack(
            self.sync, self.crc, self.length,
            self.tx_seq, self.rx_seq, self.type_flag
            )

    def data_to_payload(self):
        if self.type == PacketType.init:
            self.payload = InitData()
            self.payload.parse(self.data)
        else:
            raise Exception('Unhandled data type')

    def payload_to_data(self):
        self.data = self.payload.to_bytes()

    def to_bytes(self):
        return self.header_to_bytes() + self.payload.to_bytes() + self.stop
