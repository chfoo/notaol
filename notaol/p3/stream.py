import asyncio
import logging

from notaol.p3.packet import Packet, HEADER_LENGTH, HEADER_SIZE_OFFSET


_logger = logging.getLogger(__name__)


class Stream(object):
    '''Connection handler.'''
    def __init__(self, host='AmericaOnline.aol.com', port='5190'):
        self._host = host
        self._port = port

        self._reader = None
        self._writer = None

    def closed(self):
        '''Return whether the connection is closed.'''
        return not self._reader or self._reader.is_eof()

    def close(self):
        '''Close the connection.'''
        if self._reader:
            _logger.debug('Close connection.')
            self._reader = None
            self._writer.close()
            self._writer = None

    @asyncio.coroutine
    def connect(self):
        '''Connect to the service.

        Coroutine.
        '''
        _logger.debug('Connect.')
        self._reader, self._writer = yield from asyncio.open_connection(
            self._host, self._port)
        _logger.debug('Connected.')

    @asyncio.coroutine
    def write_packet(self, packet):
        '''Send a packet.

        Coroutine.
        '''
        _logger.debug('Write packet %s', packet)
        self._writer.write(packet.to_bytes())

        yield from self._writer.drain()

    @asyncio.coroutine
    def read_packet(self):
        '''Receive a packet.'''
        _logger.debug('Begin read packet.')

        packet = Packet()
        header = yield from self._reader.readexactly(HEADER_LENGTH)

        packet.parse_header(header)
        _logger.debug('Got header %s', packet)

        # header is 8 bytes + data + stop byte
        bytes_to_read = packet.length - HEADER_SIZE_OFFSET + 1

        _logger.debug('Need to read %d bytes', bytes_to_read)

        data = yield from self._reader.readexactly(bytes_to_read)

        packet.parse_body(data)

        _logger.debug('Got packet %s', packet)

        return packet
