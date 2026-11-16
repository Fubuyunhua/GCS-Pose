"""One effective eager FP32 implementation for timing and MAC-eq auditing."""

import hashlib
import json

BENCHMARK_OVERRIDES = {
    "compile_model": False,
    "compile_compatible_scan": False,
    "cuda_graph_model": False,
    "allow_tf32": False,
}


def apply_benchmark_overrides(config):
    config.update(BENCHMARK_OVERRIDES)
    return config


def configuration_sha256(config):
    return hashlib.sha256(json.dumps(dict(config), sort_keys=True).encode()).hexdigest()
