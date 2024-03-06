import azure.functions as func
from PIL import Image
import io
from watermarker.marker import add_mark


async def main(context: func.Context, image_blob: bytes) -> bytes:
    try:
        with Image.open(io.BytesIO(image_blob)) as img:
            # Add watermark using the provided logic
            watermark_text = "Himasnhu MacTavish"
            watermarked_img = add_mark(
                img, out=None, mark=watermark_text, size=60, color="#ffffff", opacity=0.5, angle=30, space=60)
            with io.BytesIO() as output:
                watermarked_img.save(output, format=img.format)
                watermarked_image_bytes = output.getvalue()
        return watermarked_image_bytes
    except Exception as e:
        raise Exception(f"Error applying watermark to image: {e}")
