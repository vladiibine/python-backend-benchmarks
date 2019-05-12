import subprocess
from collections import defaultdict


class AppSpec(object):
    def __init__(self, name, port, supported_endpoints):
        """
        :param str name:
        :param int port:
        :param list[str] supported_endpoints:
        """
        self.name = name
        self.port = port
        self.endpoints = supported_endpoints


class TestSpec(object):
    def __init__(self, durations, concurrency_levels):
        """
        :param list[int] durations: how many seconds should the tests last
        :param list[int] concurrency_levels: what concurrency levels to use
        """
        self.durations = durations
        self.concurrency_levels = concurrency_levels


Q_10_serial = "/10q/"
Q_1_serial = "/1q/"

DEFAULT_ENDPOINTS = [
    Q_1_serial,
    Q_10_serial,
]

APP_SPECS = [
    AppSpec("django", 9001, DEFAULT_ENDPOINTS),
    AppSpec("tornado 1 db conn", 9002, DEFAULT_ENDPOINTS),
    AppSpec("flask", 9003, DEFAULT_ENDPOINTS),
]

TEST_SPECS = [
    TestSpec([10], [1, 2, 5, 10, 20, 50, 100])
]


def main():
    # concurrency_levels = [1, 5, 10, 20, 50, 100, 1000]
    # test_time = [10]

    # {
    #     duration: {
    #         "app_name": {
    #             concurrency_level: {
    #                 "endpoint": {
    #                     "requests_per_second": X,
    #                 }
    #             }
    #         }
    #     }
    # }
    benchmark_results = \
        defaultdict(  # duration ->
            lambda: defaultdict(  # app_name ->
                lambda: defaultdict(  # concurrency_level ->
                    lambda: defaultdict  # requests_per_second ->
                )
            )
        )

    for test in TEST_SPECS:  # type: TestSpec
        for duration in test.durations:
            for concurrency in test.concurrency_levels:
                for app in APP_SPECS:  # type: AppSpec
                    for endpoint in DEFAULT_ENDPOINTS:
                        if endpoint in app.endpoints:

                            benchmark_results[duration][app.name][concurrency][
                                "requests_per_second"] = \
                                benchmark_endpoint(
                                    endpoint,
                                    app.port,
                                    concurrency,
                                    duration
                                )


def benchmark_endpoint(url_path, port, concurrency, duration):
    proc = subprocess.Popen([
        "ab",
        "-c", "{}".format(concurrency),
        "-t", "{}".format(duration),
        "http://localhost:{}{}".format(port, url_path)
    ], stdout=subprocess.PIPE)

    # Relevant line:
    # Requests per second:    53.62 [#/sec] (mean)
    out, err = proc.communicate()
    req_per_sec = out.decode('utf-8').splitlines()[20].split()[3]
    return float(req_per_sec)


def test_endpoint_is_up(url):
    try:
        # py3
        import urllib.request

        resp = urllib.request.urlopen(url)
        return resp.status == 200

    except ImportError:
        # py2
        import urllib

        resp = urllib.urlopen(url)

        return resp.getcode() == 200


if __name__ == '__main__':
    main()
