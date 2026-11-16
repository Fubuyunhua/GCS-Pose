# GCS-Pose

Graph-conditioned selective state-space modeling for video 2D-to-3D human pose estimation.

[中文](README_zh.md) · [Model card](docs/MODEL_CARD.md) · [Data](docs/DATA.md) · [Weights](docs/WEIGHTS.md) · [Results](results/README.md) · [Provenance](PROVENANCE.md)

The implementation builds on [PoseMamba](https://github.com/nankingjing/PoseMamba) and [Mamba](https://github.com/state-spaces/mamba). Pose features provide recurrent content U and output gate Z; skeleton-enhanced context provides selective parameters Δ/B/C. Spatial and temporal recurrence are factorized. The class name remains `GraphConditionedPoseMamba` for checkpoint compatibility. This is an independent implementation extension, not an official upstream release.

This source distribution includes the model, training and evaluation entry points, six core recipes, installation checks and checkpoint metadata. It does not distribute raw datasets, private training checkpoints or development-process records.

## Models

Human3.6M detected-2D input,243frames. Historical seed0 EMA checkpoints, selected by monitored test P1. P1/P2 are inmm; MAC-equivalent is per single forward clip, excluding the2D detector and flip testing.

| Model | Parameters | P1 | P2 | MAC-equivalent |
|---|---:|---:|---:|---:|
| W64D8 | 800,083 | 39.845 | 33.232 | 4.602G |
| W128D10 | 3,435,395 | 38.484 | 32.383 | 18.739G |
| W128D20 | 6,836,355 | 37.659 | 31.872 | 37.474G |

These are test-monitored best checkpoints, not independent-validation selections or fixed80 endpoints. W128D20 historically stopped at65of80planned epochs and its reported best isepoch45. The common80-epoch scratch recipes do not imply every historical run completed that budget. See the model card for the complete checkpoint and protocol disclosures. Single-seed scores do not establish statistically stable superiority or robustness across detectors and domains.

## Installation

Use Linux, Python3.10, NVIDIA CUDA, and compatible PyTorch/torchvision/nvcc. The reference native environment used PyTorch2.11.0+cu128. Install matching CUDA PyTorch first, then:

```bash
git clone https://github.com/Fubuyunhua/GCS-Pose.git
cd GCS-Pose
python -m pip install -r requirements.txt
bash scripts/build_selective_scan.sh
python scripts/verify_install.py
```

Keep Triton compatible with PyTorch. The installation check performs a small native CUDA forward/backward, not full training. Native Windows and CPU-only training are not validated.

## Data and protocols

Acquire Human3.6M separately under its data license. Required prepared-data layout and coordinate conventions are in [docs/DATA.md](docs/DATA.md). The2D inputs are Stacked Hourglass xy/confidence,17joints; training uses243-frame clips and stride81. Raw videos alone are insufficient to reproduce the supplied preprocessing.

Detector input and GT2D are separate protocols. GT2D replaces confidence withone and uses known inputXY during evaluation, so its scores cannot be compared directly with unconstrained detected-inputXYZ results.

## Training

The portable wrapper checks the layout, resolves one core recipe and records the command. Output directories must be new.

```bash
python scripts/reproduce_gcspose.py --model w64d8 --protocol detector --data-root /path/to/DATA_ROOT --output runs/prepare_w64d8 --seed 0
CUDA_VISIBLE_DEVICES=0 python scripts/reproduce_gcspose.py --model w64d8 --protocol detector --data-root /path/to/DATA_ROOT --output runs/train_w64d8 --seed 0 --run
```

Choose `w64d8`, `w128d10` or `w128d20`; use `--protocol gt2d` with its matching data convention. Layout checks are not a numerical training preflight. The trainer appends a timestamp to its checkpoint directory. Configuration files record the optimizer, losses, EMA and budget.

## Checkpoints and evaluation

```bash
python scripts/download_weights.py --model w64d8 --protocol detector
CUDA_VISIBLE_DEVICES=0 python -X utf8 train.py --config runs/prepare_w64d8/config.yaml --evaluate weights/gcs_pose_w64d8_detector_ema.bin --checkpoint runs/evaluate_w64d8 --seed 0
```

Six model-only EMA exports are available through this repository's [Release](https://github.com/Fubuyunhua/GCS-Pose/releases/tag/gcs-pose-v1.0). The downloader verifies the [manifest](checkpoints/manifest.json) SHA256. No access token is embedded in code. Exports omit optimizer states and private filesystem metadata and cannot resume the original optimizer.

The release [additional-ema-20261117](https://github.com/Fubuyunhua/GCS-Pose/releases/tag/additional-ema-20261117) provides 54 further model-only EMA exports from the 27 runs of the preregistered paired study (Human3.6M: input fusion, GCS-Pose and Δ-only seeds 3–8, B/C-only seeds 3–5; MPI-INF-3DHP: input fusion and GCS-Pose seeds 3–5). Each run has its fixed-epoch-80 checkpoint and its test-monitored best checkpoint, with one evaluation config per run. Its `manifest.json` links every export to the SHA256 of its source checkpoint, which `results/paired_runs/fixed_endpoints.csv` lists as `fixed_checkpoint_sha256`.

Evaluation retains native flip averaging, inverse normalization,2.5D factors, pelvis centering, frame filters and action aggregation. Returned evaluator arrays may already have been scaled in place; do not scale them a second time for visualizations. Report P2 from the same checkpoint as P1.

## Checks and attribution

```bash
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -p 'test_*.py' -v
```

Portable CI checks source/configuration consistency without model training; it does not certify CUDA compatibility on every device. Models are research artifacts, not validated medical or safety systems. Preserve [LICENSE](LICENSE), [NOTICE](NOTICE) and [third-party acknowledgments](docs/THIRD_PARTY_NOTICES.md). Dataset and other third-party terms are separate. Cite the underlying PoseMamba and Mamba work as described in the acknowledgments.
