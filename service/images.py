from PIL import Image
from service import parsing, logger
from io import BytesIO


async def change_image_size(url):
    try:
        img_bio = BytesIO()
        content = parsing.get_html(url).content
        img = Image.open(BytesIO(content))
        img = img.resize((150, 225))
        img.save(img_bio, 'JPEG', quality=100)
        img_bio.seek(0)
        return img_bio

    except Exception:
        text = f"Не удалось скачать картинку для: {url}"
        logger.logger.error(text)
        raise Exception(text)
