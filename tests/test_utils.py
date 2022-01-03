import asyncio
import pytest
from wechaty.utils.async_helper import gather_with_concurrency


async def number_task(num: int):
    """
    just return the original number
    """
    return num


@pytest.mark.asyncio
async def test_gather_tasks_with_n_concurrency():
    tasks = [asyncio.create_task(number_task(i)) for i in range(1000)]
    sum_value = (0 + 999) * 1000 / 2
    result = await gather_with_concurrency(10, tasks)
    assert sum_value == sum(result), 'the final sum value is not correct'
