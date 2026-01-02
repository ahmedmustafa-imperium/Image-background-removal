from app.services.service import SignatureBgRemovalService


class BgRemoveManager:
    def __init__(self):
        self.service = SignatureBgRemovalService()

    def remove_background(self, image_base64: str) -> str:
        return self.service.process(image_base64)
