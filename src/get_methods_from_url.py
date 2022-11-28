import asyncio
from urllib.parse import urlparse

import aiohttp

results = dict()


# TODO '''Make a function for sending asynchronous HTTP requests'''

def inputs() -> list:
    lines = []
    while True:
        try:
            print("Введите URL")
            line = input()
            if line == "":
                print("Нажмите Enter еще раз для завершения ввода")
                line2 = input()
                if line2 == "":
                    return lines
                elif uri_validator(line2) is False:
                    print(f"Строка '{line2}' не является ссылкой")
                else:
                    lines.append(line2)
            elif uri_validator(line) is False:
                print(f"Строка '{line}' не является ссылкой")
            else:
                lines.append(line)
        except (ValueError, EOFError):
            return lines


def uri_validator(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


async def get_allow_methods(session, url: str) -> dict:
    http_methods = ["OPTIONS", "GET", "HEAD", "POST", "PUT", "PATCH", "DELETE"]
    available_methods = dict()
    for method in http_methods:
        async with session.request(method=method, url=url) as resp:
            if resp.status != 405:
                available_methods[method] = resp.status
    results.setdefault(url, available_methods)
    return available_methods


async def get_methods_from_url(urls: list):
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            task = asyncio.create_task(get_allow_methods(session, url))
            tasks.append(task)
        await asyncio.gather(*tasks)


def main(list_if_urls):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_methods_from_url(list_if_urls))
    print(results)


if __name__ == "__main__":
    input_links = inputs()
    main(input_links)
