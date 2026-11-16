# Result tables

Numeric results of the preregistered studies in the paper, exported from the run
records of the private development repository (see [PROVENANCE.md](../PROVENANCE.md)).
Values are copied without rounding; only columns were selected. Run logs,
preregistration documents and execution records are available on request.

All errors are in millimetres. P1 is MPJPE; P2 is P-MPJPE from the same checkpoint.
Coordinate-noise levels are standard deviations in normalised 2D coordinates. On
Human3.6M one unit is 500 pixels, so 0.01, 0.02, 0.04 and 0.08 are 5, 10, 20 and
40 pixels.

## Route names

| Name in files | Paper |
|---|---|
| `full`, `Full_HQ` | GCS-Pose: U and Z from H; Δ, B and C from Q |
| `a2`, `A2_QQ` | Input fusion: all five from Q |
| `delta` | Δ-only |
| `bc` | B/C-only |
| `A1` | No graph |
| `adapted_PoseMamba`, `PoseMamba_790083_legacy`, `posemamba_ref` | PoseMamba adapted to this pipeline |
| `gcs_ref`, `GCS_best_seed0` | Historical seed-0 GCS-Pose checkpoint (test-monitored best) |

Checkpoint IDs have the form `<dataset>_<route>_s<seed>[_fixed80]`. Seeds 3–8 are the
preregistered paired runs; seed 0 is historical.

## Files

| Folder | File | Content |
|---|---|---|
| `paired_runs` | `fixed_endpoints.csv` | 27 preregistered runs. Primary endpoint: EMA checkpoint at epoch 80 (`fixed80_*`). Secondary: epoch with the lowest test P1 (`test_monitored_best_*`, P2 taken at that same epoch) and mean P1 of epochs 71–80. PCK/AUC only for MPI-INF-3DHP. |
| | `epoch_metrics.csv` | Per-epoch EMA and raw P1/P2 (and PCK/AUC on MPI-INF-3DHP) of the same runs. |
| `perturbation_h36m` | `per_condition.csv` | Fixed-epoch-80 checkpoints of input fusion, GCS-Pose and Δ-only (seeds 3–8) under C1 coordinate noise, C2 joint removal, C3 limb removal, C4 confidence changes. `degradation_p1_mm` = P1 − clean P1 of the same checkpoint. |
| | `condition_means.csv` | Means and sample SD over seeds. |
| | `primary_paired_auc.csv` | Primary endpoint per seed: area under the C1 degradation curve, input fusion minus GCS-Pose. |
| `propagation` | `group_results.csv` | Gaussian noise on one three-joint limb at a time. Errors of the perturbed, graph-adjacent, other and all unperturbed joints, before and after noise. |
| | `per_joint_errors.csv` | Per-joint P1 (`j0`–`j16`) and P2 (`p2_j0`–`p2_j16`) for every checkpoint, limb and level; `level` 0 is clean. |
| | `method_level_means.csv` | Means over seeds and limbs (noise in pixels). |
| | `primary_paired_auc.csv` | Primary endpoint per seed: area under the unperturbed-joint degradation curve, input fusion minus GCS-Pose. |
| `detector_error` | `stratum_results.csv` | Clean-input P1/P2 within strata of the real 2D detection error (quartiles by frame, clip, joint and confidence; top decile). |
| | `condition_means.csv` | Means and sample SD over seeds. |
| `perturbation_mpi3dhp` | `per_condition.csv` | Fixed-epoch-80 checkpoints of input fusion and GCS-Pose (seeds 3–5) on MPI-INF-3DHP under the same perturbation families. |
| | `condition_means.csv` | Means and sample SD over seeds. |
| `efficiency` | `latency_summary.csv` | Forward time (ms, median and 95th percentile; CUDA and wall clock) and peak allocated memory (MiB) on one RTX 3080 Ti, batch 1 and 4, with and without flip. |
| | `latency_repeats.csv`, `latency_samples.csv` | Per-repeat medians and every timed forward. |
| | `complexity.csv` | Parameter count and MAC equivalents per clip; `corrected_*` includes the selective scan, `vanilla_thop_macs` does not. |
| `supplement_perturbation` | `posemamba_results.csv`, `gcs_best_results.csv` | Historical seed-0 adapted PoseMamba and GCS-Pose checkpoints under the same perturbations, six input draws each (one trained model each, not six). |
| | `posemamba_condition_comparison.csv`, `bestpair_comparison.csv` | Condition means and differences. |

`weight_sha256` identifies the evaluated checkpoint and `input_sha256` the perturbed
input, so rows of different routes can be paired on identical inputs.

SHA256 of every file is in [SHA256SUMS](SHA256SUMS).
