'''Connection initialization.'''
import struct
from enum import IntEnum
from notaol.p3.payload import BasePayload


class Platform(IntEnum):
    windows = 0x03
    mac = 0x0c


class InitPayload(BasePayload):
    '''Data sent during INIT.

    Attributes:
        platform (int): 1 byte. Platform such as Windows or Mac.
        client_version (int): 2 bytes. Client internal major and minor version.
        build_num (int): 1 byte. For AOL 5.0.
        machine_memory (int): 1 byte.
        app_memory (int): 1 byte.
        pc_type (int): 2 byte.
        release_month (int): 1 byte.
        release_day (int): 1 byte.
        customer_class (int): 2 byte.
        timestamp (int): 4 bytes. Update disk operation (UDO) timestamp.
        dos_version (int) 2 bytes. DOS major and minor version.
        session_flags (int): 2 bytes.
        video_type (int): 1 byte.
        cpu_type (int): 1 byte.
        media_type (int): 4 bytes.
        windows_version (int): 2 bytes. Windows major and minor version.
        unknown1 (int): 2 bytes.
        windows_mem_type (int): 1 byte.
        horizonal_res (int): 2 bytes. Horizontal screen resolution.
        veritial_res (int): 2 bytes. Vertical screen resolution.
        num_colors (int): 2 bytes. Number of colors.
        filler1 (int): 1 byte.
        region (int): 2 bytes.
        language_1 (int): 2 bytes.
        language_2 (int): 2 bytes.
        language_3 (int): 2 bytes.
        language_4 (int): 2 bytes.
        unknown2 (int): 2 bytes.
        speed (int): 1 byte.
    '''
    TYPE_1_LENGTH = 49
    TYPE_2_LENGTH = 52
    field_struct_1 = struct.Struct('!BHBBBHBBHIHHBBIHHBHHHBHHHHHB')
    field_struct_2 = struct.Struct('!BHBBBHBBHIHHBBIHHBHHHBHHHHHHH')

    def __init__(self):
        self.platform = Platform.windows
        self.client_version = 139 << 8 | 109
        self.build_num = 0x0
        self.machine_memory = 16
        self.app_memory = 0
        self.pc_type = 0
        self.release_month = 5
        self.release_day = 15
        self.customer_class = 0
        self.timestamp = 1303539237
        self.dos_version = 192 << 8
        self.session_flags = 0xc014
        self.video_type = 8
        self.cpu_type = 5
        self.media_type = 0
        self.windows_version = 4 << 8 | 10
        self.unknown1 = 0
        self.windows_mem_type = 1
        self.horizontal_res = 1024
        self.vertical_res = 768
        self.num_colors = 0xffff
        self.filler1 = 0
        self.region = 0
        self.language_1 = 0
        self.language_2 = 0xfeff
        self.language_3 = 0
        self.language_4 = 0
        self.unknown2 = 1
        self.speed = 0x17

    def __str__(self):
        return '<INIT Payload>'

    def parse(self, data):
        '''Parse the data.'''
        if len(data) == self.TYPE_1_LENGTH:
            results = self.field_struct_1.unpack(data)
        elif len(data) == self.TYPE_2_LENGTH:
            results = self.field_struct_2.unpack(data)
        else:
            raise ValueError('Unknown init data.')

        self.platform = results[0]
        self.client_version = results[1]
        self.build_num = results[2]
        self.machine_memory = results[3]
        self.app_memory = results[4]
        self.pc_type = results[5]
        self.release_month = results[6]
        self.release_day = results[7]
        self.customer_class = results[8]
        self.timestamp = results[9]
        self.dos_version = results[10]
        self.session_flags = results[11]
        self.video_type = results[12]
        self.cpu_type = results[13]
        self.media_type = results[14]
        self.windows_version = results[15]
        self.unknown1 = results[16]
        self.windows_mem_type = results[17]
        self.horizontal_res = results[18]
        self.vertical_res = results[19]
        self.num_colors = results[20]
        self.filler1 = results[21]
        self.region = results[22]
        self.language_1 = results[23]
        self.language_2 = results[24]
        self.language_3 = results[25]
        self.language_4 = results[26]

        if len(data) == self.TYPE_1_LENGTH:
            self.speed = results[27]
            assert len(results) == 28
        else:
            self.unknown2 = results[27]
            self.speed = results[28]
            assert len(results) == 29

    def to_bytes(self, length=TYPE_1_LENGTH):
        '''Convert to bytes.'''
        if length == self.TYPE_1_LENGTH:
            return self.field_struct_1.pack(
                self.platform,
                self.client_version,
                self.build_num,
                self.machine_memory,
                self.app_memory,
                self.pc_type,
                self.release_month,
                self.release_day,
                self.customer_class,
                self.timestamp,
                self.dos_version,
                self.session_flags,
                self.video_type,
                self.cpu_type,
                self.media_type,
                self.windows_version,
                self.unknown1,
                self.windows_mem_type,
                self.horizontal_res,
                self.vertical_res,
                self.num_colors,
                self.filler1,
                self.region,
                self.language_1,
                self.language_2,
                self.language_3,
                self.language_4,
                self.speed,
                )
        else:
            return self.field_struct_2.pack(
                self.platform,
                self.client_version,
                self.build_num,
                self.machine_memory,
                self.app_memory,
                self.pc_type,
                self.release_month,
                self.release_day,
                self.customer_class,
                self.timestamp,
                self.dos_version,
                self.session_flags,
                self.video_type,
                self.cpu_type,
                self.media_type,
                self.windows_version,
                self.unknown1,
                self.windows_mem_type,
                self.horizontal_res,
                self.vertical_res,
                self.num_colors,
                self.filler1,
                self.region,
                self.language_1,
                self.language_2,
                self.language_3,
                self.language_4,
                self.unknown2,
                self.speed,
                )
