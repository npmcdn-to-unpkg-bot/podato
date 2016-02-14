import pytest
import requests_mock

@pytest.fixture
def mock_requests(request):
    mocker = requests_mock.Mocker()
    mocker.start()

    def finalize():
        mocker.stop()

    request.addfinalizer(finalize)
    return mocker