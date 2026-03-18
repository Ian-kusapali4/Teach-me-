"""Reusable condition checks for routing or gating nodes."""


def always_true(*_args, **_kwargs) -> bool:
    return True
