import tkinter as tk
from pydantic import BaseModel


class Point(BaseModel):
    x: int = 0
    y: int = 0


class DragArea(BaseModel):
    start: Point
    end: Point


class CaptureBBox(BaseModel):
    x1: int = 0
    y1: int = 0
    x2: int = 0
    y2: int = 0


class CaptureBBoxManager:
    def __init__(self):
        self._bbox = CaptureBBox()
        self._drag_area = DragArea(start=Point(), end=Point())
        self._root = None

    @property
    def bbox(self) -> CaptureBBox:
        return self._bbox

    def run(self):
        self._root = tk.Tk()
        self._root.attributes("-fullscreen", True)
        self._root.attributes("-topmost", True)
        self._root.wait_visibility(self._root)
        self._root.wm_attributes("-alpha", 0.3)

        self._root.bind("<Button-1>", self._on_click)
        self._root.bind("<B1-Motion>", self._on_drag)
        self._root.bind("<ButtonRelease-1>", self._on_release)
        self._root.mainloop()

    def _on_click(self, event: tk.Event):
        self._drag_area.start.x = event.x
        self._drag_area.start.y = event.y

    def _on_drag(self, event: tk.Event):
        self._drag_area.end.x = event.x
        self._drag_area.end.y = event.y
        self._root.geometry(f"+{event.x_root}+{event.y_root}")

    def _on_release(self, event: tk.Event):
        x1, x2 = sorted([self._drag_area.start.x, self._drag_area.end.x])
        y1, y2 = sorted([self._drag_area.start.y, self._drag_area.end.y])
        self._bbox.x1 = x1
        self._bbox.x2 = x2
        self._bbox.y1 = y1
        self._bbox.y2 = y2

        if self._root is not None:
            self._root.destroy()
            self._root = None
    

