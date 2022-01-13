import argparse
from getpass import getpass
import os

import urllib3

from reporter.client import Reporter


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-u",
        "--url",
        help="URL of Reporter instance (default: https://reporter.dongit.nl)",
        default="https://reporter.dongit.nl")
    parser.add_argument(
        "-k",
        "--no-ssl-verify",
        help="Disable SSL certificate verification",
        dest="ssl_verify",
        action="store_false",
    )
    args = vars(parser.parse_args())

    if not args["ssl_verify"]:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    if "REPORTER_API_TOKEN" in os.environ:
        api_token = os.environ["REPORTER_API_TOKEN"]
    else:
        api_token = getpass("Reporter API token: ")

    reporter = Reporter(api_token=api_token,
                        ssl_verify=args["ssl_verify"],
                        url=args["url"])

    attrs = {
        "assessment_type_id": "owasp_top10_2021",
        "title": "Test Assessment",
    }
    reporter.assessments.create(attrs=attrs)

    import pdb; pdb.set_trace()
