import yaml
from checkers import checkout_negative

with open('config.yaml') as f:
    data = yaml.safe_load(f)

class TestNegative:
    def test_nstep1(self, make_bad_arx, log_statistic):
        assert checkout_negative("cd {}; 7z e arxbad.7z -o{} -y".format(data["folder_out"], data["folder_ext"]),
                                 "ERROR:"), "test1 FAIL"


    def test_nstep2(self, make_bad_arx, log_statistic):
        assert checkout_negative("cd {}; 7z t arxbad.7z".format(data["folder_out"]), "ERROR:"), "test2 FAIL"
