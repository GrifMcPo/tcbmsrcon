import os
from typing import List, Union

language = 'en'  # ua / en / ru

class Configuration:
    token: str
    log_level: str
    admins_list: List[int]
    rcon_host: str
    rcon_port: int
    rcon_pass: str

    @classmethod
    def from_env(cls):
        kwargs = {'token': '8911166276:AAFyf2kdVbRCRi81Um_-f5lrfaRCBuzX87s',
                  'admins_list': '8308522569'.split('_'),
                  'rcon_host': 'f1.rustix.me:25575',
                  'rcon_pass': '__871410__grifmcproRCON'}

        if os.environ.get('RCON_PORT'):
            kwargs['rcon_port'] = os.environ['RCON_PORT']
        if os.environ.get('LOG_LEVEL'):
            kwargs['log_level'] = os.environ['LOG_LEVEL']

        return cls(**kwargs)

    def __init__(self,
                 token: str,
                 admins_list: List[Union[int, str]],
                 rcon_host: str,
                 rcon_pass: str,
                 rcon_port: Union[int, str] = 25575,
                 log_level: str = 'INFO',):
        self.token = token
        self.log_level = self._check_log_level(log_level)
        self.admins_list = [int(v) for v in admins_list]
        self.rcon_host = rcon_host
        self.rcon_port = int(rcon_port)
        self.rcon_pass = rcon_pass

    def _check_log_level(self, log_level: str):
        if log_level.upper() in ('CRITICAL', 'ERROR', 'WARNING', 'INFO',
                                 'DEBUG', 'NOTSET'):
            return log_level.upper()
        raise ValueError('Uncorrect logging level.')
