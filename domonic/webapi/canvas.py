"""
domonic.webapi.canvas
====================================
https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API
https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API
"""

from __future__ import annotations

import base64
import json
import math
import re
from dataclasses import dataclass, field
from typing import Any

from domonic.dom import DOMException


def _create_promise():
    from domonic.javascript import Promise

    return Promise()


def _canvas_dimension(canvas: Any, name: str, default: int) -> int:
    value: Any = None
    if hasattr(canvas, "getAttribute"):
        value = canvas.getAttribute(name)
    if value is None:
        value = getattr(canvas, name, default)
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _json_safe(value: Any) -> Any:
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (bytes, bytearray, memoryview)):
        return list(bytes(value))
    return repr(value)


def _bytes_from_any(data: Any) -> bytes:
    if data is None:
        return b""
    if isinstance(data, bytes):
        return data
    if isinstance(data, bytearray):
        return bytes(data)
    if isinstance(data, memoryview):
        return data.tobytes()
    if hasattr(data, "byteLength") and hasattr(data, "__getitem__"):
        return bytes(data[index] for index in range(data.byteLength))
    try:
        return bytes(data)
    except TypeError:
        return str(data).encode("utf-8")


class TextMetrics:
    """Basic text measurement returned by ``measureText()``."""

    def __init__(self, text: str, width: float) -> None:
        self.width = width
        self.actualBoundingBoxLeft = 0
        self.actualBoundingBoxRight = width
        self.actualBoundingBoxAscent = 0
        self.actualBoundingBoxDescent = 0


class ImageData:
    """Pixel buffer for canvas image APIs."""

    def __init__(self, width: int, height: int, data: Any | None = None) -> None:
        self.width = int(width)
        self.height = int(height)
        size = max(0, self.width * self.height * 4)
        data_bytes = _bytes_from_any(data) if data is not None else b""
        self.data = bytearray(data_bytes[:size])
        if len(self.data) < size:
            self.data.extend(b"\x00" * (size - len(self.data)))


class CanvasGradient:
    """Recorded canvas gradient with color stops."""

    def __init__(self, kind: str, args: tuple[Any, ...]) -> None:
        self.kind = kind
        self.args = tuple(args)
        self.colorStops: list[tuple[float, str]] = []

    def addColorStop(self, offset: float, color: str) -> None:
        offset = float(offset)
        if offset < 0 or offset > 1:
            raise DOMException(
                DOMException.INDEX_SIZE_ERR, "Color stop is out of range"
            )
        self.colorStops.append((offset, str(color)))


class CanvasPattern:
    """Recorded canvas pattern."""

    def __init__(self, image: Any, repetition: str = "repeat") -> None:
        self.image = image
        self.repetition = repetition or "repeat"


class Path2D:
    """Simple path command container."""

    def __init__(self, path: "Path2D | str | None" = None) -> None:
        self.commands: list[dict[str, Any]] = []
        if isinstance(path, Path2D):
            self.commands.extend(path.commands)
        elif path:
            self.commands.append({"name": "svgPath", "args": [str(path)]})

    def _record(self, name: str, *args: Any) -> None:
        self.commands.append({"name": name, "args": [_json_safe(arg) for arg in args]})

    def moveTo(self, x: float, y: float) -> None:
        self._record("moveTo", x, y)

    def lineTo(self, x: float, y: float) -> None:
        self._record("lineTo", x, y)

    def rect(self, x: float, y: float, width: float, height: float) -> None:
        self._record("rect", x, y, width, height)

    def arc(
        self,
        x: float,
        y: float,
        radius: float,
        startAngle: float,
        endAngle: float,
        counterclockwise: bool = False,
    ) -> None:
        self._record("arc", x, y, radius, startAngle, endAngle, counterclockwise)

    def closePath(self) -> None:
        self._record("closePath")

    def addPath(self, path: "Path2D") -> None:
        if isinstance(path, Path2D):
            self.commands.extend(path.commands)


class CanvasRenderingContext2D:
    """Canvas 2D context that records drawing commands for inspection."""

    def __init__(self, canvas: Any, options: dict[str, Any] | None = None) -> None:
        self.canvas = canvas
        self.options = dict(options or {})
        self.commands: list[dict[str, Any]] = []
        self.fillStyle: Any = "#000000"
        self.strokeStyle: Any = "#000000"
        self.globalAlpha = 1.0
        self.lineWidth = 1.0
        self.lineCap = "butt"
        self.lineJoin = "miter"
        self.font = "10px sans-serif"
        self.textAlign = "start"
        self.textBaseline = "alphabetic"
        self._path = Path2D()
        self._line_dash: list[float] = []
        self._state_stack: list[dict[str, Any]] = []
        self._transform: tuple[float, float, float, float, float, float] = (
            1.0, 0.0, 0.0, 1.0, 0.0, 0.0,
        )

    @property
    def width(self) -> int:
        return _canvas_dimension(self.canvas, "width", 300)

    @property
    def height(self) -> int:
        return _canvas_dimension(self.canvas, "height", 150)

    def _record(self, name: str, *args: Any) -> None:
        self.commands.append({"name": name, "args": [_json_safe(arg) for arg in args]})

    def save(self) -> None:
        self._state_stack.append(
            {
                "fillStyle": self.fillStyle,
                "strokeStyle": self.strokeStyle,
                "globalAlpha": self.globalAlpha,
                "lineWidth": self.lineWidth,
                "lineCap": self.lineCap,
                "lineJoin": self.lineJoin,
                "font": self.font,
                "textAlign": self.textAlign,
                "textBaseline": self.textBaseline,
                "lineDash": list(self._line_dash),
                "transform": self._transform,
            }
        )
        self._record("save")

    def restore(self) -> None:
        if self._state_stack:
            state = self._state_stack.pop()
            self.fillStyle = state["fillStyle"]
            self.strokeStyle = state["strokeStyle"]
            self.globalAlpha = state["globalAlpha"]
            self.lineWidth = state["lineWidth"]
            self.lineCap = state["lineCap"]
            self.lineJoin = state["lineJoin"]
            self.font = state["font"]
            self.textAlign = state["textAlign"]
            self.textBaseline = state["textBaseline"]
            self._line_dash = state["lineDash"]
            self._transform = state["transform"]
        self._record("restore")

    def beginPath(self) -> None:
        self._path = Path2D()
        self._record("beginPath")

    def closePath(self) -> None:
        self._path.closePath()
        self._record("closePath")

    def moveTo(self, x: float, y: float) -> None:
        self._path.moveTo(x, y)
        self._record("moveTo", x, y)

    def lineTo(self, x: float, y: float) -> None:
        self._path.lineTo(x, y)
        self._record("lineTo", x, y)

    def rect(self, x: float, y: float, width: float, height: float) -> None:
        self._path.rect(x, y, width, height)
        self._record("rect", x, y, width, height)

    def arc(
        self,
        x: float,
        y: float,
        radius: float,
        startAngle: float,
        endAngle: float,
        counterclockwise: bool = False,
    ) -> None:
        self._path.arc(x, y, radius, startAngle, endAngle, counterclockwise)
        self._record("arc", x, y, radius, startAngle, endAngle, counterclockwise)

    def fill(self, path: Path2D | None = None, fillRule: str = "nonzero") -> None:
        self._record("fill", path or self._path, fillRule)

    def stroke(self, path: Path2D | None = None) -> None:
        self._record("stroke", path or self._path)

    def clip(self, path: Path2D | None = None, fillRule: str = "nonzero") -> None:
        self._record("clip", path or self._path, fillRule)

    def clearRect(self, x: float, y: float, width: float, height: float) -> None:
        self._record("clearRect", x, y, width, height)

    def fillRect(self, x: float, y: float, width: float, height: float) -> None:
        self._record("fillRect", x, y, width, height)

    def strokeRect(self, x: float, y: float, width: float, height: float) -> None:
        self._record("strokeRect", x, y, width, height)

    def fillText(
        self, text: str, x: float, y: float, maxWidth: float | None = None
    ) -> None:
        self._record("fillText", text, x, y, maxWidth)

    def strokeText(
        self, text: str, x: float, y: float, maxWidth: float | None = None
    ) -> None:
        self._record("strokeText", text, x, y, maxWidth)

    def measureText(self, text: str) -> TextMetrics:
        match = re.search(r"(\d+(?:\.\d+)?)px", self.font)
        font_size = float(match.group(1)) if match else 10.0
        return TextMetrics(str(text), len(str(text)) * font_size * 0.6)

    def drawImage(self, image: Any, *args: Any) -> None:
        self._record("drawImage", image, *args)

    def createImageData(self, width: int, height: int) -> ImageData:
        return ImageData(width, height)

    def getImageData(self, sx: int, sy: int, sw: int, sh: int) -> ImageData:
        self._record("getImageData", sx, sy, sw, sh)
        return ImageData(sw, sh)

    def putImageData(self, imageData: ImageData, dx: int, dy: int, *dirty: Any) -> None:
        self._record("putImageData", imageData, dx, dy, *dirty)

    def createLinearGradient(
        self, x0: float, y0: float, x1: float, y1: float
    ) -> CanvasGradient:
        return CanvasGradient("linear", (x0, y0, x1, y1))

    def createRadialGradient(self, *args: Any) -> CanvasGradient:
        return CanvasGradient("radial", tuple(args))

    def createConicGradient(
        self, startAngle: float, x: float, y: float
    ) -> CanvasGradient:
        return CanvasGradient("conic", (startAngle, x, y))

    def createPattern(self, image: Any, repetition: str = "repeat") -> CanvasPattern:
        return CanvasPattern(image, repetition)

    def setLineDash(self, segments: list[float] | tuple[float, ...]) -> None:
        self._line_dash = [float(segment) for segment in segments]

    def getLineDash(self) -> list[float]:
        return list(self._line_dash)

    def translate(self, x: float, y: float) -> None:
        a, b, c, d, e, f = self._transform
        self._transform = (a, b, c, d, e + x, f + y)
        self._record("translate", x, y)

    def scale(self, x: float, y: float) -> None:
        a, b, c, d, e, f = self._transform
        self._transform = (a * x, b, c, d * y, e, f)
        self._record("scale", x, y)

    def rotate(self, angle: float) -> None:
        cos_angle = math.cos(angle)
        sin_angle = math.sin(angle)
        self._transform = (
            cos_angle,
            sin_angle,
            -sin_angle,
            cos_angle,
            self._transform[4],
            self._transform[5],
        )
        self._record("rotate", angle)

    def transform(
        self, a: float, b: float, c: float, d: float, e: float, f: float
    ) -> None:
        self._transform = (a, b, c, d, e, f)
        self._record("transform", a, b, c, d, e, f)

    def setTransform(
        self,
        a: float = 1,
        b: float = 0,
        c: float = 0,
        d: float = 1,
        e: float = 0,
        f: float = 0,
    ) -> None:
        self._transform = (a, b, c, d, e, f)
        self._record("setTransform", a, b, c, d, e, f)

    def resetTransform(self) -> None:
        self._transform = (1, 0, 0, 1, 0, 0)
        self._record("resetTransform")

    def getTransform(self) -> tuple[float, float, float, float, float, float]:
        return self._transform

    def toJSON(self) -> dict[str, Any]:
        return {
            "width": self.width,
            "height": self.height,
            "commands": list(self.commands),
        }


@dataclass
class WebGLBuffer:
    id: int
    target: int | None = None
    usage: int | None = None
    data: bytes = b""


@dataclass
class WebGLShader:
    id: int
    type: int
    source: str = ""
    compiled: bool = False
    infoLog: str = ""


@dataclass
class WebGLProgram:
    id: int
    shaders: list[WebGLShader] = field(default_factory=list)
    linked: bool = False
    infoLog: str = ""


class WebGLRenderingContext:
    """Small inspectable WebGL context for command recording and setup tests."""

    ARRAY_BUFFER = 0x8892
    ELEMENT_ARRAY_BUFFER = 0x8893
    STATIC_DRAW = 0x88E4
    DYNAMIC_DRAW = 0x88E8
    STREAM_DRAW = 0x88E0
    COLOR_BUFFER_BIT = 0x4000
    DEPTH_BUFFER_BIT = 0x0100
    STENCIL_BUFFER_BIT = 0x0400
    VERTEX_SHADER = 0x8B31
    FRAGMENT_SHADER = 0x8B30
    COMPILE_STATUS = 0x8B81
    LINK_STATUS = 0x8B82
    SHADER_TYPE = 0x8B4F
    VERSION = 0x1F02
    VENDOR = 0x1F00
    RENDERER = 0x1F01
    VIEWPORT = 0x0BA2

    def __init__(self, canvas: Any, options: dict[str, Any] | None = None) -> None:
        self.canvas = canvas
        self.options = dict(options or {})
        self.commands: list[dict[str, Any]] = []
        self.drawingBufferWidth = _canvas_dimension(canvas, "width", 300)
        self.drawingBufferHeight = _canvas_dimension(canvas, "height", 150)
        self._next_id = 1
        self._bound_buffers: dict[int, WebGLBuffer] = {}
        self._clear_color = (0.0, 0.0, 0.0, 0.0)
        self._viewport = (0, 0, self.drawingBufferWidth, self.drawingBufferHeight)
        self._current_program: WebGLProgram | None = None
        self._lost = False

    def _id(self) -> int:
        value = self._next_id
        self._next_id += 1
        return value

    def _record(self, name: str, *args: Any) -> None:
        self.commands.append({"name": name, "args": [_json_safe(arg) for arg in args]})

    def getContextAttributes(self) -> dict[str, Any]:
        defaults = {
            "alpha": True,
            "depth": True,
            "stencil": False,
            "antialias": True,
            "premultipliedAlpha": True,
            "preserveDrawingBuffer": False,
        }
        defaults.update(self.options)
        return defaults

    def isContextLost(self) -> bool:
        return self._lost

    def getParameter(self, pname: int) -> Any:
        if pname == self.VERSION:
            return "WebGL 1.0 domonic"
        if pname == self.VENDOR:
            return "domonic"
        if pname == self.RENDERER:
            return "domonic command recorder"
        if pname == self.VIEWPORT:
            return self._viewport
        return None

    def viewport(self, x: int, y: int, width: int, height: int) -> None:
        self._viewport = (int(x), int(y), int(width), int(height))
        self._record("viewport", *self._viewport)

    def clearColor(self, red: float, green: float, blue: float, alpha: float) -> None:
        self._clear_color = (float(red), float(green), float(blue), float(alpha))
        self._record("clearColor", *self._clear_color)

    def clear(self, mask: int) -> None:
        self._record("clear", int(mask))

    def createBuffer(self) -> WebGLBuffer:
        return WebGLBuffer(self._id())

    def bindBuffer(self, target: int, buffer: WebGLBuffer | None) -> None:
        if buffer is not None:
            buffer.target = target
            self._bound_buffers[target] = buffer
        else:
            self._bound_buffers.pop(target, None)
        self._record("bindBuffer", target, buffer)

    def bufferData(self, target: int, data: Any, usage: int) -> None:
        buffer = self._bound_buffers.get(target)
        if buffer is None:
            raise DOMException(DOMException.INVALID_STATE_ERR, "No buffer is bound")
        buffer.data = _bytes_from_any(data)
        buffer.usage = usage
        self._record("bufferData", target, buffer.data, usage)

    def createShader(self, shaderType: int) -> WebGLShader:
        return WebGLShader(self._id(), shaderType)

    def shaderSource(self, shader: WebGLShader, source: str) -> None:
        shader.source = str(source)
        self._record("shaderSource", shader, source)

    def compileShader(self, shader: WebGLShader) -> None:
        shader.compiled = bool(shader.source.strip())
        shader.infoLog = "" if shader.compiled else "Shader source is empty"
        self._record("compileShader", shader)

    def getShaderParameter(self, shader: WebGLShader, pname: int) -> Any:
        if pname == self.COMPILE_STATUS:
            return shader.compiled
        if pname == self.SHADER_TYPE:
            return shader.type
        return None

    def getShaderInfoLog(self, shader: WebGLShader) -> str:
        return shader.infoLog

    def createProgram(self) -> WebGLProgram:
        return WebGLProgram(self._id())

    def attachShader(self, program: WebGLProgram, shader: WebGLShader) -> None:
        if shader not in program.shaders:
            program.shaders.append(shader)
        self._record("attachShader", program, shader)

    def linkProgram(self, program: WebGLProgram) -> None:
        shader_types = {shader.type for shader in program.shaders if shader.compiled}
        program.linked = (
            self.VERTEX_SHADER in shader_types and self.FRAGMENT_SHADER in shader_types
        )
        program.infoLog = (
            ""
            if program.linked
            else "Program requires compiled vertex and fragment shaders"
        )
        self._record("linkProgram", program)

    def getProgramParameter(self, program: WebGLProgram, pname: int) -> Any:
        if pname == self.LINK_STATUS:
            return program.linked
        return None

    def getProgramInfoLog(self, program: WebGLProgram) -> str:
        return program.infoLog

    def useProgram(self, program: WebGLProgram | None) -> None:
        if program is not None and not program.linked:
            raise DOMException(DOMException.INVALID_STATE_ERR, "Program is not linked")
        self._current_program = program
        self._record("useProgram", program)

    def getSupportedExtensions(self) -> list[str]:
        return []

    def getExtension(self, name: str) -> None:
        return None


class WebGL2RenderingContext(WebGLRenderingContext):
    """WebGL 2 context marker with the same command-recorder behavior."""

    def getParameter(self, pname: int) -> Any:
        if pname == self.VERSION:
            return "WebGL 2.0 domonic"
        return super().getParameter(pname)


class OffscreenCanvas:
    """Canvas-like object that can be used without an ``HTMLElement``."""

    def __init__(self, width: int, height: int) -> None:
        self.width = int(width)
        self.height = int(height)
        self._context_type: str | None = None
        self._context: Any = None

    def getContext(self, contextId: str, options: dict[str, Any] | None = None) -> Any:
        return get_canvas_context(self, contextId, options)

    def convertToBlob(self, options: dict[str, Any] | None = None):
        options = dict(options or {})
        return _create_promise().resolve(
            canvas_to_blob(self, options.get("type", "image/png"))
        )

    def toDataURL(self, type: str = "image/png", quality: Any | None = None) -> str:
        return canvas_to_data_url(self, type, quality)


def get_canvas_context(
    canvas: Any, contextId: str, options: dict[str, Any] | None = None
) -> Any:
    kind = str(contextId or "").lower()
    existing_kind = getattr(canvas, "_context_type", None)
    existing = getattr(canvas, "_context", None)
    group = "webgl" if kind in {"webgl", "experimental-webgl", "webgl2"} else kind

    if existing is not None:
        if existing_kind == group:
            return existing
        return None

    context: Any
    if kind == "2d":
        context = CanvasRenderingContext2D(canvas, options)
    elif kind in {"webgl", "experimental-webgl"}:
        context = WebGLRenderingContext(canvas, options)
        group = "webgl"
    elif kind == "webgl2":
        context = WebGL2RenderingContext(canvas, options)
        group = "webgl"
    else:
        return None

    setattr(canvas, "_context_type", group)
    setattr(canvas, "_context", context)
    return context


def canvas_to_data_url(
    canvas: Any, type: str = "image/png", quality: Any | None = None
) -> str:
    mime_type = str(type or "image/png")
    payload = {
        "width": _canvas_dimension(canvas, "width", 300),
        "height": _canvas_dimension(canvas, "height", 150),
        "context": getattr(canvas, "_context_type", None),
        "quality": quality,
    }
    data = base64.b64encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    return f"data:{mime_type};base64,{data.decode('ascii')}"


def canvas_to_blob(canvas: Any, type: str = "image/png"):
    from domonic.webapi.file import Blob

    return Blob([canvas_to_data_url(canvas, type).encode("utf-8")], {"type": type})


__all__ = [
    "CanvasGradient",
    "CanvasPattern",
    "CanvasRenderingContext2D",
    "ImageData",
    "OffscreenCanvas",
    "Path2D",
    "TextMetrics",
    "WebGL2RenderingContext",
    "WebGLBuffer",
    "WebGLProgram",
    "WebGLRenderingContext",
    "WebGLShader",
]
