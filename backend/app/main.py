print("Starting import of dependencies in main.py")
from fastapi import FastAPI, File, UploadFile
print("Imported FastAPI")
from fastapi.responses import FileResponse
print("Imported FileResponse")
from fastapi.middleware.cors import CORSMiddleware
print("Imported CORSMiddleware")
import os
import tempfile
from PIL import Image
import io
print("Imported standard libraries")
from enhancers import enhance_image
print("Imported enhance_image from enhancers")
from filters import apply_grayscale, apply_sepia, apply_brightness
print("Imported filters")

app = FastAPI()
print("Created FastAPI app")

# Add CORS middleware for frontend (React at localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
print("Added CORS middleware")

@app.post("/enhance")
async def enhance_image(file: UploadFile = File(...), style: str = "grayscale"):
    try:
        print(f"Received request to enhance image with style: {style}")
        # Create a temporary file to store the uploaded image
        temp_dir = tempfile.mkdtemp()
        file_location = os.path.join(temp_dir, file.filename)
        with open(file_location, "wb") as f:
            content = await file.read()
            f.write(content)
        print(f"Saved uploaded file to {file_location}")

        # Validate image format
        try:
            image = Image.open(file_location)
            image.verify()  # Verify the image is valid
            image = Image.open(file_location)  # Reopen after verify
            print("Validated image format")
        except Exception as e:
            print(f"Image validation failed: {str(e)}")
            return {"error": f"Invalid image format: {str(e)}"}

        # Apply the requested style
        enhanced_file_location = os.path.join(temp_dir, f"enhanced_{file.filename}")
        if style == "anime":
            # Read image as bytes for AnimeGANv2
            with open(file_location, "rb") as f:
                image_bytes = f.read()
            enhanced_bytes = enhance_image(image_bytes, style="anime")
            with open(enhanced_file_location, "wb") as f:
                f.write(enhanced_bytes)
            print("Applied anime style enhancement")
        else:
            # Apply filters
            if style == "grayscale":
                enhanced_image = apply_grayscale(image)
            elif style == "sepia":
                enhanced_image = apply_sepia(image)
            elif style == "brightness":
                enhanced_image = apply_brightness(image)
            else:
                raise ValueError(f"Unsupported style: {style}")
            print(f"Applied {style} filter")

            # Save the enhanced image as JPEG
            enhanced_image.save(enhanced_file_location, "JPEG")
            print(f"Saved enhanced image to {enhanced_file_location}")

        # Return the enhanced image
        response = FileResponse(
            enhanced_file_location,
            media_type="image/jpeg",
            filename=f"enhanced_{file.filename}"
        )

        # Clean up after the response
        import atexit
        atexit.register(lambda: os.remove(enhanced_file_location))
        atexit.register(lambda: os.rmdir(temp_dir))
        print("Set up file cleanup and prepared response")

        return response

    except Exception as e:
        print(f"Backend error: {str(e)}")
        return {"error": f"Backend error: {str(e)}"}