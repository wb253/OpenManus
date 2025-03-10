[English](README.md) | 中文

[![GitHub stars](https://img.shields.io/github/stars/mannaandpoem/OpenManus?style=social)](https://github.com/gregpr07/browser-use/stargazers) &ensp;
[![Twitter Follow](https://img.shields.io/twitter/follow/openmanus?style=social)](https://twitter.com/openmanus) &ensp;
[![Discord Follow](https://dcbadge.vercel.app/api/server/https://discord.gg/6dn7Sa3a?style=flat)](https://discord.gg/6dn7Sa3a) &ensp;
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# 👋 OpenManus

Manus 非常棒，但 OpenManus 无需邀请码即可实现任何创意 🛫！

我们的团队成员 [@mannaandpoem](https://github.com/mannaandpoem) [@XiangJinyu](https://github.com/XiangJinyu) [@MoshiQAQ](https://github.com/MoshiQAQ) [@didiforgithub](https://github.com/didiforgithub) https://github.com/stellaHSR
和 [@Xinyu Zhang](https://x.com/xinyzng) 来自 [@MetaGPT](https://github.com/geekan/MetaGPT) 等组织，我们在 3
小时内完成了原型开发并持续迭代中！

感谢 MetaGPT 团队提供的 OpenManus 基础框架。

用 OpenManus 开启你的智能体之旅吧！

我们也非常高兴地向大家介绍 [OpenManus-RL](https://github.com/OpenManus/OpenManus-RL)，这是一个专注于基于强化学习（RL，例如 GRPO）的方法来优化大语言模型（LLM）智能体的开源项目，由来自UIUC 和 OpenManus 的研究人员合作开发。

## 项目演示

<img src="assets/webapp.png" alt="OpenManus Web App" width="800" />

## 安装指南

我们提供两种安装方式。推荐使用方式二（uv），因为它能提供更快的安装速度和更好的依赖管理。

### 方式一：使用 conda

1. 创建新的 conda 环境：

```bash
conda create -n open_manus python=3.12
conda activate open_manus
```

2. 克隆仓库：

```bash
git clone https://github.com/mannaandpoem/OpenManus.git
cd OpenManus
```

3. 安装依赖：

```bash
pip install -r requirements.txt
```

### 方式二：使用 uv（推荐）

1. 安装 uv（一个快速的 Python 包管理器）：

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. 克隆仓库：

```bash
git clone https://github.com/mannaandpoem/OpenManus.git
cd OpenManus
```

3. 创建并激活虚拟环境：

```bash
uv venv
source .venv/bin/activate  # Unix/macOS 系统
# Windows 系统使用：
# .venv\Scripts\activate
```

4. 安装依赖：

```bash
uv pip install -r requirements.txt
```

## 配置说明

OpenManus 需要配置使用的 LLM API，请按以下步骤设置：

1. 在 `config` 目录创建 `config.toml` 文件（可从示例复制）：

```bash
cp config/config.example.toml config/config.toml
```

2. 编辑 `config/config.toml` 添加 API 密钥和自定义设置：

```toml
# 全局 LLM 配置
[llm]
model = "gpt-4o"
base_url = "https://api.openai.com/v1"
api_key = "sk-..."  # 替换为真实 API 密钥
max_tokens = 4096
temperature = 0.0

# 可选特定 LLM 模型配置
[llm.vision]
model = "gpt-4o"
base_url = "https://api.openai.com/v1"
api_key = "sk-..."  # 替换为真实 API 密钥
```

## 快速启动

一行命令运行 OpenManus：

```bash
python main.py
```

### Web 界面模式
体验由 **云栖AI** 开发的全新Web交互界面：

```bash
python main.py --web
# 或直接使用
python web_run.py
```

Web界面让您可以通过浏览器直观地与OpenManus交流，更加便捷地实现您的创意！

如需体验开发中版本，可运行：

```bash
python run_flow.py
```

## 贡献指南

我们欢迎任何友好的建议和有价值的贡献！可以直接创建 issue 或提交 pull request。

或通过 📧 邮件联系 @mannaandpoem：mannaandpoem@gmail.com

## 发展路线

在全面收集了社区成员的反馈后，我们决定采用 3-4 天为周期的迭代模式，逐步实现大家期待的功能。

- [ ] 增强 Planning 能力，优化任务分解和执行逻辑
- [ ] 引入标准化评测，基于 GAIA 和 TAU-Bench，持续评估并优化性能
- [ ] 拓展模型适配，优化低成本应用场景
- [ ] 实现容器化部署，简化安装和使用流程
- [ ] 丰富示例库，增加更多实用案例，包含成功和失败示例的分析
- [ ] 前后端开发，提供用户体验

## 交流群

加入我们的飞书交流群，与其他开发者分享经验！

<div align="center" style="display: flex; gap: 20px;">
    <img src="assets/community_group.jpg" alt="OpenManus 交流群" width="300" />
</div>

## Star 数量

[![Star History Chart](https://api.star-history.com/svg?repos=mannaandpoem/OpenManus&type=Date)](https://star-history.com/#mannaandpoem/OpenManus&Date)

## 致谢

特别感谢 [anthropic-computer-use](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo)
和 [browser-use](https://github.com/browser-use/browser-use) 为本项目提供的基础支持！

OpenManus 由 **云栖AI** 基于 MetaGPT 社区的框架共同构建，感谢这个充满活力的智能体开发者社区！
