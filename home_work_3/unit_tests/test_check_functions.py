import unittest
import check_functions

class IpAndPortCheckerMok(check_functions.IpAndPortChecker):
    def ejection_program(self, eject_type='main'):
        raise Exception


class TestIpSplit(unittest.TestCase):
    def setUp(self):
        self.a = check_functions.IpAndPortChecker()
        self.spliter = '.'

    def test_split(self):
        ip = '255.255.255.255'
        self.assertEqual(self.a.ip_split(ip=ip, splitter=self.spliter), ['255', '255', '255', '255'])

    def test_wrong_split_1(self):
        ip = '255.255.255.2555'
        self.assertNotEqual(self.a.ip_split(ip=ip, splitter=self.spliter), ['255', '255', '255', '255'])

    def test_wrong_split_2(self):
        ip = '255.255.255.255'
        self.assertNotEqual(self.a.ip_split(ip, self.spliter), [255, 255, 255, 255])


class TestIpListConvert(unittest.TestCase):
    def setUp(self):
        self.a = IpAndPortCheckerMok()

    def test_convert_successful(self):
        ip = ['255', '255', '255', '255']
        self.assertEqual(self.a.ip_list_convert(ip), [255, 255, 255, 255])

    def test_convert_return_is_list(self):
        ip = ['255', '255', '255', '255']
        self.assertIs(type(self.a.ip_list_convert(ip)), list)

    def test_convert_return_not_dict(self):
        ip = ['255', '255', '255', '255']
        self.assertIsNot(type(self.a.ip_list_convert(ip)), dict)

    def test_convert_raise_exept(self):
        ip = ['dsfasds', '255', '255', '255']
        self.assertRaises(Exception, self.a.ip_list_convert, ip)

class TestCheckIpCount(unittest.TestCase):
    def setUp(self):
        self.a = IpAndPortCheckerMok()

    def test_check_successful(self):
        ip = [255, 255, 255, 255]
        for item in ip:
            self.assertEqual(self.a.check_ip_counts(item), True)

class TestPortRange(unittest.TestCase):
    def setUp(self):
        self.a = IpAndPortCheckerMok()

    def test_port_range_right(self):
        port = 3582
        self.assertEqual(self.a.check_port_range(port), True)

    def test_port_range_wront_input(self):
        port = 'sdfsfsdf'
        self.assertRaises(Exception, self.a.check_port_range, port)

class TestGetIndexSysArgs(unittest.TestCase):
    def setUp(self):
        self.a = IpAndPortCheckerMok()

    def test_get_index_successfull(self):
        my_args = ['path', '-a', '255.255.255.255']
        self.assertEqual(self.a.get_index_sys_arg('-a', my_args), 1)

    def test_get_index_wrong_argument(self):
        my_args = ['path', '-a', '255.255.255.255']
        self.assertNotEqual(self.a.get_index_sys_arg('-c', my_args), 1)

if __name__ == '__main__':
    unittest.main()
