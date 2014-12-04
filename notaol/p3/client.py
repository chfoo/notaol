import asyncio
import logging

from notaol.p3.init import InitPayload
from notaol.p3.packet import Packet, PacketType
from notaol.p3.stream import Stream
from notaol.p3.control import AckPayload
from notaol.p3.data import DataPayload
from notaol.p3 import login


_logger = logging.getLogger(__name__)


class SequenceInfo(object):
    def __init__(self):
        self.transmit = 0x7f
        self.receive = 0x7f

    def increment_transmit(self):
        self.transmit += 1

        if self.transmit > 0x7f:
            self.transmit = 0x10


class Client(object):
    def __init__(self):
        self._stream = Stream()
        self._running = False
        self._read_task = None
        self._sequence_info = SequenceInfo()
        self._incoming_packet_condition = asyncio.Condition()
        self._incoming_packet = None

    def close(self):
        self._stream.close()
        self._running = False

    @asyncio.coroutine
    def _read_packets(self):
        assert self._running

        while self._running:
            try:
                packet = yield from self._stream.read_packet()
            except Exception:
                _logger.exception('Read error')
                self._running = False
                self.close()
                raise

            try:
                yield from self._process_packet(packet)
            except Exception:
                _logger.exception('Process packet error')
                raise

    @asyncio.coroutine
    def _process_packet(self, packet):
        _logger.debug('Process packet %s', packet)

        if packet.type == PacketType.heartbeat:
            _logger.debug('Reply to heartbeat')
            ack_packet = Packet(payload=AckPayload())
            yield from self._write_packet(ack_packet)
        elif packet.type == PacketType.ack:
            assert isinstance(packet.tx_seq, int)
            self._sequence_info.receive = packet.tx_seq
        else:
            _logger.debug('Unhandled packet')
            self._sequence_info.receive = packet.tx_seq

            yield from self._incoming_packet_condition.acquire()
            self._incoming_packet = packet
            self._incoming_packet_condition.notify()
            self._incoming_packet_condition.release()
            yield from asyncio.sleep(0.01)

    @asyncio.coroutine
    def connect(self):
        _logger.info('Client connecting.')
        assert not self._running
        self._running = True
        yield from self._stream.connect()
        self._read_task = asyncio.async(self._read_packets())

        init_packet = Packet(payload=InitPayload())

        yield from self._write_packet(init_packet)

        while True:
            _logger.debug('Waiting for SD token packet.')

            yield from self._incoming_packet_condition.acquire()
            yield from self._incoming_packet_condition.wait()
            packet = self._incoming_packet
            self._incoming_packet_condition.release()

            if isinstance(packet.payload, DataPayload) and \
                    packet.payload.token_str == 'SD':
                _logger.debug('Got SD token packet!')
                break
            else:
                _logger.debug('Did not get SD token packet.')

    @asyncio.coroutine
    def login(self, username, password):
        _logger.info('Client login.')

        payload = DataPayload()
        payload.token_str = 'Dd'
        payload.atom_stream = login.new_login_atom_stream(
            username, password)

        packet = Packet()
        packet.apply_payload(payload)

        yield from self._write_packet(packet)

    @asyncio.coroutine
    def _write_packet(self, packet):
        packet.tx_seq = self._sequence_info.transmit
        packet.rx_seq = self._sequence_info.receive

        yield from self._stream.write_packet(packet)

        if packet.type in (PacketType.init, PacketType.data):
            self._sequence_info.increment_transmit()
