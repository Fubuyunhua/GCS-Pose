"""Opt-in per-example augmentation streams for paired routing comparisons."""

import hashlib
import random
import numpy as np
import torch
from torch.utils.data import Dataset


def sampler_seed(seed, epoch):
    """Separate trial/epoch streams without additive shifts across seeds."""
    digest = hashlib.sha256(f"{int(seed)}:sampler:{int(epoch)}".encode()).digest()
    return int.from_bytes(digest[:8], "little")


class PairedDataset(Dataset):
    def __init__(self, dataset, seed):
        self.dataset = dataset
        self.seed = int(seed)
        self.epoch = 0

    def __len__(self):
        return len(self.dataset)

    def set_epoch(self, epoch):
        self.epoch = int(epoch)

    def __getitem__(self, index):
        seed = int.from_bytes(
            hashlib.sha256(f"{self.seed}:{self.epoch}:{index}".encode()).digest()[:4],
            "little",
        )
        py_state = random.getstate()
        np_state = np.random.get_state()
        torch_state = torch.get_rng_state()
        try:
            random.seed(seed)
            np.random.seed(seed)
            # Dataset transforms are CPU-only. Do not alter CUDA model RNG streams.
            torch.random.default_generator.manual_seed(seed)
            return self.dataset[index]
        finally:
            random.setstate(py_state)
            np.random.set_state(np_state)
            torch.set_rng_state(torch_state)


def initialization_sha256(model):
    """Match train.py's existing fresh-initialization guard exactly."""
    digest = hashlib.sha256()
    for name, value in model.state_dict().items():
        digest.update(name.encode())
        digest.update(value.detach().cpu().numpy().tobytes())
    return digest.hexdigest()
