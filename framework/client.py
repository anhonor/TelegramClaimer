import tls_client
import random
import re

import tls_client.exceptions

class Proxy:
    @staticmethod
    def __construct__(proxy: str) -> str | None:
        patterns = [
            r'(?P<hostname>^[^:]+):(?P<port>\d+):(?P<username>[^:]+):(?P<password>.+)',
            r'(?P<hostname>^[^:]+):(?P<port>\d+)@(?P<username>[^:]+):(?P<password>.+)',
            r'(?P<username>[^:]+):(?P<password>[^:]+):(?P<hostname>[^:]+):(?P<port>\d+)',
            r'(?P<username>[^:]+):(?P<password>[^:]+)@(?P<hostname>[^:]+):(?P<port>\d+)',
            r'(?P<hostname>^[^:]+):(?P<port>\d+)'
        ]

        for pattern in patterns:
            match = re.match(pattern, proxy)
            if match:
                groups = match.groupdict()
                username = groups.get('username')
                password = groups.get('password')
                hostname = groups.get('hostname')
                port = groups.get('port')

                return (
                    f'{username}:{password}@{hostname}:{port}' if username and password else
                    f'{hostname}:{port}'
                )

        return None
    
class Client:
    @staticmethod
    def __get_random_identifier__() -> str:
        return random.choice([
            'chrome_112',
            'chrome_110',
            'chrome_109',
            'chrome_105',
            'chrome_103',
            'chrome_102'
        ])
    
    @staticmethod
    def __get_client__(proxy: str | None) -> tls_client.Session:
        client = tls_client.Session(client_identifier = Client.__get_random_identifier__(), random_tls_extension_order = True)
        formatted_proxy = Proxy.__construct__(proxy)

        if formatted_proxy:
            client.proxies.update({
                'http': 'http://{}'.format(formatted_proxy),
                'https': 'http://{}'.format(formatted_proxy)
            })

        return client
    
    def __init__(self, proxy: str | None) -> None:
        self.client = Client.__get_client__(proxy)
    
    def request(self, method: str, url: str, headers: dict = {}, **kwargs) -> None:
        try:
            self.client.execute_request(method, url, **kwargs)
        except tls_client.exceptions.TLSClientExeption as Exception:
            return (type(Exception), str(Exception))
