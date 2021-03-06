from PIL import Image, ImageChops

import logging
logging.getLogger('PIL.PngImagePlugin').setLevel(logging.INFO)

def image_diff(diff_path, before_path, after_path, superimpose=False):
    """ Returns the percentage of differing pixels. """
    before = Image.open(before_path)
    after = Image.open(after_path)

    before = before.convert('RGBA')
    after = after.convert('RGBA')

    width = max(before.width, after.width)
    height = max(before.height, after.height)

    resized_before = Image.new("RGBA", (width, height), "white")
    resized_after = Image.new("RGBA", (width, height), "white")

    resized_before.paste(before)
    resized_after.paste(after)

    mask = ImageChops.difference(resized_before, resized_after)
    mask = mask.convert('L')
    mask = mask.point(lambda k: 0 if k == 0 else 255)

    if mask.getbbox() is None:
        return 0
    else:
        diff = mask.convert('RGB')
        if superimpose:
            diff.paste(resized_after, mask=mask)
        else:
            diff.paste((0, 0, 255), mask=mask)
        diff.save(diff_path)

        pixels = 0

        for v in mask.getdata():
            if v == 255:
                pixels += 1

        return float(pixels)/(width*height)*100
