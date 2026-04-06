"""Excalidraw diagram builder — encapsulates element creation and file output."""

import json
import math
import os


class ExcalidrawDiagram:
    """Builds an Excalidraw document with rect, txt, arr, line, and diamond elements."""

    def __init__(self, seed: int = 1000):
        self._seed = seed
        self.data: dict = {
            "type": "excalidraw",
            "version": 2,
            "source": "https://excalidraw.com",
            "elements": [],
            "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None},
            "files": {},
        }

    @property
    def elements(self) -> list:
        return self.data["elements"]

    def _ns(self) -> int:
        self._seed += 1
        return self._seed

    def rect(
        self,
        id: str,
        x: int | float,
        y: int | float,
        w: int | float,
        h: int | float,
        stroke: str,
        bg: str,
        *,
        fill: str = "solid",
        opacity: int = 100,
        dashed: bool = False,
        bnd: list | None = None,
        sw: int = 2,
    ) -> None:
        self.elements.append({
            "type": "rectangle",
            "id": id,
            "x": x,
            "y": y,
            "width": w,
            "height": h,
            "angle": 0,
            "strokeColor": stroke,
            "backgroundColor": bg,
            "fillStyle": fill,
            "strokeWidth": sw,
            "strokeStyle": "dashed" if dashed else "solid",
            "roughness": 1,
            "opacity": opacity,
            "roundness": {"type": 3},
            "seed": self._ns(),
            "version": 1,
            "versionNonce": self._ns(),
            "isDeleted": False,
            "groupIds": [],
            "boundElements": bnd if bnd is not None else [],
            "frameId": None,
            "link": None,
            "locked": False,
            "updated": 1710000000000,
        })

    def txt(
        self,
        id: str,
        x: int | float,
        y: int | float,
        w: int | float,
        h: int | float,
        t: str,
        sz: int | float,
        *,
        color: str = "#1e1e1e",
        cid: str | None = None,
        op: int = 100,
        align: str = "center",
        valign: str = "middle",
    ) -> None:
        if cid:
            num_lines = t.count("\n") + 1
            actual_h = math.ceil(num_lines * sz * 1.25)
            y = y + (h - actual_h) // 2
            h = actual_h
        self.elements.append({
            "type": "text",
            "id": id,
            "x": x,
            "y": y,
            "width": w,
            "height": h,
            "angle": 0,
            "text": t,
            "originalText": t,
            "fontSize": sz,
            "fontFamily": 1,
            "textAlign": align,
            "verticalAlign": valign,
            "lineHeight": 1.25,
            "autoResize": True,
            "containerId": cid,
            "strokeColor": color,
            "backgroundColor": "transparent",
            "fillStyle": "solid",
            "strokeWidth": 2,
            "strokeStyle": "solid",
            "roughness": 1,
            "opacity": op,
            "seed": self._ns(),
            "version": 1,
            "versionNonce": self._ns(),
            "isDeleted": False,
            "groupIds": [],
            "boundElements": [],
            "frameId": None,
            "link": None,
            "locked": False,
            "updated": 1710000000000,
        })

    def arr(
        self,
        id: str,
        x: int | float,
        y: int | float,
        pts: list,
        stroke: str,
        *,
        dash: bool = False,
        op: int = 100,
        sb: dict | None = None,
        eb: dict | None = None,
    ) -> None:
        self.elements.append({
            "type": "arrow",
            "id": id,
            "x": x,
            "y": y,
            "width": abs(pts[-1][0] - pts[0][0]),
            "height": abs(pts[-1][1] - pts[0][1]),
            "angle": 0,
            "points": pts,
            "startArrowhead": None,
            "endArrowhead": "arrow",
            "startBinding": sb,
            "endBinding": eb,
            "elbowed": False,
            "strokeColor": stroke,
            "backgroundColor": "transparent",
            "fillStyle": "solid",
            "strokeWidth": 2,
            "strokeStyle": "dashed" if dash else "solid",
            "roughness": 1,
            "opacity": op,
            "seed": self._ns(),
            "version": 1,
            "versionNonce": self._ns(),
            "isDeleted": False,
            "groupIds": [],
            "boundElements": [],
            "frameId": None,
            "link": None,
            "locked": False,
            "updated": 1710000000000,
        })

    def line(
        self,
        id: str,
        x: int | float,
        y: int | float,
        pts: list,
        stroke: str,
        *,
        sw: int = 2,
        dash: bool = False,
        op: int = 100,
    ) -> None:
        self.elements.append({
            "type": "line",
            "id": id,
            "x": x,
            "y": y,
            "width": max(abs(p[0]) for p in pts),
            "height": max(abs(p[1]) for p in pts),
            "angle": 0,
            "points": pts,
            "startArrowhead": None,
            "endArrowhead": None,
            "startBinding": None,
            "endBinding": None,
            "strokeColor": stroke,
            "backgroundColor": "transparent",
            "fillStyle": "solid",
            "strokeWidth": sw,
            "strokeStyle": "dashed" if dash else "solid",
            "roughness": 1,
            "opacity": op,
            "seed": self._ns(),
            "version": 1,
            "versionNonce": self._ns(),
            "isDeleted": False,
            "groupIds": [],
            "boundElements": [],
            "frameId": None,
            "link": None,
            "locked": False,
            "updated": 1710000000000,
        })

    def diamond(
        self,
        id: str,
        x: int | float,
        y: int | float,
        w: int | float,
        h: int | float,
        stroke: str,
        bg: str,
        *,
        fill: str = "solid",
        opacity: int = 100,
        bnd: list | None = None,
    ) -> None:
        self.elements.append({
            "type": "diamond",
            "id": id,
            "x": x,
            "y": y,
            "width": w,
            "height": h,
            "angle": 0,
            "strokeColor": stroke,
            "backgroundColor": bg,
            "fillStyle": fill,
            "strokeWidth": 2,
            "strokeStyle": "solid",
            "roughness": 1,
            "opacity": opacity,
            "roundness": {"type": 2},
            "seed": self._ns(),
            "version": 1,
            "versionNonce": self._ns(),
            "isDeleted": False,
            "groupIds": [],
            "boundElements": bnd if bnd is not None else [],
            "frameId": None,
            "link": None,
            "locked": False,
            "updated": 1710000000000,
        })

    def save(self, path: str) -> None:
        """Write the .excalidraw JSON file, creating parent dirs if needed."""
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, "w") as f:
            json.dump(self.data, f, indent=2)
