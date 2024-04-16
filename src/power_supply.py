import json
import socket

from .core.config import app_settings
from .core.loggers import logger_console, logger_file


class PowerSupply:
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.socket = None

    def connect(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        logger_console.info('Connected to power supply')

    def disconnect(self) -> None:
        self.socket.close()
        logger_console.info('Disconnected from power supply')

    def _send_command(self, command: str) -> None:
        self.socket.sendall((command + '\n').encode())

    def _receive_response(self) -> str:
        return self.socket.recv(1024).decode().strip()

    def get_telemetry(self, channel: int) -> dict:
        channel_parameters = {}
        channel_parameters['channel'] = channel
        self._send_command(f':MEASure{channel}:ALL?')
        parameters = self._receive_response()
        channel_parameters['parameters'] = parameters
        return channel_parameters

    def log_telemetry(self, channel: int):
        telemetry = self.get_telemetry(channel)
        logger_file.info(telemetry)

    def get_current_state(self) -> json:
        channels = []

        for i in range(1, 5):
            channel_parameters = {}
            channel_parameters['channel'] = i

            self._send_command(f':MEASure{i}:CURRent?')
            current_ch = self._receive_response()
            channel_parameters['current'] = current_ch

            self._send_command(f':MEASure{i}:VOLTage?')
            voltage_ch = self._receive_response()
            channel_parameters['voltage'] = voltage_ch

            logger_console.info(f'CH{i} info received')
            channels.append(channel_parameters)

        json_data = json.dumps(channels)
        return json_data

    def channel_on(self, channel: int, voltage: float, current: float) -> None:
        self._send_command(f':SOURce{channel}:CURRent {current}')
        self._send_command(f':SOURce{channel}:VOLTage {voltage}')
        self._send_command(f':OUTPut{channel}:STATe ON')
        logger_console.info(f'CH{channel} output turned on')

    def channel_off(self, channel: int) -> None:
        self._send_command(f':OUTPut{channel}:STATe OFF')
        logger_console.info(f'CH{channel} output turned off')


power_supply = PowerSupply(host=app_settings.socket_host, port=app_settings.socket_port)
