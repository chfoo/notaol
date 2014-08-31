import asyncio
import logging

from notaol.p3.client import Client


_logger = logging.getLogger(__name__)


class RPCServer(object):
    def __init__(self, reader, writer):
        self._reader = reader
        self._writer = writer
        self._client = Client()

    @asyncio.coroutine
    def run(self):
        _logger.info('RPC session started on port %s',
                     self._writer.get_extra_info('sockname'))
        yield from self._client.connect()

        while True:
            packet = yield from self._client._receive_queue.get()

            self._writer.write(str(packet).encode())


@asyncio.coroutine
def session(reader, writer):
    server = RPCServer(reader, writer)
    yield from server.run()


def run_server():
    event_loop = asyncio.get_event_loop()
    handle = event_loop.run_until_complete(asyncio.start_server(session, port=5000))
    event_loop.run_forever()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    run_server()
