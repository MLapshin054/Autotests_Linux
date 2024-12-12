import yaml
from sshcheckers import ssh_checkout_negative, upload_files, ssh_checkout

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestNegative:

    def test_install(self, start_time, log_statistic):
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

        assert all(res), "test FAIL"

    def test_nstep1(self, make_bad_arx, log_statistic):
        assert ssh_checkout_negative(data["ip"], data["user"], data["passwd"],
                                     "cd {}; 7z e arxbad.{} -o{} -y".format(data["folder_out"], data["type"],
                                                                            data["folder_ext"]),
                                     "ERROR:"), "test1 FAIL"

    def test_nstep2(self, make_bad_arx, log_statistic):
        assert ssh_checkout_negative(data["ip"], data["user"], data["passwd"],
                                     "cd {}; 7z t arxbad.{}".format(data["folder_out"], data["type"]),
                                     "ERROR:"), "test2 FAIL"

    def test_deinstall(self, start_time, log_statistic):
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

        assert all(res), "test FAIL"
