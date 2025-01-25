import tls_client
import tls_client.response
from client import Client
from typing import Union

class Fragment:
    def __init__(self, proxy: str | None) -> None:
        self.client = Client(proxy)

        self.base_url = 'https://fragment.com'
        self.base_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Connection': 'keep-alive',
            'Host': 'fragment.com',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Priority': 'u=0, i'
        }

    def getUsername(self, username: str) -> Union[tls_client.response.Response, tuple]:
        return self.client.request('GET', f'{self.base_url}/username/{username}', headers = self.base_headers)
