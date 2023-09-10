from __future__ import annotations

from dataclasses import dataclass, asdict
import json
import re

from rcon.source import Client

REQUIRED_PLUGINS = (
    'CS:GO Ramp Slope Fix',
    'SurfTimer',
    'CS:GO Movement Unlocker',
    'SurfTimer MapChooser',
)

@dataclass
class SourcemodPlugin:
    Filename: str
    Title: str
    Author: str
    Version: str
    URL: str
    Status: str
    Timestamp: str
    Hash: str

    def from_rcon(raw: str):
        values = {}
        # skip the last line
        for line in list(map(str.strip, raw.split('\n')))[:-1]:
            k, v = line.split(': ', 1)
            values[k] = v
        return SourcemodPlugin(**values)

    def is_running(self) -> bool:
        return self.Status == 'running'

    def __str__(self):
        return json.dumps(asdict(self))


@dataclass
class RCONSurfer:
    password: str
    host: str = '127.0.0.1'
    port: int = 27015

    def send_command(self, command: str) -> str:
        with Client(self.host, self.port, passwd=self.password) as client:
            response = client.run(command)
        return response


    def list_plugins(self) -> str:
        plugins = self.send_command('sm plugins list')

        # skip the first and last line
        for line in list(map(str.strip, plugins.split('\n')))[1:-1]:
            idx, plugin_name, plugin_version, author = re.match(
                f'(?P<idx>\d+) "(?P<plugin_name>.*)" \((?P<plugin_version>.*)\) by (?P<author>.*)',
                line,
            ).groups()
            print(idx, plugin_name, plugin_version, author, sep=', ')

            print(self.send_command(f'sm plugins info {idx}'))

    def check_required_plugins(self) -> str:
        pass
