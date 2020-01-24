from yuleak_api.client import YuleakClient


def test_basics():
    credits_ = YuleakClient.credits()
    assert credits_ == 0
    dashboards = YuleakClient.dashboards()
    assert len(dashboards) > 0
