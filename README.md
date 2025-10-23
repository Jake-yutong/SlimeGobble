# 🎮 SlimeGobble - 史莱姆大冒险

<div align="center">

[![Play Now](https://img.shields.io/badge/🎮_Play_Now-Online-success?style=for-the-badge)](https://jake-yutong.github.io/SlimeGobble/)
[![Python](https://img.shields.io/badge/Python-3.12+-blue?style=flat-square&logo=python)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.6.1-green?style=flat-square)](https://www.pygame.org/)
[![License](https://img.shields.io/badge/License-Educational-orange?style=flat-square)](LICENSE)

**一款基于 Pygame 开发的吃豆人风格游戏，包含 3 个关卡、AI 敌人、动画系统和完整的音效**

[🎮 立即开始游玩](#-在线游玩) • [📖 查看文档](#-项目结构) • [🚀 本地运行](#-本地运行)

</div>

---

## 🌐 在线游玩

**🎮 [点击这里在浏览器中游玩](https://jake-yutong.github.io/SlimeGobble/)**

无需安装，打开即玩！支持所有现代浏览器（Chrome、Firefox、Safari、Edge）。

## 🚀 本地运行

想在本地电脑上运行？只需三步：

```bash
# 1. 克隆仓库
git clone https://github.com/Jake-yutong/SlimeGobble.git
cd SlimeGobble

# 2. 创建虚拟环境并安装依赖
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install pygame numpy

# 3. 启动游戏
python main.py
```

### 系统要求
- Python 3.12 或更高版本
- macOS / Windows / Linux
- 支持 Pygame 的图形环境

## 🎯 Controls

| Key | Action |
|-----|--------|
| W | Move Up |
| A | Move Left |
| S | Move Down |
| D | Move Right |
| P | Pause/Resume |
| ESC | Return to Main Menu |

## 🎮 游戏玩法

### 游戏目标
控制可爱的史莱姆 "Mumu" 收集金币，达到 500 分即可进入下一关！

### 游戏元素
- 🪙 **小金币**：10 分
- 💰 **大金币**：50 分
- 👻 **追逐者（Chaser）**：碰到会失去 1 条生命
- ❤️ **生命系统**：3 条生命，用完游戏结束

### 关卡设计
- **第一关**：2 个 Random 敌人（随机移动）
- **第二关**：2 个 Chase 敌人（追踪玩家）+ 1 个 Fast Chase（快速追踪）
- **第三关**：3 个 Fast Chase 敌人（终极挑战！）

## 📁 项目结构

```
SlimeGobble/
├── 📄 核心代码
│   ├── main.py          # 游戏入口（支持 Web 异步）
│   ├── game.py          # 游戏主逻辑和状态管理
│   ├── player.py        # 玩家角色类（动画系统）
│   ├── enemy.py         # 敌人 AI 系统（3种行为模式）
│   └── config.py        # 游戏配置和关卡地图
│
├── 🎨 游戏素材
│   └── assets/          # 精灵图、音效、JSON 动画文件
│       ├── slime *.png/json    # 玩家动画（4方向）
│       ├── Chaser *.png        # 敌人图像（4方向）
│       ├── coin.png, big coin.png
│       └── *.wav               # 背景音乐和音效
│
├── 🚀 部署相关
│   ├── deploy_web.sh    # 自动化部署脚本
│   ├── build_executable.sh
│   └── WEB_DEPLOYMENT.md
│
├── 📚 文档
│   ├── README.md        # 本文件
│   ├── DEVELOPMENT.md   # 开发文档
│   ├── SUBMISSION.md    # 作业提交说明
│   └── PHASE1_SUMMARY.md
│
└── 🧪 测试
    └── test_phase1.py   # 自动化测试
```

## ✨ 技术特性

### 核心系统
- 🎯 **完整的游戏状态机**：主菜单、游戏中、暂停、胜利、失败
- 🎨 **帧动画系统**：基于 JSON 配置的精灵动画
- 🤖 **智能敌人 AI**：三种行为模式（随机、追踪、快速追踪）
- 🎵 **音效系统**：背景音乐、金币收集、胜利/失败音效
- 💾 **关卡系统**：3 个关卡，难度递增

### Web 部署
- 🌐 **WebAssembly 转换**：使用 Pygbag 转换为浏览器可运行版本
- 📦 **GitHub Pages 托管**：免费、稳定、全球 CDN 加速
- ⚡ **异步游戏循环**：专为浏览器优化的事件循环

## 📊 开发历程

| 阶段 | 状态 | 内容 |
|------|------|------|
| **Phase 1** | ✅ 完成 | 游戏框架、玩家控制、关卡 1 |
| **Phase 2** | ✅ 完成 | 敌人 AI、生命系统、音效、完整 3 关 |
| **Web 部署** | ✅ 完成 | Pygbag 转换、GitHub Pages 上线 |

## 📚 相关文档

- 📖 [开发文档 (DEVELOPMENT.md)](DEVELOPMENT.md) - 技术实现细节
- 📝 [作业提交说明 (SUBMISSION.md)](SUBMISSION.md) - 完整提交材料
- 🚀 [Web 部署指南 (WEB_DEPLOYMENT.md)](WEB_DEPLOYMENT.md) - 部署教程
- 📋 [Phase 1 总结 (PHASE1_SUMMARY.md)](PHASE1_SUMMARY.md) - 第一阶段报告

## 🧪 测试

运行自动化测试验证实现：

```bash
python test_phase1.py
```

## 🤝 作者

**Jake Yutong** - [@Jake-yutong](https://github.com/Jake-yutong)

## 📝 许可证

本项目仅用于教育目的。

---

<div align="center">

**🎮 [立即开始游玩](https://jake-yutong.github.io/SlimeGobble/) • 收集金币，躲避追逐者！**

Made with ❤️ using Python & Pygame

</div>
