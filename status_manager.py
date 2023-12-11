import time
import numpy as np
from PIL import ImageGrab
from typing import Optional
import threading

# from capture_bbox_manager import CaptureBBoxManager


class StatusManager:
    def __init__(self):
        self._capture_img: Optional[np.ndarray] = None
        self._result_img: Optional[np.ndarray] = None
        # self._bbox_manager = CaptureBBoxManager()
        self._capture_thread = None
        # self._is_capturing: bool = False

        self.bbox = None
        self.is_capturing = False

    # @property
    # def is_capturing(self) -> bool:
    #     return self._is_capturing

    @property
    def capture_img(self) -> Optional[np.ndarray]:
        return self._capture_img

    @property
    def result_img(self) -> Optional[np.ndarray]:
        return self._result_img

    @result_img.setter
    def result_img(self, img: np.ndarray) -> None:
        self._result_img = img

    def run_capture(self) -> None:
        # self._bbox_manager.run()
        # self._is_capturing = True
        self._start_capture()

    def _start_capture(self) -> None:
        if (
            self._capture_thread is not None
            and self._capture_thread.is_alive()
        ):
            return
        self._capture_thread = threading.Thread(target=self._capture_screen)
        self._capture_thread.daemon = True
        self._capture_thread.start()

    def _capture_screen(self) -> None:
        print(self.is_capturing)
        print(self.bbox)
        while self.is_capturing and self.bbox is not None:
            self._capture_img = np.array(ImageGrab.grab(bbox=self.bbox))
            time.sleep(0.1)

    # def _get_bbox(self) -> tuple[int, int, int, int]:
    #     # bbox = self._bbox_manager.bbox
    #     bbox = self._bbox_manager.bbox
    #     return (bbox.x1, bbox.y1, bbox.x2, bbox.y2)

    def stop_capture(self):
        self.is_capturing = False
        if self._capture_thread is not None:
            self._capture_thread.join()
