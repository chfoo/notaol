from notaol.p3.payload import BasePayload


class EmptyPayload(BasePayload):
    def parse(self, data):
        pass

    def to_bytes(self):
        return b''


class AckPayload(EmptyPayload):
    def __str__(self):
        return '<ACK Payload>'


class NakPayload(EmptyPayload):
    def __str__(self):
        return '<NAK Payload>'


class SSPayload(EmptyPayload):
    def __str__(self):
        return '<SS Payload>'


class SSRPayload(EmptyPayload):
    def __str__(self):
        return '<SSR Payload>'


class HeartbeatPayload(EmptyPayload):
    def __str__(self):
        return '<Heartbeat Payload>'
