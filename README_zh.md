# GCS-Pose

基于图条件化选择性状态空间建模的视频二维到三维人体姿态估计。

[English](README.md) · [模型与评测说明](docs/MODEL_CARD.md) · [数据](docs/DATA.md) · [权重](docs/WEIGHTS.md)

本实现基于PoseMamba及Mamba。姿态特征提供状态内容U和输出门控Z，骨架增强上下文提供Δ/B/C；空间与时间递推采用分解序列。实现类名保留为`GraphConditionedPoseMamba`以兼容权重。本项目为独立扩展，非上游官方发行版。

当前版本包含模型、训练评测入口、六组核心配置、安装检查与权重身份说明。原始数据、私有训练检查点及开发过程记录不随代码分发。

## 模型

Human3.6M检测二维输入，243帧，历史seed0 EMA。P1/P2单位mm；MAC-equivalent按单次片段前向统计，不含二维检测器和翻转测试。

| 模型 | 参数量 | P1 | P2 | MAC-equivalent |
|---|---:|---:|---:|---:|
| W64D8 | 800,083 | 39.845 | 33.232 | 4.602G |
| W128D10 | 3,435,395 | 38.484 | 32.383 | 18.739G |
| W128D20 | 6,836,355 | 37.659 | 31.872 | 37.474G |

以上为逐轮监测测试P1得到的最佳权重，不是独立验证集选点或固定80轮终点。W128D20历史上完成65/80计划轮数，表中权重为第45轮。统一的80轮配置不代表所有历史运行完成了80轮。单seed成绩不能证明稳定显著优势或跨检测器、跨域鲁棒性。完整协议与局限见模型卡。

## 安装与数据

使用Linux、Python3.10、NVIDIA CUDA及匹配的PyTorch/torchvision/nvcc。参考原生环境为PyTorch2.11.0+cu128。先安装CUDA PyTorch，再运行：

```bash
git clone https://github.com/Fubuyunhua/GCS-Pose.git
cd GCS-Pose
python -m pip install -r requirements.txt
bash scripts/build_selective_scan.sh
python scripts/verify_install.py
```

安装检查运行小规模CUDA前向/反向，不进行完整训练；原生Windows或CPU训练未经验证。Triton需与PyTorch匹配。

Human3.6M须自行合法获取。输入是SH检测器的xy/confidence，17关节，243帧，训练stride81。所需处理后数据布局见[数据说明](docs/DATA.md)。仅有原视频不足以复现相同预处理。

GT2D是单独协议：置信度设为1，评测使用输入已知XY，不可与检测输入下自由XYZ预测的数值混用。

## 训练与评测

```bash
# 检查数据布局并生成配置，不启动训练；输出目录必须是新目录。
python scripts/reproduce_gcspose.py --model w64d8 --protocol detector --data-root /path/to/DATA_ROOT --output runs/prepare_w64d8 --seed 0
# 从头训练。
CUDA_VISIBLE_DEVICES=0 python scripts/reproduce_gcspose.py --model w64d8 --protocol detector --data-root /path/to/DATA_ROOT --output runs/train_w64d8 --seed 0 --run
# 下载、核对并评测对应权重。
python scripts/download_weights.py --model w64d8 --protocol detector
CUDA_VISIBLE_DEVICES=0 python -X utf8 train.py --config runs/prepare_w64d8/config.yaml --evaluate weights/gcs_pose_w64d8_detector_ema.bin --checkpoint runs/evaluate_w64d8 --seed 0
```

可选模型为`w64d8/w128d10/w128d20`。GT2D需使用匹配配置和数据约定。布局检查不能替代数值预检；训练入口会为检查点目录追加时间戳。优化器、损失、EMA和预算由配置给出。

六份正式EMA导出见[当前仓库Release](https://github.com/Fubuyunhua/GCS-Pose/releases/tag/gcs-pose-v1.0)，SHA256见[清单](checkpoints/manifest.json)。代码中不包含令牌。导出仅有模型与最少身份信息，不含优化器状态和私有路径，不能恢复原优化器。

另一个 release [additional-ema-20261117](https://github.com/Fubuyunhua/GCS-Pose/releases/tag/additional-ema-20261117) 提供预登记配对实验 27 次运行的 54 份 EMA 导出（Human3.6M：输入融合、GCS-Pose、仅Δ seed 3–8，仅B/C seed 3–5；MPI-INF-3DHP：输入融合、GCS-Pose seed 3–5），每次运行有第 80 轮权重和逐轮监测测试集得到的最佳权重，并附每次运行的评测配置。其 `manifest.json` 给出每份导出对应的原始权重 SHA256，与 `results/paired_runs/fixed_endpoints.csv` 中的 `fixed_checkpoint_sha256` 对应。

评测保留翻转平均、反归一化、2.5D因子、骨盆中心化、原帧过滤及动作平均。返回数组中的有效预测可能已原位缩放，可视化时不要二次乘尺度。P2使用与P1相同的权重。

## 检查与许可

```bash
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -p 'test_*.py' -v
```

便携检查与CI不训练模型，也不替代真实CUDA安装验证。本模型为研究用途，未经医疗或安全决策验证。保留[许可证](LICENSE)、[NOTICE](NOTICE)与[第三方归属](docs/THIRD_PARTY_NOTICES.md)；数据及第三方条款分别适用。上游PoseMamba与Mamba引用信息见第三方说明。
