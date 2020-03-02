# Yuleak API

[![Latest Version on PyPI](https://img.shields.io/pypi/v/yuleak-api.svg)](https://pypi.python.org/pypi/yuleak-api/)
[![Documentation Status](https://readthedocs.org/projects/yuleak-api/badge/?version=latest)](https://yuleak-api.readthedocs.io/en/latest/?badge=latest)
[![Licence](https://img.shields.io/pypi/l/yuleak--api.svg)](https://pypi.python.org/pypi/yuleak-api)

The official Python library for the [Yuleak API](https://app.yuleak.com/apidoc).


## Features

- Convenient methods for making calls to the API.
- Automatic parsing of API responses into Python objects.

## Installation

``yuleak-api`` is available on [PYPI](https://pypi.python.org/pypi/yuleak-api)

```bash
pip install yuleak-api
```

## Documentation

You can use the API with default demo key for development purpose but to use it you'll need to [register to Yuleak](https://app.yuleak.com).

### [Authentication](https://app.yuleak.com/apidoc#authentication)

```python
from yuleak_api.client import YuleakClient
YuleakClient.set_apikey('my_secret_api_key')
```

### [Errors](https://app.yuleak.com/apidoc#errors)

In case of error, GET methods will return an empty list and POST/DELETE will return False.

The error will be displayed in ``yuleak-api`` logger.

Warnings will (such as a deprecated endpoint) will also be displayed in ``yuleak-api`` logger.

### [Pagination](https://app.yuleak.com/apidoc#pagination)

Pagination will be handle by the YuleakClient, you do not have to care about.


## Usage

This is not intended to provide complete documentation of the API.

For more details, [please refer to the official documentation](https://app.yuleak.com/apidoc).

For more information on the included models and abstractions, please read the code.

### [Credits](https://app.yuleak.com/apidoc#get-credits)

Please check your credits amount before making any search or renew action to avoid errors.

```python
print(YuleakClient.credits())
```

### [Dashboards](https://app.yuleak.com/apidoc#get-dashboards)

```python
dashboards = YuleakClient.dashboards()
for dashboard in dashboards:
    # Display stats (similar to dashboard view in WebUI)
    print(dashboard.stats())
    # Display map (similar to map widget in WebUI)
    print(dashboard.map())
    # Display graph (similar to graph view in WebUI)
    for node in dashboard.graph():
        if node.type == 'asn':
            print('AS: {0}'.format(node.label))
            for child in node.neighbors:
                if child.type == 'server':
                    print(child)
    # Display timeline (similar to timeline widget in WebUI)
    print(dashboard.timeline())
    # Display details (similar to details view in WebUI)
    for server in dashboard.details():
        print(server.geo.country_name)
        # Download screenshots
        for domain in server.domains:
            if domain.screenshot is not None:
                domain.screenshot.download('/tmp/{0}.png'.format(domain.value))
    dashboard.delete()
```

### [Resources](https://app.yuleak.com/apidoc#get-resources)

```python
resources = dashboard.resources()
for resource in resources:
    print('{0} :: {1}'.format(resource.value, resource.status))
    if resource.type == 'server':
        resource.renew()
    else:
        resource.delete()
```

### [Bookmarks](https://app.yuleak.com/apidoc#post-bookmark)

```python
server = dashboard.details()[0]
assert not server.bookmark
server.add_bookmark()
assert server.bookmark
server.del_bookmark()
assert not server.bookmark
```

### [Filters](https://app.yuleak.com/apidoc#get-filters)
```python
dashboard.add_filter('domain', 'all')
for f in dashboard.filters():
    print(f)
    f.delete()
```

### [Search](https://app.yuleak.com/apidoc#post-search)
```python
YuleakClient.search('yuleak.com')
dashboard = YuleakClient.dashboards()[-1]
dashboard.search('yuleak.io')
# Mass search
new_servers = dashboard.list_new_servers()
if YuleakClient.credits() >= new_servers > 0:
    dashboard.searchall()
```

## Changelog
### v1.5.0
 * GET dashboard/{id}/statsdns added
 * GET dashboard/{id}/dns added
 * you can now add custom headers in YuleakClient requests
### v1.4.0
 * preview screenshot can now be recovered using server.domain.screenshot.download()
### v1.3.4
 * requests timeout can now be set with YuleakClient.REQUESTS_TIMEOUT
 * requests retry on error can now be set with YuleakClient.REQUESTS_RETRY
### v1.3.3
 * correct error on 'DELETE dashboard/{id}' endpoint
### v1.3.2
 * correct error on 'searchall' endpoint
### v1.3.1
 * correct error on pip install
### v1.3.0
 * GET dashboard/{id}/renewall added
 * POST dashboard/{id}/renewall added
### v1.2.0
 * GET dashboard/{id}/searchall added
 * POST dashboard/{id}/searchall added
### v1.1.0
 * Change to match the Yuleak API path modifications
