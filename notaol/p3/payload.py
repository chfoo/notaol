import abc


class BasePayload(object, metaclass=abc.ABCMeta):
    '''Base class for packet data.'''

    @abc.abstractmethod
    def parse(self, data):
        '''Parse payload data'''

    @abc.abstractmethod
    def to_bytes(self):
        '''Convert to bytes'''
