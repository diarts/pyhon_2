import unittest
import check_functions


class TestIpAndPortChecker(unittest.TestCase):
    def setUp(self):
        self.ip_port_checker = check_functions.IpAndPortChecker()
        self.spliter = '.'
        self.my_sys_args = ['path', 'some', 'things', '-a', '255.255.255.255']
        self.my_var = {'-a': 'localhost', '-p': 7777, '-un': 'Vasiliy Pupckin'}

    def test_init_help_function_failed(self):
        test_function = 1234
        self.assertRaises(ValueError, self.ip_port_checker._init_help_function, test_function)

    def test_ejection_programm_main_success(self):
        eject_type = 'variable'
        returned_string = self.ip_port_checker.ejection_program(eject_type)
        self.assertIs(type(returned_string), str)
        self.assertEqual(returned_string, self.ip_port_checker._WRONG_VARIABLE_MESS)

    def test_ejection_program_ip_success(self):
        eject_type = 'ip'
        returned_string = self.ip_port_checker.ejection_program(eject_type)
        self.assertIs(type(returned_string), str)
        self.assertEqual(returned_string, self.ip_port_checker._WRONG_IP_MESS)

    def test_ejection_program_port_success(self):
        eject_type = 'port'
        returned_string = self.ip_port_checker.ejection_program(eject_type)
        self.assertIs(type(returned_string), str)
        self.assertEqual(returned_string, self.ip_port_checker._WRONG_PORT_MESS)

    def test_ejection_program_wrong_argument(self):
        eject_type = 124131
        self.assertRaises(ValueError, self.ip_port_checker.ejection_program, eject_type)
        eject_type = ''
        self.assertRaises(ValueError, self.ip_port_checker.ejection_program, eject_type)
        eject_type = [4, 5, 584]
        self.assertRaises(ValueError, self.ip_port_checker.ejection_program, eject_type)

    def test_check_ip_success(self):
        ip = [255, 255, 255, 255]
        for item in ip:
            self.assertEqual(self.ip_port_checker.check_ip_counts(item), True)

    def test_check_ip_failed_float(self):
        ip_segment = 235.54
        self.assertRaises(ValueError, self.ip_port_checker.check_ip_counts, ip_segment)
        ip_segment = 'some things'
        self.assertRaises(ValueError, self.ip_port_checker.check_ip_counts, ip_segment)
        ip_segment = 256
        self.assertRaises(ValueError, self.ip_port_checker.check_ip_counts, ip_segment)

    def test_ip_split_success(self):
        ip = '255.255.255.255'
        model = ['255', '255', '255', '255']
        self.assertEqual(self.ip_port_checker.ip_split(ip=ip, splitter=self.spliter), model)

    def test_ip_split_wrong(self):
        ip = '255.255.255.2555'
        model = ['255', '255', '255', '255']
        self.assertNotEqual(self.ip_port_checker.ip_split(ip=ip, splitter=self.spliter), model)
        model = [255, 255, 255, 255]
        self.assertNotEqual(self.ip_port_checker.ip_split(ip, self.spliter), model)

    def test_ip_slit_failed(self):
        ip = 2313143242423424
        self.assertRaises(ValueError, self.ip_port_checker.ip_split, ip, self.spliter)

    def test_convert_successful(self):
        ip = ['255', '255', '255', '255']
        model = [255, 255, 255, 255]
        self.assertEqual(self.ip_port_checker.ip_list_items_convert_to_int(ip), model)

    def test_convert_return_is_list(self):
        ip = ['255', '255', '255', '255']
        self.assertIs(type(self.ip_port_checker.ip_list_items_convert_to_int(ip)), list)

    def test_convert_return_not_dict(self):
        ip = ['255', '255', '255', '255']
        self.assertIsNot(type(self.ip_port_checker.ip_list_items_convert_to_int(ip)), dict)

    def test_convert_failed(self):
        ip = [45453.45, '255', '255', '255']
        self.assertRaises(ValueError, self.ip_port_checker.ip_list_items_convert_to_int, ip)

    def test_pars_ip_success(self):
        ip = '255.255.255.255'
        model = [255, 255, 255, 255]
        self.assertEqual(self.ip_port_checker.check_ip(ip), model)

    def test_pars_ip_failed(self):
        ip = 'some thing'
        self.assertRaises(ValueError, self.ip_port_checker.check_ip, ip)
        ip = 53457132154
        self.assertRaises(ValueError, self.ip_port_checker.check_ip, ip)

    def test_port_range_success(self):
        port = 3582
        self.assertEqual(self.ip_port_checker.check_port(port), port)

    def test_port_range_failed(self):
        port = 'some thing'
        self.assertRaises(ValueError, self.ip_port_checker.check_port, port)
        port = 1231214124
        self.assertRaises(ValueError, self.ip_port_checker.check_port, port)

    def test_get_index_successfull(self):
        key = '-a'
        self.assertEqual(self.ip_port_checker.get_index_sys_arg(key, self.my_sys_args), 3)

    def test_get_index_wrong_argument(self):
        key = '-c'
        self.assertEqual(self.ip_port_checker.get_index_sys_arg(key, self.my_sys_args), False)
        key = 46421
        self.assertEqual(self.ip_port_checker.get_index_sys_arg(key, self.my_sys_args), False)

    def test_get_variable_success(self):
        index = 3
        model_var = '255.255.255.255'
        self.assertEqual(self.ip_port_checker.get_variable(self.my_sys_args, index), model_var)

    def test_get_variable_failed(self):
        index = 4
        self.assertRaises(ValueError, self.ip_port_checker.get_variable, self.my_sys_args, index)

    def test_add_variables_success(self):
        my_sys_args = ['path', 'some', 'things', '-a', '255.255.255.255']
        my_var = {'-a': 'localhost', '-p': 7777, '-un': 'Vasiliy Pupckin'}
        model_dict = {'-a': '255.255.255.255', '-p': 7777, '-un': 'Vasiliy Pupckin'}
        self.assertEqual(self.ip_port_checker.add_variables(my_sys_args, self.my_var), model_dict)

    def test_add_variables_failed(self):
        my_sys_args = ['path', 'some', 'things', '-a', '368.255.255.255']
        self.assertRaises(ValueError, self.ip_port_checker.add_variables, my_sys_args, self.my_var)



if __name__ == '__main__':
    unittest.main()
