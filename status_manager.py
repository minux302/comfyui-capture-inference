import time
import numpy as np
from PIL import ImageGrab
from typing import Optional
import threading

# from capture_bbox_manager import CaptureBBoxManager


class StatusManager:
    def __init__(self):
        self.capture_img: Optional[np.ndarray] = None
        self.result_img: Optional[np.ndarray] = None
        self._capture_thread = None
        self.bbox = None
        self.is_capturing = False

    def run_capture(self) -> None:
        if (
            self._capture_thread is not None
            and self._capture_thread.is_alive()
        ):
            return
        self._capture_thread = threading.Thread(target=self._capture_screen)
        self._capture_thread.daemon = True
        self._capture_thread.start()

    def _capture_screen(self) -> None:
        while self.is_capturing and self.bbox is not None:
            self.capture_img = np.array(ImageGrab.grab(bbox=self.bbox))
            time.sleep(0.1)

    def stop_capture(self):
        self.is_capturing = False
        if self._capture_thread is not None:
            self._capture_thread.join()
