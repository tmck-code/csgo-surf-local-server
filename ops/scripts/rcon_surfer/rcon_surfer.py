from __future__ import annotations

from dataclasses import dataclass, asdict, field
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
class RCONSurfer:
    password: str
    host: str = '127.0.0.1'
    port: int = 27015

    def send_command(self, command: str) -> str:
        with Client(self.host, self.port, passwd=self.password) as client:
            response = client.run(command)
        return response

    def check_required_plugins(self) -> str:
        pass
from collections import namedtuple

@dataclass
class SourcemodPluginCommand:
    Name: str
    Type: str
    Help: str

@dataclass
class SourcemodPluginCommands:
    commands: List[SourcemodPluginCommand]

    def from_rcon(client, idx: int) -> SourcemodPluginCommands:
        raw = client.send_command(f'sm cmds {idx}')
        commands = []
        # skip the first and last lines
        for line in list(map(str.strip, raw.split('\n')))[1:-1]:
            commands.append(SourcemodPluginCommand(
                *map(str.strip, line.split(' ', 2))
            ))

        return SourcemodPluginCommands(commands)

@dataclass
class SourcemodPluginInfo:
    Filename: str
    Title: str
    Author: str
    Version: str
    Status: str
    Timestamp: str
    Hash: str
    URL: str = ''

    def from_rcon(client, idx: int):
        raw = client.send_command(f'sm plugins info {idx}')
        values = {}
        # skip the last line
        for line in list(map(str.strip, raw.split('\n')))[:-1]:
            k, v = line.split(': ', 1)
            values[k] = v
        return SourcemodPluginInfo(**values)

    def is_running(self) -> bool:
        return self.Status == 'running'

    def __str__(self):
        return json.dumps(asdict(self))

@dataclass
class SourcemodPlugin:
    info: SourcemodPluginInfo
    commands: SourcemodPluginCommands

@dataclass
class SourcemodPlugins:
    client: RCONSurfer
    plugins: List[SourcemodPlugin] = field(default_factory=list)

    def list_plugins(self) -> str:
        plugins = self.client.send_command('sm plugins list')

        # skip the first and last line
        for line in list(map(str.strip, plugins.split('\n')))[1:-1]:
            idx, plugin_name, plugin_version, author = re.match(
                f'(?P<idx>\d+) "(?P<plugin_name>.*)" \((?P<plugin_version>.*)\) by (?P<author>.*)',
                line,
            ).groups()

            self.plugins.append(
                SourcemodPlugin(
                    info = SourcemodPluginInfo.from_rcon(self.client, idx),
                    commands = SourcemodPluginCommands.from_rcon(self.client, idx),
                )
            )

    def __str__(self):
        return json.dumps(asdict(self))
