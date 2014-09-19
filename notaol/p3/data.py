import logging

from notaol.fdo.stream import AtomStream
from notaol.fdo.token import TOKEN_TO_DESC_MAP
from notaol.p3.payload import BasePayload


_logger = logging.getLogger(__name__)


class DataPayload(BasePayload):
    '''FDO 91 Atom messages.

    Attributes:
        token (bytes): 2 bytes. The type of atom message.
        data (bytes): The payload bytes of the atom message.
        token_str (str): The token expressed as a string.
        atom_stream (AtomStream): The atom stream.
    '''
    def __init__(self):
        self.token = None
        self.data = None
        self.atom_stream = None

    @property
    def token_str(self):
        return self.token.decode('latin-1')

    @token_str.setter
    def token_str(self, token):
        self.token = token.encode('latin-1')

    def parse(self, data):
        self.token = data[:2]
        self.data = data[2:]

        self.atom_stream = AtomStream()
        try:
            self.atom_stream.parse(data[2:])
        except Exception:
            _logger.exception('Error parsing atom stream.')
            self.atom_stream = None

    def to_bytes(self):
        if self.atom_stream:
            self.data = self.atom_stream.to_bytes()

        return self.token + self.data

    def __str__(self):
        token_desc = TOKEN_TO_DESC_MAP.get(self.token_str)

        if token_desc:
            token_text = '{} ({})'.format(self.token_str, token_desc)
        else:
            token_text = self.token_str

        if self.atom_stream:
            return '<Data Payload Token={} AtomStream={}>'.format(
                token_text, self.atom_stream)
        else:
            return '<Data Payload Token={}>'.format(token_text)
