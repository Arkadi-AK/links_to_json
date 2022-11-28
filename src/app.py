"""
Module methods are needed to determine the available methods of url
"""

from typing import List

import requests
import urlextract


def get_methods_throw_input() -> dict:
    line = input('Input any link and push enter: ')
    if line == "":
        print("Something wrong, repeat it")
        get_methods_throw_input()
    else:
        if check_link(line) is False:
            print("Something wrong, repeat it")
            get_methods_throw_input()
        else:
            link = get_link(line)
    return get_methods(link)


def extract_link(link: str) -> List[str]:
    """Return list of links"""
    extractor = urlextract.URLExtract()
    urls = extractor.find_urls(link)
    return urls


def check_link(link: str) -> bool:
    """Check if the link is in the list"""
    links = extract_link(link)
    return False if not links else True


def get_link(link: str) -> str:
    links = extract_link(link)
    return links[0]


def get_methods(url: str) -> dict:
    """Return dict of methods of url"""
    methods = {}
    http_methods = ["OPTIONS", "GET", "HEAD", "POST", "PUT", "PATCH", "DELETE"]
    for i in http_methods:
        req = requests.Request(method=i, url=url)
        prepared_request = req.prepare()
        request_sessions = requests.Session()
        status_code = request_sessions.send(prepared_request).status_code
        if status_code != 405:
            methods[i] = status_code
    return methods
