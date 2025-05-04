from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import io

app = FastAPI()

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/enhance")
async def enhance_image(
    file: UploadFile = File(...),
    operation: str = Form(...),
    value: float = Form(1.0)
):
    image = Image.open(file.file).convert("RGB")

    if operation == "grayscale":
        image = image.convert("L")
    elif operation == "sharpen":
        image = image.filter(ImageFilter.SHARPEN)
    elif operation == "contrast":
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(value)
    elif operation == "rotate":
        image = image.rotate(value)
    elif operation == "thumbnail":
        image.thumbnail((100, 100))
    elif operation == "ghibli":
        image = image.filter(ImageFilter.DETAIL).filter(ImageFilter.EDGE_ENHANCE)
    elif operation == "sketch":
        gray = image.convert("L")
        inverted = ImageOps.invert(gray)
        blurred = inverted.filter(ImageFilter.GaussianBlur(10))
        sketch = Image.blend(gray, blurred, 0.5)
        image = sketch.convert("RGB")
    elif operation == "cartoon":
        image = image.filter(ImageFilter.CONTOUR).filter(ImageFilter.SMOOTH_MORE)
    elif operation == "paint":
        image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="image/png")
