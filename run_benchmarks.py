import csv
import subprocess
from collections import defaultdict
from datetime import datetime


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
    def __init__(self, durations, concurrency_levels, name='default'):
        """
        :param list[int] durations: how many seconds should the tests last
        :param list[int] concurrency_levels: what concurrency levels to use
        """
        self.durations = durations
        self.concurrency_levels = concurrency_levels
        self.name = name


Q_10_serial = "/10q/"
Q_1_serial = "/1q/"
Q_0 = "/0q/"

DEFAULT_ENDPOINTS = [
    Q_0,
    Q_1_serial,
    Q_10_serial,
]

APP_SPECS = [
    AppSpec("django", 9001, DEFAULT_ENDPOINTS),
    AppSpec("tornado 1 db conn", 9002, DEFAULT_ENDPOINTS),
    AppSpec("flask", 9003, DEFAULT_ENDPOINTS),
    AppSpec("fastapi-sqlalchemy-async", 9004, DEFAULT_ENDPOINTS),
    AppSpec("fastapi-sqlalchemy-async-threadpool", 9005, DEFAULT_ENDPOINTS),
]

TEST_SPECS = [
    TestSpec(
        durations=[1],
        concurrency_levels=[
            1,
            10,
            100,
        ]
    ),
]


def main():
    benchmark_results = \
        defaultdict(  # duration ->
            lambda: defaultdict(  # endpoint name ->
                lambda: defaultdict(  # concurrency_level ->
                    lambda: defaultdict(  # app_name ->
                        lambda: {}  # requests_per_second ->
                    )
                )
            )
        )
    # estimate progress
    for test in TEST_SPECS:  # type: TestSpec
        num_expected_benchmarks = (
                len(test.concurrency_levels) *
                len(test.durations) *
                len(APP_SPECS) *
                len(DEFAULT_ENDPOINTS)
        )
        print("For test session {}, running {} tests".format(test.name, num_expected_benchmarks))
        current_test_idx = 1
        for duration in test.durations:
            for concurrency in test.concurrency_levels:
                for app in APP_SPECS:  # type: AppSpec
                    for endpoint in DEFAULT_ENDPOINTS:
                        if endpoint in app.endpoints:
                            print(
                                "Running benchmark {count} for {app} {endpoint} concurrency={concurrency} duration={duration}"
                                    .format(
                                    count=current_test_idx,
                                    app=app.name,
                                    endpoint=endpoint,
                                    concurrency=concurrency,
                                    duration=duration,
                                )
                            )
                            current_test_idx += 1
                            benchmark = benchmark_endpoint(
                                endpoint, app.port, concurrency, duration)

                            benchmark_results[duration][endpoint][app.name][concurrency][
                                "requests_per_second"] = benchmark
                            print("Benchmark result (req. per second): " + str(benchmark))
                            print()

    for test in TEST_SPECS:
        # report_to_file(benchmark_results, test)
        report_to_file_collapsed(benchmark_results, test)


def _get_concurrency_column_name(concurrency_: int):
    return 'conc. ' + str(concurrency_)


def report_to_file_collapsed(benchmark_results, test: TestSpec):
    """Like report_to_file, but all endpoints will be reported in the same file

    Produces .tsv reports like this (one file for all endpoints)

    testname_2020-05-20T13:04_05.tsv  # endpoints and backend stacks are concatenated
    |           |  concurrency1 | concurrency2  | concurrency 3   | ...concurrency N  |
    | [0q] backend1  |   132         |  333          |                 |   444             |
    | [1q] backend1  |   132         |  333          |                 |   444             |
    | [10q] backend1  |   132         |  333          |                 |   444             |
    | [0q] backend2  |   333         |   444         |   12321         |                   |
    | [1q] backend2  |   333         |   444         |   12321         |                   |
    | [10q] backend2  |   333         |   444         |   12321         |                   |

    """

    for duration, d1 in benchmark_results.items():
        now = datetime.now()
        target_file_name = "benchmark_results/" + (
            'collapsed_{name}_{y}-{m}-{d}T{h}:{mi}:{s}_{dur}.tsv'
                .format(
                name=test.name, y=now.year, m=now.month, d=now.day, h=now.hour, mi=now.minute,
                s=now.second, dur=duration
            )
        )

        with open(target_file_name, 'w') as f:
            writer.writeheader()
            for endpoint, d2 in d1.items():
                writer = csv.DictWriter(
                    f, fieldnames=['app_name'] + [_get_concurrency_column_name(l) for l in test.concurrency_levels],
                    delimiter='\t', quotechar='"'
                )

                for app_name, d3 in d2.items():
                    row = {
                        "app_name": "[{}] {}".format(endpoint, app_name)
                    }
                    for concurrency, d4 in d3.items():
                        row[_get_concurrency_column_name(concurrency)] = d4["requests_per_second"]

                    writer.writerow(row)


def report_to_file(benchmark_results, test):
    """
    Produces .tsv reports like this (one file per endpoint)

    testname_2020-05-20T13:04_05_10q.tsv  # includes endpoint name 10q
    |           |  concurrency1 | concurrency2  | concurrency 3   | ...concurrency N  |
    | backend1  |   132         |  333          |                 |   444             |
    | backend2  |   333         |   444         |   12321         |                   |

    testname_2020-05-20T13:04_05_1q.tsv  # includes endpoint name 1q
    |           |  concurrency1 | concurrency2  | concurrency 3   | ...concurrency N  |
    | backend1  |   132         |  333          |                 |   444             |
    | backend2  |   333         |   444         |   12321         |                   |

    ...
    """

    for duration, d1 in benchmark_results.items():
        for endpoint, d2 in d1.items():

            now = datetime.now()
            target_file_name = "benchmark_results/" + ((
                                                           '{name}_{y}-{m}-{d}T{h}:{mi}:{s}_{endpoint}.tsv'
                                                               .format(
                                                               name=test.name, y=now.year, m=now.month, d=now.day,
                                                               h=now.hour, mi=now.minute,
                                                               s=now.second, endpoint=str(endpoint)
                                                           )
                                                       ).replace('/', ""))

            with open(target_file_name, 'w') as f:
                writer = csv.DictWriter(
                    f, fieldnames=['app_name'] + [_get_concurrency_column_name(l) for l in test.concurrency_levels],
                    delimiter='\t', quotechar='"'
                )
                writer.writeheader()

                for app_name, d3 in d2.items():
                    row = {
                        "app_name": app_name
                    }
                    for concurrency, d4 in d3.items():
                        row[_get_concurrency_column_name(concurrency)] = d4["requests_per_second"]

                    writer.writerow(row)


def benchmark_endpoint(url_path, port, concurrency, duration):
    proc = subprocess.Popen([
        "ab",
        "-c", "{}".format(concurrency),
        "-t", "{}".format(duration),
        "http://localhost:{}{}".format(port, url_path)
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Relevant line:
    # Requests per second:    53.62 [#/sec] (mean)
    out, err = proc.communicate()
    try:
        req_per_sec = [
            line
            for line in out.decode('utf-8').splitlines()
            if 'requests per second' in line.lower()
        ][0].split()[3]
    except Exception as err:
        return "Error, check docker-compose logs. Possibly timed out."

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


