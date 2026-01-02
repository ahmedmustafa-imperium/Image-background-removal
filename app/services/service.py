import base64
import cv2
import numpy as np
from PIL import Image
import io


class SignatureBgRemovalService:
    def process(self, image_base64: str) -> str:
        # Decode base64
        image_bytes = base64.b64decode(image_base64)
        np_arr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Adaptive threshold (best for paper)
        thresh = cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            31,
            15,
        )

        # Morphological cleanup (improve strokes)
        kernel = np.ones((3, 3), np.uint8)
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)

        # Create RGBA image
        rgba = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
        rgba[:, :, 3] = cleaned  # alpha channel

        # Convert to PNG bytes
        pil_img = Image.fromarray(rgba)
        buffer = io.BytesIO()
        pil_img.save(buffer, format="PNG")

        # Encode back to base64
        return base64.b64encode(buffer.getvalue()).decode("utf-8")
