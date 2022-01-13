from getpass import getpass

from reporter.client import Reporter


def main():
    api_token = getpass("Reporter API token: ")

    reporter = Reporter(api_token)
    result = reporter.findings.list(filter={"severity": "11"})

    import pdb; pdb.set_trace()
