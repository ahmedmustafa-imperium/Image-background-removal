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

        # Convert to LAB (best perceptual space)
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)

        # Estimate paper background color (top-left corner average)
        bg_sample = lab[0:40, 0:40]
        bg_color = np.mean(bg_sample.reshape(-1, 3), axis=0)

        # Compute color distance from background
        diff = np.linalg.norm(lab.astype(np.float32) - bg_color, axis=2)

        # Normalize distance to alpha
        alpha = np.clip((diff - 10) * 4, 0, 255).astype(np.uint8)

        # Smooth alpha (critical)
        alpha = cv2.GaussianBlur(alpha, (5, 5), 0)

        # Create RGBA
        rgba = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
        rgba[:, :, 3] = alpha

        # Save PNG
        pil_img = Image.fromarray(rgba)
        buffer = io.BytesIO()
        pil_img.save(buffer, format="PNG")

        return base64.b64encode(buffer.getvalue()).decode("utf-8")
