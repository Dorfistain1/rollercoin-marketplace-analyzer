REGIONS = {
    "name": (23, 46, 535, 34),
    "power_bonus": (20, 85, 400, 27),
    "price": (450, 97, 150, 23),
}

def crop_region(image, region_key):
    if region_key not in REGIONS:
        raise ValueError(f"Region '{region_key}' is not defined.")

    x, y, w, h = REGIONS[region_key]

    img_height, img_width = image.shape[:2]
    if x + w > img_width or y + h > img_height:
        raise ValueError(
            f"Cropped region '{region_key}' ({x},{y},{w},{h}) exceeds image bounds ({img_width}x{img_height})"
        )

    return image[y:y+h, x:x+w]
