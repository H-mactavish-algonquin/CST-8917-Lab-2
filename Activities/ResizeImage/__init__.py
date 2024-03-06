import azure.functions as func
from PIL import Image
import io


async def main(context: func.Context, image_blob: bytes) -> bytes:
    try:
        with Image.open(io.BytesIO(image_blob)) as img:
            img_resized = img.resize((1024, 768))
            with io.BytesIO() as output:
                img_resized.save(output, format=img.format)
                resized_image_bytes = output.getvalue()
        return resized_image_bytes
    except Exception as e:
        raise Exception(f"Error resizing image: {e}")
