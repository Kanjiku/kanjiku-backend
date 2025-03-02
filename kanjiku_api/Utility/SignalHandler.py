import asyncio

from uuid import UUID

from kanjiku_api.Utility import ImageHandler


async def create_thumbnail(img_uid: UUID, img_handler: ImageHandler):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, img_handler.create_thumbnail, str(img_uid))
