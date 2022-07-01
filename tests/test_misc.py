import pytest

from reporter import Reporter
from reporter.exceptions import ReporterHttpError


def test_http_request_404(rc: Reporter):
    """Test that a 404 response raises a ReporterHttpError exception."""
    with pytest.raises(ReporterHttpError):
        rc.http_request(
            verb="get",
            path="does-not-exist",
        )
