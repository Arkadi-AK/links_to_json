import aiohttp
import pytest

from src.get_methods_from_url import uri_validator, get_allow_methods


@pytest.mark.parametrize("a, expected_result", [
    ("https://google.com", True),
    ("https://www.youtube.com/", True),
    ("https://vk.com", True),
    ("https://www.facebook.com", True),
    ("mail.ru", False),
    ("https://httpbin.org", True),
    ("httpshttpbinorg", False)
])
def test_uri_validator(a, expected_result):
    assert uri_validator(a) == expected_result


@pytest.fixture
async def test_get_allow_methods():
    url = "https://google.com"
    async with aiohttp.ClientSession() as session:
        assert await get_allow_methods(session, url) == {'GET': 200, 'HEAD': 200}
