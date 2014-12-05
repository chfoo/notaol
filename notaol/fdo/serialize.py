import enum
import struct

import notaol.fdo.stream

from notaol.fdo.atomdatatype import AtomDataType
from notaol.fdo.datatype import DataType
from notaol.fdo.atomdef import Atom


class AtomTypeComp(enum.IntEnum):
    no_comp = 0
    length_comp = 1
    data_comp = 2
    atom_noarg_comp = 3
    atom_comp = 4
    zero_comp = 5
    one_comp = 6
    extended = 7


def get_atom_type(num):
    # TODO: figure out what this means
    return num >> 5


def get_atom_value(num):
    # TODO: figure out what this means
    return num & 0x1f


def unserialize(last_protocol_id, data):
    index = 0

    while index < len(data):
        atom_protocol_add = 0
        atom_add = 0

        while (get_atom_type(data[index]) == AtomTypeComp.extended):
            atom_protocol_add += (data[index] & 0x18) << 2
            atom_add += (data[index] & 0x06) << 4
            index += 1

        atom_type = get_atom_type(data[index])

#         print(' ', AtomTypeComp(atom_type))

        if atom_type == AtomTypeComp.no_comp:
            atom_protocol_id = get_atom_value(data[index])
            index += 1
            atom_id = data[index]
            index += 1
            arg_length = data[index]
            index += 1
            arg = data[index:index + arg_length]
            index += arg_length
        elif atom_type == AtomTypeComp.length_comp:
            atom_protocol_id = get_atom_value(data[index])
            index += 1
            atom_id = get_atom_value(data[index])
            arg_length = get_atom_type(data[index])
            index += 1
            arg = data[index:index + arg_length]
            index += arg_length
        elif atom_type == AtomTypeComp.data_comp:
            atom_protocol_id = get_atom_value(data[index])
            index += 1
            atom_id = get_atom_value(data[index])
            arg_length = 1
            arg = get_atom_type(data[index])
            index += 1
        elif atom_type == AtomTypeComp.atom_noarg_comp:
            atom_protocol_id = last_protocol_id
            atom_id = get_atom_value(data[index])
            index += 1
            arg_length = 0
            arg = None
        elif atom_type == AtomTypeComp.atom_comp:
            atom_protocol_id = last_protocol_id
            atom_id = get_atom_value(data[index])
            index += 1
            arg_length = data[index]
            index += 1
            arg = data[index:index + arg_length]
            index += arg_length
        elif atom_type == AtomTypeComp.zero_comp:
            atom_protocol_id = last_protocol_id
            atom_id = get_atom_value(data[index])
            index += 1
            arg_length = 1
            arg = 0
        elif atom_type == AtomTypeComp.one_comp:
            atom_protocol_id = last_protocol_id
            atom_id = get_atom_value(data[index])
            index += 1
            arg_length = 1
            arg = 1

        atom_protocol_id += atom_protocol_add
        atom_id += atom_add
        last_protocol_id = atom_protocol_id

        try:
            atom_def = Atom((atom_protocol_id, atom_id))
            data_type = getattr(AtomDataType, atom_def.name)
        except ValueError:
            atom_def = '(unknown atom)'
            data_type = None

#         print(atom_protocol_id, atom_id, atom_def, arg_length, arg)
        
        if data_type == DataType.stream:
            atom_stream = notaol.fdo.stream.AtomStream()
            atom_stream.parse(arg)

        yield (atom_protocol_id, atom_id, atom_def, arg_length, arg)


def serialize(file, atom_def, *args):
    atom_type_id, atom_sub_id = atom_def

    if atom_type_id > 32 or atom_sub_id > 32:
        # Extended byte
        byte_num = 0xe0
        byte_num |= (atom_type_id & 0x60) >> 2
        byte_num |= (atom_sub_id & 0x60) >> 4

        file.write(bytes([byte_num]))

    file.write(bytes([atom_type_id & 0x1f, atom_sub_id & 0x1f]))

    for arg in args:
        data_type = getattr(AtomDataType, atom_def.name)

        if data_type == DataType.dword:
            arg_len = 4
            data = struct.pack('!I', arg)
        elif data_type == DataType.str:
            arg_len = len(arg)
            data = arg
        elif data_type == DataType.word:
            arg_len = 2
            data = struct.pack('!H', arg)
        else:
            raise Exception('unhandled data type {}'.format(data_type))

        assert len(data) == arg_len
        file.write(bytes([arg_len]))

        if arg_len:
            file.write(data)

    if not args:
        file.write(b'\x00')


def unserialize_stream_id(data):
    # FIXME: this is bogus!
    stream_id = 0
    length = 0
    for index, byte_value in zip(range(len(data)), data):
        stream_id <<= 8
        stream_id |= byte_value
        length = index + 1
        if byte_value >= 0x10:
            break

    return (stream_id, data[:length])


def serialize_stream_id(num):
    # FIXME: this is bogus!
    assert num >= 0x10
    length = max(num.bit_length() // 8 + 1, 2)
    return num.to_bytes(length, 'big', signed=False)
