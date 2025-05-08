def enhance_image(image_bytes: bytes, style: str) -> bytes:
    if style == "anime":
        from .anime_style import apply_anime_style
        return apply_anime_style(image_bytes)
    else:
        raise ValueError("Unknown style")

def apply_enhancement(image_path: str, style: str) -> str:
    # your enhancement logic
    enhanced_image_path = f"{image_path}_enhanced"  # Placeholder logic
    return enhanced_image_path
