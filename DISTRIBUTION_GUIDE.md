# 🎯 游戏分发完整指南

## 📊 方案对比

| 方案 | 方便度 | 专业度 | 适合场景 | 推荐度 |
|------|--------|--------|----------|--------|
| 网页版 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 快速分享 | ⭐⭐⭐⭐⭐ |
| 可执行文件 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 作业提交 | ⭐⭐⭐⭐⭐ |
| itch.io | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 作品展示 | ⭐⭐⭐⭐ |
| GitHub Release | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 开源项目 | ⭐⭐⭐⭐ |
| 视频演示 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 补充说明 | ⭐⭐⭐ |

---

## 🎮 推荐方案：三位一体

### 给老师提供3种方式：

#### 1️⃣ 在线试玩（最方便）
```
🌐 https://jake-yutong.github.io/SlimeGobble/
```
老师打开浏览器就能玩，无需安装任何东西。

#### 2️⃣ 下载运行（体验最好）
```
📦 下载地址: https://github.com/Jake-yutong/SlimeGobble/releases
```
提供Windows和Mac版本，双击即玩。

#### 3️⃣ 查看源码（评分依据）
```
💻 源码地址: https://github.com/Jake-yutong/SlimeGobble
```
老师可以查看完整的开发历史和代码。

---

## 🛠️ 实现步骤

### 步骤1: 部署网页版（已准备好）

参考 `QUICK_DEPLOY.md` 完成部署。

完成后获得链接：`https://jake-yutong.github.io/SlimeGobble/`

---

### 步骤2: 打包可执行文件

#### 在Mac上打包Mac版本：

```bash
cd /Users/liyutong/Desktop/SlimeGobble
source venv/bin/activate

# 安装打包工具
pip install pyinstaller

# 运行打包脚本
chmod +x build_executable.sh
./build_executable.sh
```

生成的文件在 `dist/SlimeGobble.app`

#### 在Windows上打包Windows版本：

如果你有Windows电脑或虚拟机：

```bash
# 在Windows PowerShell或CMD中
cd C:\path\to\SlimeGobble
python -m venv venv
venv\Scripts\activate
pip install pygame numpy pyinstaller

# 打包
pyinstaller --name="SlimeGobble" ^
    --windowed ^
    --onefile ^
    --add-data="assets;assets" ^
    --noconfirm ^
    main.py
```

生成的文件在 `dist/SlimeGobble.exe`

---

### 步骤3: 发布到GitHub Releases

```bash
cd /Users/liyutong/Desktop/SlimeGobble

# 打包可执行文件为zip
cd dist
zip -r SlimeGobble-Mac.zip SlimeGobble.app
# 如果有Windows版本
# zip SlimeGobble-Windows.zip SlimeGobble.exe

# 返回项目目录
cd ..

# 创建版本标签
git tag -a v1.0.0 -m "SlimeGobble 第一版"
git push origin v1.0.0
```

然后：
1. 访问 https://github.com/Jake-yutong/SlimeGobble/releases
2. 点击 "Create a new release"
3. 选择刚才创建的标签 `v1.0.0`
4. 填写发布说明
5. 上传 `SlimeGobble-Mac.zip` 和 `SlimeGobble-Windows.zip`
6. 点击 "Publish release"

---

### 步骤4: 发布到itch.io（可选）

#### 4.1 注册账号
访问 https://itch.io/register

#### 4.2 创建新游戏
1. 点击右上角头像 → "Upload new project"
2. 填写基本信息：
   - **Title**: SlimeGobble
   - **Project URL**: slimegobble
   - **Short description**: 一款类似吃豆人的益智游戏
   - **Classification**: Games
   - **Kind of project**: HTML (网页版) 或 Downloadable (下载版)

#### 4.3 上传文件

**网页版：**
- 上传 `build/web` 文件夹内的所有文件
- 勾选 "This file will be played in the browser"

**下载版：**
- 上传 `SlimeGobble-Mac.zip`
- 上传 `SlimeGobble-Windows.zip`

#### 4.4 添加截图和描述

**游戏截图建议：**
- 主菜单
- 游戏进行中
- 关卡2/3展示
- 游戏胜利画面

**描述模板：**
```markdown
# SlimeGobble

一款受经典吃豆人启发的益智游戏。

## 🎮 游戏特色
- 3个独特关卡
- 智能敌人AI系统
- 流畅的操作体验
- 精美的像素风格

## 🕹️ 操作方式
- WASD: 移动
- P: 暂停
- ESC: 返回主菜单

## 🎯 游戏目标
每关收集500分即可进入下一关，完成第3关获胜！

## 🛠️ 技术栈
- Python 3.12
- Pygame
- 面向对象设计

---
Made with ❤️ by Jake-yutong
```

#### 4.5 发布设置
- **Visibility**: Public（公开）或 Restricted（限制访问）
- **Pricing**: Free（免费）

---

### 步骤5: 录制演示视频（可选）

**工具推荐：**
- Mac: QuickTime Player（系统自带）
- 跨平台: OBS Studio（免费）

**录制内容建议：**
1. 开场：显示游戏标题
2. 主菜单：展示UI
3. 关卡1：展示基础玩法
4. 关卡2：展示敌人追踪
5. 关卡3：展示高难度
6. 结尾：胜利画面

**Mac上录制：**
```bash
# 使用QuickTime Player
# 文件 → 新建屏幕录制 → 开始录制

# 或使用命令行（需要先安装ffmpeg）
brew install ffmpeg
ffmpeg -f avfoundation -i "1:0" -r 30 gameplay.mp4
```

上传到：
- YouTube（设置为"不公开"，只有链接的人能看）
- Bilibili
- 或直接嵌入到作业文档中

---

## 📝 作业提交建议

### 方式A: 简洁版（推荐）

创建一个 `README_SUBMISSION.md`：

```markdown
# SlimeGobble - 游戏作业提交

**学生:** 你的名字
**学号:** 你的学号
**日期:** 2025-10-23

## 🎮 试玩方式

### 方式1: 在线试玩（推荐）
🌐 https://jake-yutong.github.io/SlimeGobble/

打开即玩，无需安装。

### 方式2: 下载运行
📦 https://github.com/Jake-yutong/SlimeGobble/releases

提供Windows和Mac版本。

### 方式3: 查看源码
💻 https://github.com/Jake-yutong/SlimeGobble

完整的开发历史和代码。

## 📊 项目说明

- **开发语言:** Python 3.12
- **主要框架:** Pygame
- **开发工具:** VS Code, GitHub Codespaces
- **关卡数量:** 3关
- **特色功能:** 智能AI、流畅操作、渐进难度

## 📸 游戏截图

（插入截图）

## 🎥 演示视频

（可选：插入YouTube/Bilibili链接）
```

---

### 方式B: 完整版

除了上述内容，还包括：

1. **开发文档**
   - 设计思路
   - 技术架构
   - 遇到的问题和解决方案

2. **代码说明**
   - 主要类和函数的说明
   - 关键算法解释

3. **测试报告**
   - 功能测试结果
   - 兼容性测试

---

## 🎯 最终交付清单

- [ ] 网页版部署完成
- [ ] Mac可执行文件打包
- [ ] Windows可执行文件打包（如有条件）
- [ ] GitHub Release发布
- [ ] 游戏截图准备
- [ ] 演示视频录制（可选）
- [ ] itch.io发布（可选）
- [ ] 提交文档编写
- [ ] 源码整理和注释

---

## ⚠️ 注意事项

### 关于可执行文件

1. **Mac版本注意：**
   - 首次打开需要：右键 → 打开
   - 或在系统偏好设置 → 安全性 → 允许运行

2. **Windows版本注意：**
   - 可能被Windows Defender拦截
   - 说明：右键 → 属性 → 解除锁定

3. **文件大小：**
   - 单个可执行文件可能50-100MB
   - 建议压缩成zip分发

### 关于网页版

1. **浏览器兼容性：**
   - 推荐Chrome/Firefox
   - Safari可能有性能问题

2. **音效播放：**
   - 需要用户点击后才能播放
   - 这是浏览器安全限制

3. **移动设备：**
   - 可以访问但无法操作（需要键盘）

---

## 📞 需要帮助？

如果在打包或发布过程中遇到问题，告诉我：
1. 错误信息截图
2. 操作系统版本
3. Python版本
4. 具体在哪一步出错

我会帮你解决！
