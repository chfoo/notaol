import unittest

from notaol.p3.packet import Packet, PacketType
import codecs


SAMPLE_INIT_HEADER = codecs.decode(b'5aedd800377f7fa3', 'hex')
SAMPLE_INIT_PACKET = codecs.decode(b'5ab35f00377f7fa3039d116180000000050f00001fb4b53ec00014d1032000000000040a0000014b070504ffff0000000000fffec8f718000001b2070d', 'hex')


class TestPacket(unittest.TestCase):
    def test_header_parse_header(self):
        packet = Packet()
        packet.parse_header(SAMPLE_INIT_HEADER)

        print(packet)

        self.assertEqual(b'\x5a', packet.sync)
        self.assertEqual(60888, packet.crc)
        self.assertEqual(55, packet.length)
        self.assertEqual(0x7f, packet.tx_seq)
        self.assertEqual(0x7f, packet.rx_seq)
        self.assertEqual(PacketType.init, packet.type)

        self.assertEqual(SAMPLE_INIT_HEADER, packet.header_to_bytes())

    def test_parse_init(self):
        packet = Packet()
        packet.parse(SAMPLE_INIT_PACKET)

        self.assertEqual(157 << 8 | 17, packet.payload.client_version)
        self.assertEqual(SAMPLE_INIT_PACKET, packet.to_bytes())

    def test_length(self):
        packet = Packet()
        packet.parse(SAMPLE_INIT_PACKET)

        packet.compute_length()
        self.assertEqual(55, packet.length)

        packet.data = b''
        packet.compute_length()
        self.assertEqual(3, packet.length)

    def test_checksum(self):
        packet = Packet()
        packet.parse(SAMPLE_INIT_PACKET)

        packet.payload_to_data()
        packet.compute_checksum()
        self.assertEqual(0xb35f, packet.crc)
