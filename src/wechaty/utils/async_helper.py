"""
async helpers
"""
from __future__ import annotations
import asyncio
from asyncio import Task
from typing import List, Any


async def gather_with_concurrency(n_task: int, tasks: List[Task]) -> Any:
    """
    gather tasks with the specific number concurrency
    Args:
        n_task: the number of tasks
        tasks: task objects
    """
    semaphore = asyncio.Semaphore(n_task)

    async def sem_task(task: Task) -> Any:
        async with semaphore:
            return await task
    return await asyncio.gather(*(sem_task(task) for task in tasks))
