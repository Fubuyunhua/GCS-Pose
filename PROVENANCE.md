# Provenance and development timeline

This repository is a single-commit source release of GCS-Pose. The development
repository (all commits, preregistration documents, run logs and code review) is
private. This file lists identifiers that link this release to it. Editors and
reviewers can obtain the originals on request and check them against the commit
IDs and SHA256 values below.

"Server" times were recorded by GitHub when the event happened; the author cannot
set them. Commit times are set by the author's machine and are given only to
identify commits.

## Public period of the development repository

| Event | Server time (UTC) | Source |
|---|---|---|
| Repository created | 2026-09-02 13:12 | GitHub repository metadata |
| Visibility changed from private to public | 2026-09-02 13:21 | account security log, `repo.access` |
| Visibility changed from public to private | 2026-10-29 10:07 | account security log, `repo.access` |

The exported security-log entries are available on request.

## Original code and checkpoint release

| Event | Identifier | Time |
|---|---|---|
| Source of release `gcs-pose-v1.0` | commit `314782b894cda78b224270c4003f59a474c649d8` | commit time 2026-09-17 12:22 (UTC+8) |
| GitHub release `gcs-pose-v1.0` with six EMA checkpoints | release published (`published_at`) | server 2026-09-17 04:36 UTC |
| First submission of the manuscript to IEEE Signal Processing Letters | journal record | 2026-09-17 |

The release was published while the repository was public. The six checkpoint
files are distributed again with this repository, byte-identical (the download
URLs in `checkpoints/manifest.json` were changed, so that file differs):

| File | SHA256 |
|---|---|
| `gcs_pose_w64d8_detector_ema.bin` | `029774a1dd8e67fa2b1aef14cf0f835a4d8e30f5fa708cc117c7b9698ee18b1b` |
| `gcs_pose_w128d10_detector_ema.bin` | `922aafed458ea1f5e3d4ede4104f9538a1f4dc3b7c999c9463b8d302c8f5df4a` |
| `gcs_pose_w128d20_detector_ema.bin` | `41095be7d84fe3bc7d355dc10a69a1a482e4d701719751a97f54bf3b8bea9c8e` |
| `gcs_pose_w64d8_gt2d_ema.bin` | `53d92d13a1cd2e8397f7bb15971cf6c131d6b2632172b45fdea74264d2c8923b` |
| `gcs_pose_w128d10_gt2d_ema.bin` | `3d968eb64a9438e1d1259360943b6decb4feee6bdb661e8149fba63b2b22a5da` |
| `gcs_pose_w128d20_gt2d_ema.bin` | `fa74b10e1eae29fc94b22cb9d565dfd9932c35e99c24cd98faa6612238e3db37` |

These are historical seed-0 checkpoints selected by monitored test P1. They are
not the fixed-epoch-80 checkpoints of the preregistered paired study.

## Paired-study checkpoints

| Event | Identifier |
|---|---|
| Training runs | execution commit `52d0e58e9fbc5520cc3ab23b2fa9a7db3a12970a` (see below) |
| Model-only exports | release [additional-ema-20261117](https://github.com/Fubuyunhua/GCS-Pose/releases/tag/additional-ema-20261117) |

The 27 runs of the preregistered paired study are distributed as 54 model-only
EMA exports (fixed epoch 80 and test-monitored best for each run). The release
`manifest.json` gives, for every export, the SHA256 of the original training
checkpoint; for the fixed-epoch-80 exports these equal `fixed_checkpoint_sha256`
in `results/paired_runs/fixed_endpoints.csv`. The original checkpoints are
archived privately and are available on request.

## Preregistrations

Each document was first committed on a branch and opened as a pull request in the
development repository. SHA256 is of the file as first committed. A pull-request
time shows that the pull request existed at that time; that it preceded the
analysis is shown by the execution commits and run records, available on request.
The first document was opened while the repository was public.

| Analysis | Document (private repository) | First commit | Pull request, opened (server, UTC) | SHA256 |
|---|---|---|---|---|
| Paired clean-input comparison (27 runs) | `docs/PREREGISTRATION_RESUBMISSION.md` | `cd92d866220d376ca90c084805c9a7720a2ea1e1` | #9, 2026-10-29 04:41 | `27200249afdc80fc71890d5a0e8a64d2e6bc8ce828e8feec6c02e64fe46b8be8` |
| Synthetic input perturbations | `docs/ROBUSTNESS_PREREG_20261110.md` | `d17079cb8d5a6925e3b7c8dceceb8baaddb6e6f4` | #11, 2026-11-10 08:11 | `824cfc9284ce9d10b2d6737c2ee7b430082f173b3a76d34c94f35254187684ae` |
| MPI-INF-3DHP perturbations | `docs/MPI_ROBUSTNESS_PREREG_20261115.md` | `f2b2b59e822cbf51898396469426ec3473881005` | #14, 2026-11-15 01:08 | `e9fc832aa6cb08e060bce4237038cc9641a99f3c4aa7697507fd41ef57527d0e` |
| Detector-error strata | `docs/DETECTOR_ERROR_PREREG_20261115.md` | `94893875752cb67129f18c706778ad0a027754a4` | #16, 2026-11-15 05:16 | `7dfe7ac1c411c9b18eb415b3ddbdce0b77bf8be4829ff9228cf409854d0f64e7` |
| Single-limb noise propagation | `docs/PROPAGATION_PREREG_20261116.md` | `abad062d6ffbf1945159f225793bd558534ec7bd` | #20, 2026-11-16 03:11 | `3f084d1c23511b76ca1f77f893a41eb6646ac449076e874d730f4c0a8862eae5` |
| Propagation evaluation specification | `docs/PROPAGATION_EVAL_SPEC_20261116.md` | `abad062d6ffbf1945159f225793bd558534ec7bd` | #20, 2026-11-16 03:11 | `1d3a50c55be1255ab9294011c2fcc25afdb382c2a866dc5bf0efd00027ae3c4d` |

## Execution sources

| Study | Commit | Tag |
|---|---|---|
| Preregistered training runs | `52d0e58e9fbc5520cc3ab23b2fa9a7db3a12970a` | `resubmission-execution-20261029` |
| Synthetic perturbation evaluation | `686eeb7b7aa9f79c7ba6b64bad649719513f429b` | `robustness-execution-3080ti-20261110` |

The files under `lib/model` and `kernels` in this release are identical to those
at both commits. Other parts of the execution environment (training entry points,
evaluation scripts, run configuration) are not all included here.
