from notaol.fdo.stream import AtomStream
from notaol.fdo.atomdef import Atom


def new_login_atom_stream(username, password):
    assert len(username) <= 10

    atom_stream = AtomStream()
    atom_stream.stream_id = 0x16
    atom_stream.atoms = [
        (Atom.uni_start_stream,),
        (Atom.man_set_context_relative, 1),
        (Atom.man_set_context_index, 5),
        (Atom.de_data, username.ljust(10).encode('ascii')),
        (Atom.man_end_context,),
        (Atom.man_end_context,),
        (Atom.man_set_context_relative, 2),
        (Atom.de_data, password.encode('ascii')),
        (Atom.man_end_context,),
        (Atom.man_set_context_relative, 16),
        (Atom.man_set_context_index, 1),
        (Atom.man_end_context,),
        (Atom.man_end_context,),
        (Atom.uni_end_stream,),
    ]

    return atom_stream
