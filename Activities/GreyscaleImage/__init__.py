import azure.functions as func
from PIL import Image
import io


async def main(context: func.Context, image_blob: bytes) -> bytes:
    try:
        with Image.open(io.BytesIO(image_blob)) as img:
            img_grayscale = img.convert("L")
            with io.BytesIO() as output:
                img_grayscale.save(output, format=img.format)
                grayscale_image_bytes = output.getvalue()
        return grayscale_image_bytes
    except Exception as e:
        raise Exception(f"Error converting image to grayscale: {e}")
