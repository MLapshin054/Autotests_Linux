from sshcheckers import ssh_checkout, upload_files, ssh_getout
from checkers import getout
import yaml

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestPositive:

    def save_log(self, starttime, name):
        with open(name, 'w') as log_file:
            log_file.write(getout("journalctl --since '{}'".format(starttime)))

    def test_step1(self, start_time):
        res = []
        upload_files(
            data["ip"],
            data["user"], data["passwd"],
            data["pkgname"] + ".deb",
            "/home/{}/{}.deb".format(data["user"], data["pkgname"])
        )
        res.append(
            ssh_checkout(
                data["ip"],
                data["user"], data["passwd"],
                "echo '{}' | sudo -S dpkg -i /home/{}/{}.deb".format(data["passwd"], data["user"], data["pkgname"]),
                "Настраивается пакет"
            )
        )
        res.append(
            ssh_checkout(
                data["ip"],
                data["user"], data["passwd"],
                "echo '{}' | sudo -S dpkg -s {}".format(data["passwd"], data["pkgname"]
                                                        ),
                "Status: install ok installed")
        )

        self.save_log(start_time, "log_test1.txt")
        assert all(res), "test1 FAIL"

    def test_step2(self, make_folders, clear_folders, make_files, start_time, log_statistic):
        res1 = ssh_checkout(
            data["ip"], data["user"], data["passwd"],
            "cd {}; 7z a {}/arx2 -t{}".format(data["folder_in"], data["folder_out"],
                                              data["type"]), "Everything is Ok")
        res2 = ssh_checkout(
            data["ip"], data["user"], data["passwd"],
            "ls {}".format(data["folder_out"]), "arx2.{}".format(data["type"]))
        self.save_log(start_time, "log_test2.txt")
        assert res1 and res2, "test2 FAIL"

    def test_step3(self, clear_folders, make_files, start_time, log_statistic):
        res = []
        res.append(ssh_checkout(
            data["ip"], data["user"], data["passwd"],
            "cd {}; 7z a {}/arx2 -t{}".format(data["folder_in"], data["folder_out"], data["type"]),
            "Everything is Ok"))
        res.append(ssh_checkout(
            data["ip"], data["user"], data["passwd"],
            "cd {}; 7z e arx2.{} -o{} -y".format(data["folder_out"], data["type"], data["folder_ext"]),
            "Everything is Ok"))
        for item in make_files:
            res.append(ssh_checkout(
                data["ip"], data["user"], data["passwd"],
                "ls {}".format(data["folder_ext"]), item))
        self.save_log(start_time, "log_test3.txt")
        assert all(res), "test3 FAIL"

    def test_step4(self, start_time, log_statistic):
        self.save_log(start_time, "log_test4.txt")
        assert ssh_checkout(
            data["ip"], data["user"], data["passwd"],
            "cd {}; 7z t arx2.{}".format(data["folder_out"], data["type"]),
            "Everything is Ok"), "test4 FAIL"

    def test_step5(self, start_time, log_statistic):
        self.save_log(start_time, "log_test5.txt")
        assert ssh_checkout(
            data["ip"], data["user"], data["passwd"],
            "cd {}; 7z u arx2.{}".format(data["folder_in"], data["type"]), "Everything is Ok"), "test5 FAIL"

    def test_step6(self, clear_folders, make_files, start_time, log_statistic):
        res = []
        res.append(ssh_checkout(
            data["ip"], data["user"], data["passwd"],
            "cd {}; 7z a {}/arx2 -t{}".format(data["folder_in"], data["folder_out"], data["type"]),
            "Everything is Ok"))
        for item in make_files:
            res.append(ssh_checkout(
                data["ip"], data["user"], data["passwd"],
                "cd {}; 7z l arx2.{}".format(data["folder_out"], data["type"]), item))
        self.save_log(start_time, "log_test6.txt")
        assert all(res), "test6 FAIL"

    def test_step7(self, clear_folders, make_files, make_subfolder, start_time, log_statistic):
        res = []
        res.append(ssh_checkout(
            data["ip"], data["user"], data["passwd"],
            "cd {}; 7z a {}/arx -t{}".format(data["folder_in"], data["folder_out"], data["type"]),
            "Everything is Ok"))
        res.append(ssh_checkout(
            data["ip"], data["user"], data["passwd"],
            "cd {}; 7z x arx.{} -o{} -y".format(data["folder_out"], data["type"], data["folder_ext2"]),
            "Everything is Ok"))
        for item in make_files:
            res.append(ssh_checkout(
                data["ip"], data["user"], data["passwd"],
                "ls {}".format(data["folder_ext2"]), item))
        res.append(ssh_checkout(
            data["ip"], data["user"], data["passwd"],
            "ls {}".format(data["folder_ext2"]), make_subfolder[0]))
        res.append(ssh_checkout(
            data["ip"], data["user"], data["passwd"],
            "ls {}/{}".format(data["folder_ext2"], make_subfolder[0]), make_subfolder[1]))
        self.save_log(start_time, "log_test7.txt")
        assert all(res), "test7 FAIL"

    def test_step8(self, start_time, log_statistic):
        self.save_log(start_time, "log_test9.txt")
        assert ssh_checkout(
            data["ip"], data["user"], data["passwd"],
            "cd {}; 7z d arx.7z".format(data["folder_out"]), "Everything is Ok"), "test8 FAIL"

    def test_step9(self, clear_folders, make_files, start_time, log_statistic):
        res = []
        for item in make_files:
            res.append(ssh_checkout(
                data["ip"], data["user"], data["passwd"],
                "cd {}; 7z h {}".format(data["folder_in"], item), "Everything is Ok"))
            hash = ssh_getout(
                data["ip"], data["user"], data["passwd"],
                "cd {}; crc32 {}".format(data["folder_in"], item)).upper()
            res.append(ssh_checkout(
                data["ip"], data["user"], data["passwd"],
                "cd {}; 7z h {}".format(data["folder_in"], item), hash))
        self.save_log(start_time, "log_test9.txt")
        assert all(res), "test9 FAIL"

    def test_step10(self, start_time, log_statistic):
        res = []

        res.append(
            ssh_checkout(
                data["ip"],
                data["user"], data["passwd"],
                "echo '{}' | sudo -S dpkg -r {}".format(data["passwd"], data["pkgname"]),
                "Удаляется"
            )
        )
        res.append(
            ssh_checkout(
                data["ip"],
                data["user"], data["passwd"],
                "echo '{}' | sudo -S dpkg -s {}".format(data["passwd"], data["pkgname"]
                                                        ),
                "Status: deinstall ok")
        )

        self.save_log(start_time, "log_test10.txt")
        assert all(res), "test10 FAIL"
