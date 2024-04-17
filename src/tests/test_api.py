import pytest
from fastapi.testclient import TestClient

from start_api import app

client = TestClient(app)


class MockPowerSupply:
    def connect(self):
        print('successfully connected')

    def disconnect(self):
        print('successfully disconnected')

    def get_telemetry(self, channel):
        return {'channel': channel, 'voltage': 5, 'current': 56}

    def log_telemetry(self, channel):
        pass

    def get_current_state(self):
        pass

    def channel_on(self, channel, voltage, current):
        pass

    def channel_off(self, channel):
        pass


@pytest.fixture
def mock_power_supply(monkeypatch):
    monkeypatch.setattr('src.power_supply.PowerSupply.connect',
                        MockPowerSupply().connect)
    monkeypatch.setattr('src.power_supply.PowerSupply.disconnect',
                        MockPowerSupply().disconnect)
    monkeypatch.setattr('src.power_supply.PowerSupply.get_telemetry',
                        MockPowerSupply().get_telemetry)
    monkeypatch.setattr('src.power_supply.PowerSupply.log_telemetry',
                        MockPowerSupply().log_telemetry)
    monkeypatch.setattr('src.power_supply.PowerSupply.get_current_state',
                        MockPowerSupply().get_current_state)
    monkeypatch.setattr('src.power_supply.PowerSupply.channel_on',
                        MockPowerSupply().channel_on)
    monkeypatch.setattr('src.power_supply.PowerSupply.channel_off',
                        MockPowerSupply().channel_off)


def test_connect_socket(mock_power_supply):
    response = client.get(app.url_path_for('connect_socket'))
    assert response.status_code == 200


def test_disconnect_socket(mock_power_supply):
    response = client.get(app.url_path_for('disconnect_socket'))
    assert response.status_code == 200


def test_read_telemetry(mock_power_supply):
    channel = 1
    response = client.get(f'/telemetry/{channel}')
    assert response.status_code == 200
    channel = 5
    response = client.get(f'/telemetry/{channel}')
    assert response.status_code == 400


def test_write_telemetry(mock_power_supply):
    channel = 1
    response = client.get(f'/log_telemetry/{channel}')
    assert response.status_code == 200
    channel = 5
    response = client.get(f'/log_telemetry/{channel}')
    assert response.status_code == 400


def test_read_current_state(mock_power_supply):
    response = client.get('/current_state')
    assert response.status_code == 200


def test_channel_on(mock_power_supply):
    channel_1 = 1
    channel_2 = 5
    voltage = 5
    current = 10
    response = client.post(f'/channel/on/?channel={channel_1}&voltage={voltage}&current={current}')
    assert response.status_code == 200
    response = client.post(f'/channel/on/?channel={channel_2}&voltage={voltage}&current={current}')
    assert response.status_code == 400


def test_channel_off(mock_power_supply):
    channel = 1
    response = client.post(f'/channel/off/{channel}')
    assert response.status_code == 200
    channel = 0
    response = client.post(f'/channel/off/{channel}')
    assert response.status_code == 400
