import os
from PIL import Image
from flog.configs.conf import upload_folder, image_width, watermark_path

# Watermark adding with specified (or default) value of position on image
def watermark(image_out):
    water = Image.open(os.path.join(upload_folder, watermark_path))
    water = water.resize((image_out.size[0] // 4, int((image_out.size[0] // 4 * water.size[1]) // water.size[0])), Image.BILINEAR)
    layer = Image.new('RGBA', image_out.size, (0, 0, 0, 0))
    pos_water = ((image_out.size[0] - 10 - water.size[0], image_out.size[1] - 10 - water.size[1]))
    layer.paste(water,(pos_water))
    image_out = Image.composite(layer, image_out, layer)
    return image_out

def image_resizer(image, filename, subfolder):
    width = int(image_width)
    image_out = Image.open(image)
    if image_out.mode != 'RGBA':
        image_out = image_out.convert('RGBA')
    if image_out.size[0] > 500:
        # Resize image proportional to specified width
        image_out = image_out.resize((width, int((width * image_out.size[1]) / image_out.size[0])), Image.BILINEAR)
    image_out = watermark(image_out)
    image_out.save(os.path.join(upload_folder, subfolder, filename))