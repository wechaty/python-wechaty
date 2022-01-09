import pytest
from wechaty.wechaty import Wechaty  # noqa


@pytest.mark.asyncio
async def test_room(test_bot: Wechaty) -> None:
    owner = await test_bot.Room("fake_room").owner()
    await owner.ready()
    assert owner.contact_id == "wechaty_user"
