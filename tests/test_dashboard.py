from yuleak_api.client import YuleakClient


def test_views():
    dashboards = YuleakClient.dashboards()
    assert len(dashboards) > 0
    for dashboard in dashboards:
        # Display stats (similar to dashboard view in WebUI)
        stats = dashboard.stats()
        assert len(stats) > 0
        assert 'blacklist' in stats
        # Display map (similar to map widget in WebUI)
        map_ = dashboard.map()
        assert len(map_) > 0
        # Display graph (similar to graph view in WebUI)
        graph = dashboard.graph()
        assert len(graph) > 0
        for node in graph:
            assert len(node.neighbors) > 0
        # Display timeline (similar to timeline widget in WebUI)
        timeline = dashboard.timeline()
        assert len(timeline) > 0
        assert timeline[0].total > 0
        # Display details (similar to details view in WebUI)
        details = dashboard.details()
        assert len(details) > 0
        for server in details:
            assert server.geo.country_name is not None
            for domain in server.domains:
                if domain.screenshot is not None:
                    assert domain.screenshot.url is not None
                    assert domain.screenshot.url != ''
                    assert domain.screenshot.download('/tmp/{0}.png'.format(domain.value))
        assert details[0].geo.country_name is not None


def test_resources():
    dashboards = YuleakClient.dashboards()
    assert len(dashboards) > 0
    dashboard = dashboards[0]
    resources = dashboard.resources()
    for resource in resources:
        if resource.type == 'server':
            assert resource.renew()
        else:
            assert resource.delete()


def test_bookmark():
    dashboards = YuleakClient.dashboards()
    server = dashboards[0].details()[0]
    assert not server.bookmark
    assert server.add_bookmark()
    assert server.bookmark
    assert server.del_bookmark()
    assert not server.bookmark


def test_filters():
    dashboards = YuleakClient.dashboards()
    dashboard = dashboards[0]
    # Add filter
    nb_old = len(dashboard.details())
    dashboard.add_filter('domain', 'all')
    assert len(dashboard.details()) < nb_old
    # Del filter
    for f in dashboard.filters():
        print(f)
        assert f.delete()
    assert len(dashboard.filters()) == 0


def test_search():
    YuleakClient.search('yuleak.com')
    dashboard = YuleakClient.dashboards()[-1]
    dashboard.search('yuleak.io')
    dashboard.delete()
    if len(dashboard.list_new_servers()) > 0:
        dashboard.searchall()
