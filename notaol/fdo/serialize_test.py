import codecs
import io
import unittest

from notaol.fdo.atomdef import Atom, AtomProtocol
from notaol.fdo.serialize import unserialize, serialize, unserialize_stream_id, \
    serialize_stream_id


class TestSerialize(unittest.TestCase):
    def test_unserialize(self):
        # Dd token sent from client
        data = codecs.decode(b'0016000100010a0400000001010b040000000503010a61736466202020202020011d00011d00010a040000000203010950617373576f726431011d00010a0400000010010b0400000001011d00011d00000200', 'hex')
        stream_id, stream_id_bytes = unserialize_stream_id(data)
        data = data[len(stream_id_bytes):]
        atoms = unserialize(data)
        atoms = tuple(atoms)

        atom_protocol_id, atom_id, name, arg_length, arg = atoms[0]
        self.assertEqual(AtomProtocol.UNI, atom_protocol_id)
        self.assertEqual(Atom.uni_start_stream, name)

        atom_protocol_id, atom_id, name, arg_length, arg = atoms[3]
        self.assertEqual(AtomProtocol.DE, atom_protocol_id)
        self.assertEqual(Atom.de_data, name)
        self.assertEqual(b'asdf      ', arg)

        atom_protocol_id, atom_id, name, arg_length, arg = atoms[7]
        self.assertEqual(AtomProtocol.DE, atom_protocol_id)
        self.assertEqual(Atom.de_data, name)
        self.assertEqual(b'PassWord1', arg)

        atom_protocol_id, atom_id, name, arg_length, arg = atoms[13]
        self.assertEqual(AtomProtocol.UNI, atom_protocol_id)
        self.assertEqual(Atom.uni_end_stream, name)

    def test_serialize(self):
        # Dd token sent from client
        payload_file = io.BytesIO()
        payload_file.write(serialize_stream_id(0x16))
        serialize(payload_file, Atom.uni_start_stream)
        serialize(payload_file, Atom.man_set_context_relative, 1)
        serialize(payload_file, Atom.man_set_context_index, 5)
        serialize(payload_file, Atom.de_data, b'asdf      ')
        serialize(payload_file, Atom.man_end_context)
        serialize(payload_file, Atom.man_end_context)
        serialize(payload_file, Atom.man_set_context_relative, 2)
        serialize(payload_file, Atom.de_data, b'PassWord1')
        serialize(payload_file, Atom.man_end_context)
        serialize(payload_file, Atom.man_set_context_relative, 16)
        serialize(payload_file, Atom.man_set_context_index, 1)
        serialize(payload_file, Atom.man_end_context)
        serialize(payload_file, Atom.man_end_context)
        serialize(payload_file, Atom.uni_end_stream)

        good = codecs.decode(b'0016000100010a0400000001010b040000000503010a61736466202020202020011d00011d00010a040000000203010950617373576f726431011d00010a0400000010010b0400000001011d00011d00000200', 'hex')
        result = payload_file.getvalue()
        print(good)
        print(result)
        self.assertEqual(good, result)
