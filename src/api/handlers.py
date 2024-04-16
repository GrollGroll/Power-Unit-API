from fastapi import APIRouter, HTTPException

from ..power_supply import power_supply

router = APIRouter()


@router.get('/connect')
async def connect_socket():
    power_supply.connect()


@router.get('/telemetry/{channel}')
async def read_telemetry(channel: int):
    if channel > 4:
        raise HTTPException(status_code=400, detail='Select channel from 1 to 4')
    telemetry = power_supply.get_telemetry(channel)
    if not telemetry:
        raise HTTPException(status_code=404, detail='Channel not found')
    return telemetry


@router.get('/current_state/')
async def read_current_state():
    return power_supply.get_current_state()


@router.post('/channel/on/')
async def channel_on(channel: int, voltage: float, current: float):
    if channel > 4:
        raise HTTPException(status_code=400, detail='Select channel from 1 to 4')
    power_supply.channel_on(channel, voltage, current)
    return None


@router.post('/channel/off/{channel}')
async def channel_off(channel: int):
    if channel > 4:
        raise HTTPException(status_code=400, detail='Select channel from 1 to 4')
    power_supply.channel_off(channel)
    return None
