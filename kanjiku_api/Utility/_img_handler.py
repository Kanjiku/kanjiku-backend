import os
import aiofiles
import aiofiles.os
import logging

from PIL import Image
from sanic.response import file_stream
from typing import Optional
from dataclasses import dataclass

logger = logging.getLogger("kanjiku_api.Utility.ImageHandler")


@dataclass
class ImageHandler:
    image_path: str
    supported_image_types: list[str]

    def __post_init__(self):
        os.makedirs(self.image_path, exist_ok=True)

    async def create_file(self, file: bytes, filename: str):
        logger.debug(f"{self.image_path}/{filename}")
        async with aiofiles.open(f"{self.image_path}/{filename}", mode="wb") as f:
            await f.write(file)

    async def remove_file(self, filename: str):
        if self.exists(f"{self.image_path}/{filename}"):
            await aiofiles.os.remove(f"{self.image_path}/{filename}")
        if self.exists(f"{self.image_path}/{filename}_thumbnail"):
            await aiofiles.os.remove(f"{self.image_path}/{filename}_thumbnail")

    def exists(self, filename: str) -> bool:
        return os.path.isfile(f"{self.image_path}/{filename}")

    def get_file(self, filepath: str, filename: Optional[str] = None):
        return file_stream(f"{self.image_path}/{filepath}", filename=filename)

    def create_thumbnail(self, filename):
        img = Image.open(f"{self.image_path}/{filename}")
        img.thumbnail((250, 250))
        img.save(f"{self.image_path}/{filename}_thumbnail", "webp")
