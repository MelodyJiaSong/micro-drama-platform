from __future__ import annotations


class EpisodeError(Exception):
    pass


class InvalidStageTransitionError(EpisodeError):
    pass
