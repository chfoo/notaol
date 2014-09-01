import enum

from notaol.fdo.tokenmeta import TOKEN_METADATA


class Token(enum.Enum):
    # TODO: put commonly used tokens here
    pass


TOKEN_TO_DESC_MAP = dict([
    (meta.token, meta.description) for meta in TOKEN_METADATA
    ])
