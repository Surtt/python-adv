import asyncio
import random


async def send_email(user: str) -> None:
    delay = random.uniform(0.3, 0.8)
    await asyncio.sleep(delay)
    print(f'Email sent to {user}')


async def send_bulk(users: list[str]) -> None:
    await asyncio.gather(*[send_email(user) for user in users])


async def main() -> None:
    users = ['alice', 'bob', 'carol', 'dave', 'eve']
    await send_bulk(users)


asyncio.run(main())
