"""Strict experiment records and non-retriable numerical divergence states."""

import json
import math
import numbers
import os
from pathlib import Path

DIVERGENCE_EXIT_CODE = 42


class NumericalDivergence(RuntimeError):
    """An observed numerical outcome, never an automatically retriable failure."""


def resubmission_enabled(args):
    return bool(
        getattr(args, "resubmission_metrics_jsonl", False)
        or getattr(args, "resubmission_evaluate_raw", False)
        or getattr(args, "paired_data_seed", None) is not None
    )


def validate_resubmission_settings(args):
    if resubmission_enabled(args) and not getattr(args, "use_ema", False):
        raise RuntimeError(
            "Resubmission fixed endpoints require EMA; raw aliases are forbidden"
        )
    if getattr(args, "paired_data_seed", None) is not None and getattr(
        args, "train_2d", False
    ):
        raise RuntimeError(
            "paired_data_seed with train_2d is not a registered paired data flow"
        )


def sanitized(value, prefix=""):
    """Return JSON-safe numbers plus paths of actual non-finite values."""
    if isinstance(value, dict):
        result, paths = {}, []
        for key, item in value.items():
            result[key], child = sanitized(
                item, f"{prefix}.{key}" if prefix else str(key)
            )
            paths.extend(child)
        return result, paths
    if isinstance(value, (list, tuple)):
        result, paths = [], []
        for index, item in enumerate(value):
            clean, child = sanitized(item, f"{prefix}[{index}]")
            result.append(clean)
            paths.extend(child)
        return result, paths
    if isinstance(value, bool) or value is None:
        return value, []
    if isinstance(value, numbers.Integral):
        return int(value), []
    if isinstance(value, numbers.Real):
        return (float(value), []) if math.isfinite(value) else (None, [prefix])
    return value, []


def write_strict_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    clean, _ = sanitized(value)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(clean, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )
    os.replace(temporary, path)


def divergence(args, epoch, stage, metrics, detail=None):
    clean, paths = sanitized(metrics)
    record = dict(
        status="DIVERGED",
        epoch=int(epoch) + 1,
        stage=stage,
        non_finite=True,
        non_finite_fields=paths,
        metrics=clean,
        detail=detail,
        retry_allowed=False,
    )
    try:
        write_strict_json(Path(args.resubmission_run_dir) / "divergence.json", record)
    except OSError as exc:
        # A recording failure must not convert an unfavorable numerical outcome
        # into a retriable technical failure.
        raise NumericalDivergence(
            f"Numerical divergence; recording also failed: {exc}"
        ) from exc
    raise NumericalDivergence(f"Numerical divergence at epoch {epoch + 1}: {stage}")


def guard_loss(loss, args, epoch):
    if not resubmission_enabled(args):
        return
    import torch

    if not bool(torch.isfinite(loss).all()):
        divergence(args, epoch, "training_loss", {"loss": float(loss.detach().cpu())})


def guard_gradients(model, args, epoch):
    if not resubmission_enabled(args):
        return
    import torch

    values = [
        p.grad.detach().reshape(-1) for p in model.parameters() if p.grad is not None
    ]
    if values and not bool(torch.isfinite(torch.cat(values)).all()):
        divergence(args, epoch, "training_gradients", {"gradient": float("nan")})


def checked_metrics(args, epoch, stage, metrics, jsonl_path=None):
    """Persist null/flag for invalid computed metrics, then terminate explicitly."""
    clean, paths = sanitized(metrics)
    clean["non_finite"] = bool(paths)
    clean["non_finite_fields"] = paths
    if paths:
        try:
            if jsonl_path is not None:
                with Path(jsonl_path).open("a", encoding="utf-8") as handle:
                    handle.write(json.dumps(clean, allow_nan=False) + "\n")
            write_strict_json(
                Path(args.resubmission_run_dir) / "non_finite_metrics.json", clean
            )
        finally:
            divergence(args, epoch, stage, metrics)
    if jsonl_path is not None:
        with Path(jsonl_path).open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(clean, allow_nan=False) + "\n")
    return clean


def classify_process(returncode, run_folder):
    events = list(Path(run_folder).glob("checkpoints*/divergence.json"))
    if returncode == DIVERGENCE_EXIT_CODE:
        return "DIVERGED"
    if events:
        return "INVALID"
    return "PROCESS_EXITED" if returncode == 0 else "FAILED"
