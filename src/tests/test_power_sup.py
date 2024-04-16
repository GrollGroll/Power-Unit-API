import json
import os

import pytest

from src.power_supply import PowerSupply


@pytest.fixture
def mocked_power_supply(mocker):
    power_supply = PowerSupply('127.0.0.1', 1026)

    mocker.patch.object(power_supply, '_send_command')
    mocker.patch.object(power_supply, '_receive_response', return_value=12)

    return power_supply


def test_get_telemetry(mocked_power_supply):

    telemetry = mocked_power_supply.get_telemetry(1)

    mocked_power_supply._send_command.assert_called_with(':MEASure1:ALL?')
    assert telemetry['parameters'] == 12
    assert type(telemetry) is dict


def test_log_telemetry(mocked_power_supply):
    mocked_power_supply.log_telemetry(1)
    file_path = 'logs\power_supply.log'
    assert os.path.getsize(file_path) > 0


def test_get_current_state(mocked_power_supply):
    json_data = mocked_power_supply.get_current_state()
    assert type(json_data) is str

    try:
        json_data = json.loads(json_data)
    except json.JSONDecodeError:
        pass


def test_channel_on(mocked_power_supply):
    channel = 1
    current = 124.54
    voltage = 12.7
    mocked_power_supply.channel_on(channel, current, voltage)

    mocked_power_supply._send_command.assert_called_with(f':OUTPut{channel}:STATe ON')

    assert mocked_power_supply._send_command.call_count == 3


def test_channel_off(mocked_power_supply):
    mocked_power_supply.channel_off(1)
    mocked_power_supply._send_command.assert_called_with(':OUTPut1:STATe OFF')
