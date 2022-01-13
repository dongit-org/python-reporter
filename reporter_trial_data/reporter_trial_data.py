from getpass import getpass
import os

from reporter.client import Reporter


def main():
    if "REPORTER_API_TOKEN" in os.environ:
        api_token = os.environ["REPORTER_API_TOKEN"]
    else:
        api_token = getpass("Reporter API token: ")

    reporter = Reporter(api_token)
    result = reporter.findings.list(filter={"severity": "11"})

    import pdb; pdb.set_trace()
