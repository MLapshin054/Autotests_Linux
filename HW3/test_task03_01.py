import yaml
from checkers import checkout, getout

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestPositive:

    def test_step1(self, make_folders, clear_folders, make_files, log_statistic):
        # test1
        res1 = checkout("cd {}; 7z a {}/arx2 -t{}".format(data["folder_in"], data["folder_out"], data["type"]), "Everything is Ok")
        res2 = checkout("ls {}".format(data["folder_out"]), "arx2.{}".format(data["type"]))
        assert res1 and res2, "test1 FAIL"

    def test_step2(self, clear_folders, make_files, log_statistic):
        # test2
        res = []
        res.append(checkout("cd {}; 7z a {}/arx2 -t{}".format(data["folder_in"], data["folder_out"], data["type"]), "Everything is Ok"))
        res.append(checkout("cd {}; 7z e arx2.{} -o{} -y".format(data["folder_out"], data["type"], data["folder_ext"]), "Everything is Ok"))
        for item in make_files:
            res.append(checkout("ls {}".format(data["folder_ext"]), item))
        assert all(res), "test2 FAIL"

    def test_step3(self, log_statistic):
        # test3
        assert checkout("cd {}; 7z t arx2.{}".format(data["folder_out"], data["type"]), "Everything is Ok"), "test3 FAIL"

    def test_step4(self, log_statistic):
        # test4
        assert checkout("cd {}; 7z u arx2.{}".format(data["folder_in"], data["type"]), "Everything is Ok"), "test4 FAIL"

    def test_step5(self, clear_folders, make_files, log_statistic):
        # test5
        res = []
        res.append(checkout("cd {}; 7z a {}/arx2 -t{}".format(data["folder_in"], data["folder_out"], data["type"]), "Everything is Ok"))
        for item in make_files:
            res.append(checkout("cd {}; 7z l arx2.{}".format(data["folder_out"], data["type"]), item))
        assert all(res), "test5 FAIL"

    def test_step6(self, clear_folders, make_files, make_subfolder, log_statistic):
        # test6
        res = []
        res.append(checkout("cd {}; 7z a {}/arx -t{}".format(data["folder_in"], data["folder_out"], data["type"]), "Everything is Ok"))
        res.append(checkout("cd {}; 7z x arx.{} -o{} -y".format(data["folder_out"], data["type"], data["folder_ext2"]), "Everything is Ok"))
        for item in make_files:
            res.append(checkout("ls {}".format(data["folder_ext2"]), item))
        res.append(checkout("ls {}".format(data["folder_ext2"]), make_subfolder[0]))
        res.append(checkout("ls {}/{}".format(data["folder_ext2"], make_subfolder[0]), make_subfolder[1]))
        assert all(res), "test6 FAIL"

    def test_step7(self, log_statistic):
        # test7
        assert checkout("cd {}; 7z d arx.7z".format(data["folder_out"]), "Everything is Ok"), "test7 FAIL"

    def test_step8(self, clear_folders, make_files, log_statistic):
        # test8
        res = []
        for item in make_files:
            res.append(checkout("cd {}; 7z h {}".format(data["folder_in"], item), "Everything is Ok"))
            hash = getout("cd {}; crc32 {}".format(data["folder_in"], item)).upper()
            res.append(checkout("cd {}; 7z h {}".format(data["folder_in"], item), hash))
        assert all(res), "test8 FAIL"
