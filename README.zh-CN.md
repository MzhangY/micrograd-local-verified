# micrograd：本地验证与中文快速上手

> 原作者：Andrej Karpathy。原仓库：https://github.com/karpathy/micrograd
> 本仓库为学习与本地验证版本，不是原创重写；保留完整上游历史、README 和 MIT LICENSE。

## 这个 AI 项目做什么？

micrograd 用很短的 Python 代码实现标量自动求导，并在其上实现神经元、全连接层和多层感知机（MLP）。适合学习反向传播和神经网络训练，不是聊天机器人或大语言模型。

本次新增一个 **CPU 上从零训练 XOR 分类器** 的可运行演示。演示只用标准库和本项目，不需要显卡、付费服务、API Key 或下载模型。

## 一键验证（Windows PowerShell，Python 3.13）

在本仓库根目录运行：

```powershell
.\verify_local.ps1 -InstallDependencies
```

脚本会建立独立 `.venv`，按 `requirements-local.txt` 安装测试依赖，然后运行训练演示与测试。PyTorch 仅用于与上游自动求导测试对照，演示自身不依赖 PyTorch。

如果只想运行无第三方依赖的训练演示，在仓库根目录执行：

```powershell
python local_demo.py
```

## 2026-11-20 本机实测

- 环境：Windows 11、Python 3.13.5、CPU；PyTorch 2.14.1，pytest 8.3.4。
- 上游基线：`7bc720e951fe422b8f8814aa5aa1b64121d26b4c`。
- 上游 2 项测试 + 新增 5 项测试：**7 passed，0 failed，0 skipped**。
- XOR：105 个参数，固定随机种子 42，400 步；4/4 训练样本分类正确。
- 均方误差从 **0.96497558** 降至 **7.2090e-08**。
- 这是 4 个 XOR 样本上的训练结果，不代表真实数据上的泛化能力。

## 本次修改

1. 修复 `setup.py` 未指定 UTF-8 导致中文 Windows 默认 GBK 读取 README 安装失败的问题。
2. 增加 `local_demo.py`、`test/test_local_validation.py`。
3. 增加精确验证依赖清单和 `verify_local.ps1`。
4. 增加 `verification/` 原始测试与演示结果（已去除本机路径和主机名）。

## 验证证据

- `verification/pytest.log`：测试结果。
- `verification/junit.xml`：机器可读测试报告。
- `verification/demo.json`：训练轨迹和预测。
- `verification/environment.json`：Python、依赖版本与上游提交。

仅验证了这一台 Windows / Python / CPU 环境；未宣称完成安全审计、多平台兼容性认证、GPU 测试或生产部署。
