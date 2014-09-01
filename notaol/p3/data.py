from notaol.p3.payload import BasePayload


class DataPayload(BasePayload):
    def __init__(self):
        self.data = None

    def parse(self, data):
        self.data = data

    def to_bytes(self):
        return self.data
