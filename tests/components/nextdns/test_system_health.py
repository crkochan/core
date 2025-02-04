"""Test NextDNS system health."""
import asyncio

from aiohttp import ClientError
from nextdns.const import API_ENDPOINT

from homeassistant.components.nextdns.const import DOMAIN
from homeassistant.setup import async_setup_component

from tests.common import get_system_health_info


async def test_nextdns_system_health(hass, aioclient_mock):
    """Test NextDNS system health."""
    aioclient_mock.get(API_ENDPOINT, text="")
    hass.config.components.add(DOMAIN)
    assert await async_setup_component(hass, "system_health", {})

    info = await get_system_health_info(hass, DOMAIN)

    for key, val in info.items():
        if asyncio.iscoroutine(val):
            info[key] = await val

    assert info == {"can_reach_server": "ok"}


async def test_nextdns_system_health_fail(hass, aioclient_mock):
    """Test NextDNS system health."""
    aioclient_mock.get(API_ENDPOINT, exc=ClientError)
    hass.config.components.add(DOMAIN)
    assert await async_setup_component(hass, "system_health", {})

    info = await get_system_health_info(hass, DOMAIN)

    for key, val in info.items():
        if asyncio.iscoroutine(val):
            info[key] = await val

    assert info == {"can_reach_server": {"type": "failed", "error": "unreachable"}}
