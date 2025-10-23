# 👨‍🏫 教师评审指南

## 🎮 快速试玩

**在线游玩链接：** https://jake-yutong.github.io/SlimeGobble/

- ✅ 无需安装，打开即玩
- ✅ 支持所有现代浏览器
- ✅ 完整游戏体验（3 个关卡）

**操作说明：**
- **WASD** - 移动
- **P** - 暂停
- **ESC** - 返回主菜单

---

## 📂 源码查看

**GitHub 仓库：** https://github.com/Jake-yutong/SlimeGobble

### 核心代码文件
点击下方链接直接查看源码：

1. **[main.py](https://github.com/Jake-yutong/SlimeGobble/blob/main/main.py)** - 游戏入口（40 行）
   - Web 异步支持
   
2. **[game.py](https://github.com/Jake-yutong/SlimeGobble/blob/main/game.py)** - 游戏主逻辑（560 行）
   - 状态机管理（6 个状态）
   - 关卡系统
   - 碰撞检测
   - HUD 显示
   
3. **[player.py](https://github.com/Jake-yutong/SlimeGobble/blob/main/player.py)** - 玩家控制（280 行）
   - 帧动画系统
   - 移动逻辑
   - 自动对齐
   
4. **[enemy.py](https://github.com/Jake-yutong/SlimeGobble/blob/main/enemy.py)** - 敌人 AI（290 行）
   - Random AI（随机移动）
   - Chase AI（追踪玩家）
   - Fast Chase AI（快速追踪）
   
5. **[config.py](https://github.com/Jake-yutong/SlimeGobble/blob/main/config.py)** - 游戏配置（150 行）
   - 3 个关卡地图定义
   - 游戏参数配置

### 游戏素材
- **[assets/](https://github.com/Jake-yutong/SlimeGobble/tree/main/assets)** - 20 个素材文件
  - 玩家动画（4 方向，8 帧）
  - 敌人图像（4 方向）
  - 音效文件（BGM、金币、胜利/失败）

---

## 📊 项目统计

| 指标 | 数值 |
|------|------|
| **总代码行数** | 1,320 行 |
| **核心文件数** | 5 个 |
| **游戏素材** | 20 个文件 |
| **关卡数量** | 3 关 |
| **AI 类型** | 3 种 |
| **测试覆盖** | 基础测试完成 |

---

## ✨ 技术亮点

### 1. 完整的游戏系统
- ✅ 状态机管理（主菜单、游戏中、暂停、胜利、失败）
- ✅ 3 个关卡，难度递增
- ✅ 生命系统和得分系统
- ✅ HUD 界面显示

### 2. 智能 AI 系统
- ✅ 3 种敌人行为模式
- ✅ 曼哈顿距离算法追踪
- ✅ 混合策略（游荡+追击）

### 3. 动画与音效
- ✅ 基于 JSON 的帧动画系统
- ✅ 4 方向动画切换
- ✅ 完整的音效系统

### 4. Web 部署
- ✅ Pygbag 转换为 WebAssembly
- ✅ GitHub Pages 托管
- ✅ 长期有效的在线访问

---

## 📝 评审建议

### 代码质量
- ✅ 模块化设计（MVC 架构）
- ✅ 清晰的注释和文档
- ✅ 一致的代码风格
- ✅ 异常处理

### 游戏设计
- ✅ 渐进式难度曲线
- ✅ 流畅的操作体验
- ✅ 完整的反馈系统
- ✅ 友好的用户界面

### 创新点
- ✅ Web 部署（超出基本要求）
- ✅ 3 种 AI 行为模式
- ✅ 帧动画系统
- ✅ 完整的音效系统

---

## 📚 相关文档

- **[README.md](https://github.com/Jake-yutong/SlimeGobble/blob/main/README.md)** - 项目主文档
- **[SUBMISSION.md](https://github.com/Jake-yutong/SlimeGobble/blob/main/SUBMISSION.md)** - 详细提交说明
- **[DEVELOPMENT.md](https://github.com/Jake-yutong/SlimeGobble/blob/main/DEVELOPMENT.md)** - 开发文档

---

## ⏱️ 建议评审流程

1. **试玩游戏（5 分钟）**
   - 打开 https://jake-yutong.github.io/SlimeGobble/
   - 完成至少 1 个关卡
   - 体验 AI 行为和游戏机制

2. **查看核心代码（10 分钟）**
   - 浏览 game.py 的状态机实现
   - 查看 enemy.py 的 AI 算法
   - 检查代码质量和注释

3. **评估项目完成度（5 分钟）**
   - 功能完整性
   - 代码质量
   - 文档完善度
   - 创新点

**总计：约 20 分钟完成评审**

---

## 📧 联系方式

**学生：** Jake Yutong  
**GitHub：** [@Jake-yutong](https://github.com/Jake-yutong)  
**项目仓库：** https://github.com/Jake-yutong/SlimeGobble

---

<div align="center">

**感谢您的评审！**

🎮 [立即游玩](https://jake-yutong.github.io/SlimeGobble/) | 📂 [查看源码](https://github.com/Jake-yutong/SlimeGobble)

</div>
