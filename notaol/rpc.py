import asyncio
import json
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

        command_map = {
            'connect': self._connect
        }

        while True:
            line = yield from self._reader.readline()

            if not line.endswith(b'\n'):
                self._close()
                break

            try:
                request = json.loads(line.decode('utf-8'))
            except ValueError:
                yield from self._reply(
                    {'status': 'error', 'reason': 'syntax error'})
                continue

            if 'command' not in request:
                yield from self._reply(
                    {'status': 'error', 'reason': 'missing command'})
                continue

            command = command_map.get(request['command'])

            if command:
                yield from command(request)
            else:
                yield from self._reply(
                    {'status': 'error', 'reason': 'unknown command'})

        _logger.info('RPC session ended on port %s',
                     self._writer.get_extra_info('sockname'))

    @asyncio.coroutine
    def _reply(self, response):
        self._writer.write(json.dumps(response).encode('utf-8'))
        self._writer.write(b'\n')
        yield from self._writer.drain()

    @asyncio.coroutine
    def _connect(self, request):
        username = request['username']
        password = request['password']

        yield from self._client.connect()
        yield from self._client.login(username, password)

    def _close(self):
        self._writer.close()
        self._client.close()


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
