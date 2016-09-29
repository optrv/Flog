import os
from PIL import Image
from flog.configs.conf import UPLOAD_FOLDER, IMAGE_WIDTH, WATERMARK_PATH


def watermark(image_out):
    """
    Add the watermark
    """
    water = Image.open(os.path.join(UPLOAD_FOLDER, WATERMARK_PATH))
    water = water.resize((image_out.size[0] // 4, int((image_out.size[0] // 4 * water.size[1]) //
                                                      water.size[0])), Image.BILINEAR)
    layer = Image.new('RGBA', image_out.size, (0, 0, 0, 0))
    # Add watermark to the right bottom
    pos_water = ((image_out.size[0] - 10 - water.size[0], image_out.size[1] - 10 - water.size[1]))
    layer.paste(water, (pos_water))
    image_out = Image.composite(layer, image_out, layer)
    return image_out


def image_resizer(image, filename, subfolder):
    """
    Resize the image to the specified width
    """
    width = int(IMAGE_WIDTH)
    image_out = Image.open(image)
    if image_out.mode != 'RGBA':
        image_out = image_out.convert('RGBA')
    if image_out.size[0] > width:
        # Resize the image proportional to specified width
        image_out = image_out.resize((width, int((width * image_out.size[1]) /
                                                 image_out.size[0])), Image.BILINEAR)
    image_out = watermark(image_out)
    image_out.save(os.path.join(UPLOAD_FOLDER, subfolder, filename))
