import pytest
import requests_mock


@pytest.fixture
def mock_requests(request):
    """A test fixture to mock the requests library."""
    mocker = requests_mock.Mocker()
    mocker.start()

    def finalize():
        mocker.stop()

    request.addfinalizer(finalize)
    return mocker