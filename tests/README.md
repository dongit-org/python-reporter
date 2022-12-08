# Testing

## Running tests
Run `poetry shell`, and from within this shell run `tox` to run all tests, or `tox -e pytest` to run integration tests.

## Choosing a release
By default, the integration tests run against the release image of Reporter.
To run against the preview release, set the environment variable `IMAGE_REPO` to `preview`.