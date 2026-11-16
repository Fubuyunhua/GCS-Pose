# Core checkpoints

Six EMA checkpoints are prepared for the three core models and separate detector/
GT2D protocols. They retain model tensors exactly while omitting optimizer states,
training logs and private filesystem metadata. Original checkpoints are archived
privately. The public manifest records SHA256, architecture, protocol and epoch.

Download from [GCS-Pose core weights](https://github.com/Fubuyunhua/GCS-Pose/releases/tag/gcs-pose-v1.0).
The [manifest](../checkpoints/manifest.json) records sizes, SHA256 hashes, epochs,
and input protocols. The downloader verifies both file size and SHA256:

```bash
python scripts/download_weights.py --model w128d20 --protocol detector
```

Use `--protocol gt2d` only with the matching GT configuration. All six exports
passed exact tensor roundtrip and strict loading against the public model code.
Only model state and minimal identity metadata are included; there is no optimizer
state for resuming the original training. Read the model card before comparing scores.

## Paired-study checkpoints

The release [additional-ema-20261117](https://github.com/Fubuyunhua/GCS-Pose/releases/tag/additional-ema-20261117) holds 54 model-only EMA exports
from the 27 runs of the preregistered paired study, in two archives:

- Human3.6M (SH detector xy/confidence, 243 frames): input fusion (`a2`), GCS-Pose
  (`full`) and Delta-only (`delta`) seeds 3-8; B/C-only (`bc`) seeds 3-5.
- MPI-INF-3DHP (GT2D, confidence 1, 81 frames): `a2` and `full` seeds 3-5.

Each run provides its fixed-epoch-80 checkpoint (the preregistered primary
endpoint) and its test-monitored best checkpoint, plus one evaluation config.
The release `manifest.json` records each export's SHA256, size, epoch, selection
and the SHA256 of its source checkpoint; for the fixed-epoch-80 exports the latter
equals `fixed_checkpoint_sha256` in `results/paired_runs/fixed_endpoints.csv`.
The archive `README.md` gives the evaluation commands. These exports cannot resume
training and do not replace the six core checkpoints above.
