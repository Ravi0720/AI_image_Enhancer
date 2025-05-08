from PIL import Image, ImageEnhance

def apply_grayscale(image: Image.Image) -> Image.Image:
    return image.convert("L")

def apply_sepia(image: Image.Image) -> Image.Image:
    # Convert to RGB if not already
    image = image.convert("RGB")
    pixels = image.load()
    width, height = image.size

    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            # Sepia formula
            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tb = int(0.272 * r + 0.534 * g + 0.131 * b)
            pixels[x, y] = (
                min(255, tr),
                min(255, tg),
                min(255, tb)
            )
    return image

def apply_brightness(image: Image.Image, factor: float = 1.5) -> Image.Image:
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)