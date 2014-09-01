'''Message format.'''
import enum
import struct

import crcmod

from notaol.p3.control import AckPayload, HeartbeatPayload, SSPayload, \
    SSRPayload, NakPayload
from notaol.p3.data import DataPayload
from notaol.p3.init import InitPayload


HEADER_FORMAT = '!cHHBBB'
PACKET_START = b'\x5a'
PACKET_END = b'\r'
HEADER_LENGTH = 8
HEADER_SIZE_OFFSET = 3


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


PAYLOAD_MAP = {
    PacketType.ack: AckPayload,
    PacketType.ss: SSPayload,
    PacketType.ssr: SSRPayload,
    PacketType.nak: NakPayload,
    PacketType.init: InitPayload,
    PacketType.data: DataPayload,
    PacketType.heartbeat: HeartbeatPayload,
}
PAYLOAD_TO_TYPE_MAP = dict([
    (payload, value) for value, payload in PAYLOAD_MAP.items()])


class Packet(object):
    '''A message in the P3 protocol.

    This class handles messages with the 8-byte header.

    Attributes:
        sync (bytes): 1 byte. Indicates start of packet.
        crc (int): 2 bytes. 16 bit CRC.
        length (int): 2 bytes. Size of the data including sequence numbers and
            type flags.
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
    crc_func = crcmod.predefined.mkPredefinedCrcFun('crc-16')

    def __init__(self, payload=None):
        self.sync = PACKET_START
        self.crc = 0
        self.length = 3
        self.tx_seq = 0x7f
        self.rx_seq = 0x7f
        self.type_flag = None
        self.data = None
        self.stop = PACKET_END
        self.payload = None

        if payload is not None:
            self.apply_payload(payload)

    @property
    def type(self):
        return self.type_flag & 0x7F

    @type.setter
    def type(self, type_val):
        self.type_flag = type_val | 0x80

    def __str__(self):
        return ('<Packet at {obj_id} Len={length} Tx=0x{tx:x} Rx=0x{rx:x} '
                'Type=0x{type:x} Payload={payload}>'
                ).format(obj_id=id(self), length=self.length,
                         tx=self.tx_seq, rx=self.rx_seq,
                         type=self.type, payload=self.payload)

    def parse_header(self, data):
        '''Parse the 8-byte header.'''
        results = self.header_struct.unpack(data)
        self.sync = results[0]
        self.crc = results[1]
        self.length = results[2]
        self.tx_seq = results[3]
        self.rx_seq = results[4]
        self.type = results[5]

    def parse_body(self, data):
        '''Parse data after the header including the end stop marker.'''
        self.data = data[:-1]
        self.stop = data[-1:]
        self.data_to_payload()

    def parse(self, data):
        '''Parse a complete packet including the end stop marker.'''
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
        '''Parse the data for the payload object.'''
        payload_class = PAYLOAD_MAP.get(self.type)

        if payload_class:
            self.payload = payload_class()
            self.payload.parse(self.data)
        else:
            raise Exception('Unhandled data type')

    def payload_to_data(self):
        '''Convert the payload object to bytes and apply it.'''
        self.data = self.payload.to_bytes()

    def compute_length(self):
        '''Compute length field and apply it.'''
        self.length = len(self.data) + HEADER_SIZE_OFFSET

    def compute_checksum(self):
        '''Compute and apply the checksum.'''
        data = self.to_bytes()[3:-1]

        self.crc = Packet.crc_func(data)

    def to_bytes(self):
        '''Return the packet as bytes.'''
        return self.header_to_bytes() + self.data + self.stop

    def prepare(self):
        '''Prepare the packet for transmission.'''
        self.payload_to_data()
        self.compute_length()
        self.compute_checksum()

    def apply_payload(self, payload):
        '''Apply the payload.'''
        self.payload = payload
        self.type = PAYLOAD_TO_TYPE_MAP[type(payload)]
        self.prepare()
