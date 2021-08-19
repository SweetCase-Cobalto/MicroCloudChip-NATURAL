from django.test import TestCase
from module.label.file_type import *


class SizeCalculateUnittest(TestCase):

    def test_calculate(self):
        n1 = 12300  # 12.3KB
        n2 = 56004  # 56.004KB

        b1 = FileVolumeType.get_file_volume_type(n1)
        b2 = FileVolumeType.get_file_volume_type(n2)

        self.assertEqual(b2, (FileVolumeType.KB, 56.004))
        self.assertEqual(b1, (FileVolumeType.KB, 12.3))

        b = FileVolumeType.add(b1, b2)
        s = FileVolumeType.sub(b2, b1)

        self.assertEqual(b, (FileVolumeType.KB, 68.304))
        self.assertEqual(s, (FileVolumeType.KB, 43.704))
