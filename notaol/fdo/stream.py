from notaol.fdo import serialize
import io


class AtomStream(object):
    '''Atom stream.

    Attributes:
        stream_id (int): Stream ID.
        atom_protocol_id (int): Last protocol ID for this stream.
        atoms (list): A list of tuples. The first item in the tuple is
            a Atom. The remainder of the tuple is the argument.
    '''
    def __init__(self):
        self.stream_id = None
        self.atom_protocol_id = 0
        self.atoms = None

    def parse(self, data):
        self.stream_id, stream_id_bytes = serialize.unserialize_stream_id(data)
        self.atoms = []

        for item in serialize.unserialize(self.atom_protocol_id, data[len(stream_id_bytes):]):
            self.atom_protocol_id, atom_id, name, arg_length, arg = item

            self.atoms.append((name, arg))

    def to_bytes(self):
        buffer = io.BytesIO()
        buffer.write(serialize.serialize_stream_id(self.stream_id))

        for item in self.atoms:
            atom_def = item[0]
            args = item[1:]

            serialize.serialize(buffer, atom_def, *args)

        return buffer.getvalue()

    def __str__(self):
        return '<AtomStream at {} SID={} Atoms={}>'.format(
            id(self), self.stream_id, self.atoms)
