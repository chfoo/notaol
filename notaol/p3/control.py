from notaol.p3.payload import BasePayload


class AckPayload(BasePayload):
    def parse(self, data):
        pass

    def __str__(self):
        return '<ACK Payload>'


class NakPayload(BasePayload):
    def parse(self, data):
        pass

    def __str__(self):
        return '<NAK Payload>'


class SSPayload(BasePayload):
    def parse(self, data):
        pass

    def __str__(self):
        return '<SS Payload>'


class SSRPayload(BasePayload):
    def parse(self, data):
        pass

    def __str__(self):
        return '<SSR Payload>'


class HeartbeatPayload(BasePayload):
    def parse(self, data):
        pass

    def __str__(self):
        return '<Heartbeat Payload>'
