import codecs
import unittest

from notaol.p3.init import InitPayload, Platform


SAMPLE_INIT_DATA = codecs.decode(b'039d116180000000050f00001fb4b53ec00014d1032000000000040a0000014b070504ffff0000000000fffec8f718000001b207', 'hex')


class TestInit(unittest.TestCase):
    def test_parse(self):
        init_payload = InitPayload()
        init_payload.parse(SAMPLE_INIT_DATA)

        data = init_payload.to_bytes()

        for i in range(len(SAMPLE_INIT_DATA)):
            print(SAMPLE_INIT_DATA[i], data[i])

        print(init_payload.__dict__)

        self.assertEqual(Platform.windows, init_payload.platform)
        self.assertEqual(0x14d1, init_payload.session_flags)
        self.assertEqual(0xffff, init_payload.num_colors)
        self.assertEqual(0xb207, init_payload.speed)
