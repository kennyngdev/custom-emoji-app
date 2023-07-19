import base64
from io import BytesIO

from PIL import Image
from pydantic import BaseModel


class Emoji(BaseModel):
    name: str  # name of emoji
    image_data: str  # base64 string

    def transform_to_thumbnail_gif(self):
        # decode data from base64 string
        image_bytes = base64.b64decode(self.image_data)
        # open image and resize
        image = Image.open(BytesIO(image_bytes)).resize((100, 100))
        # Saves to a new BytesIO image to avoid re-opening image, and convert it to GIF
        gif_image = BytesIO()
        image.save(gif_image, 'GIF')
        gif_image.seek(0)
        gif_data = gif_image.read()
        # encode thumbnail data to b64 string
        self.image_data = base64.b64encode(gif_data).decode()

    def get_image_as_bytes(self):
        return base64.b64decode(self.image_data)
