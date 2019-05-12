import os
import subprocess

Q_10_serial = "/10q/"
Q_1_serial = "/1q/"

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

DEFAULT_ENDPOINTS = [
    Q_1_serial,
    Q_10_serial,
]

APP_SPECS = [
    AppSpec("django", 9001, DEFAULT_ENDPOINTS),
    AppSpec("tornado", 9002, DEFAULT_ENDPOINTS),
    AppSpec("flask", 9003, DEFAULT_ENDPOINTS),
]

TEST_SPECS = [
    TestSpec([10], [1, 2, 5, 10, 20, 50, 100])
]


def main():
    # concurrency_levels = [1, 5, 10, 20, 50, 100, 1000]
    # test_time = [10]

    for test in TEST_SPECS:  # type: TestSpec
        for duration in test.durations:
            for concurrency in test.concurrency_levels:
                for app in APP_SPECS:  # type: AppSpec
                    for endpoint in DEFAULT_ENDPOINTS:
                        if endpoint in app.endpoints:

                            proc = subprocess.Popen([
                                "ab",
                                f"-c{concurrency}"
                                f"-t{duration}"
                                ""
                            ], stdout=subprocess.PIPE, shell=True)

                            out, err = proc.communicate()

def test_endpoint_is_up(url):
    import requests
    response = requests.get(url)

    return response.status == 200




if __name__ == '__main__':
    main()