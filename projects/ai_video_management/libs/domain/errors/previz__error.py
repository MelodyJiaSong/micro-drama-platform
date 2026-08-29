"""Previz-aggregate errors: rendering a Blender previz `.blend` to an MP4."""
from __future__ import annotations


class PrevizError(Exception):
    """Base for every previz render failure."""


class InvalidPrevizPathError(PrevizError):
    """Path is empty, outside the exposed sandbox, or not a previz location."""


class PrevizBlendNotFoundError(PrevizError):
    """No `.blend` (or more than one) under the resolved previz folder."""


class BlenderMissingError(PrevizError):
    """No Blender executable found — `BLENDER_EXE` unset and no known install."""


class PrevizRenderBusyError(PrevizError):
    """A render is already in flight. Blender saturates the CPU, so one at a time."""


class PrevizRenderFailedError(PrevizError):
    """Blender or ffmpeg exited non-zero, or produced no output."""
