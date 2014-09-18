import unittest
from notaol.fdo.serialize import unserialize
import codecs
from notaol.fdo.atomdef import Atom, AtomProtocol


class TestSerialize(unittest.TestCase):
    def test_unserialize(self):
        # Dd token sent from client
        atoms = unserialize(codecs.decode(b'0016000100010a0400000001010b040000000503010a61736466202020202020011d00011d00010a040000000203010950617373576f726431011d00010a0400000010010b0400000001011d00011d00000200', 'hex'))
        atoms = tuple(atoms)

        atom_protocol_id, atom_id, name, arg_length, arg = atoms[0]
        self.assertEqual(AtomProtocol.UNI, atom_protocol_id)
        self.assertEqual(Atom.uni_start_stream, name)

        atom_protocol_id, atom_id, name, arg_length, arg = atoms[3]
        self.assertEqual(AtomProtocol.DE, atom_protocol_id)
        self.assertEqual(Atom.de_data, name)
        self.assertEqual('asdf', arg)

        atom_protocol_id, atom_id, name, arg_length, arg = atoms[7]
        self.assertEqual(AtomProtocol.DE, atom_protocol_id)
        self.assertEqual(Atom.de_data, name)
        self.assertEqual('PassWord1', arg)

        atom_protocol_id, atom_id, name, arg_length, arg = atoms[13]
        self.assertEqual(AtomProtocol.UNI, atom_protocol_id)
        self.assertEqual(Atom.uni_end_stream, name)
