import enum


class DataType(enum.Enum):
    na = 'na'
    raw = 'raw'
    byte = 'byte'
    word = 'word'
    dword = 'dword'
    str = 'str'
    bool = 'bool'
    gid = 'gid'
    token = 'token'
    atom = 'atom'
    stream = 'stream'
    crit = 'crit'
    objst = 'objst'
    var = 'var'
    vdword = 'vdword'
    vstring = 'vstring'
    alert = 'alert'
    bytelist = 'bytelist'
    orient = 'orient'
    multi = 'multi'
    ignore = 'ignore'
