import asyncio
import logging

from notaol.p3.init import InitPayload
from notaol.p3.packet import Packet
from notaol.p3.stream import Stream


_logger = logging.getLogger(__name__)


class SequenceInfo(object):
    def __init__(self):
        self.last_transmit = 0x7f
        self.last_receive = 0x7f

    def increment_transmit(self):
        self.last_transmit += 1

        if self.last_transmit > 0x7f:
            self.last_transmit = 0x10


class Client(object):
    def __init__(self):
        self._stream = Stream()
        self._running = False
        self._read_task = None

    def close(self):
        self._stream.close()
        self._running = False

    @asyncio.coroutine
    def _read_packets(self):
        assert self._running

        while self._running:
            try:
                packet = yield from self._stream.read_packet()
            except ConnectionError:
                self._running = False
                self.close()
                raise

            # TODO: do something with packet

    @asyncio.coroutine
    def connect(self):
        _logger.info('Client connecting.')
        assert not self._running
        self._running = True
        yield from self._stream.connect()
        self._read_task = asyncio.async(self._read_packets())

        init_packet = Packet(payload=InitPayload())

        yield from self._stream.write_packet(init_packet)
