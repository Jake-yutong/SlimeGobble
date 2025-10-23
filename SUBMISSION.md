# 🎮 SlimeGobble - 作业提交文档

<div align="center">

**开发者:** Jake Yutong ([@Jake-yutong](https://github.com/Jake-yutong))  
**项目类型:** Python 游戏开发 (Pygame)  
**开发时间:** 2025年10月  
**仓库地址:** https://github.com/Jake-yutong/SlimeGobble

[![Play Online](https://img.shields.io/badge/🎮_在线游玩-立即开始-success?style=for-the-badge)](https://jake-yutong.github.io/SlimeGobble/)

</div>

---

## � 快速试玩

### 🌐 在线游玩（推荐）

**� [点击这里在浏览器中游玩](https://jake-yutong.github.io/SlimeGobble/)**

- ✅ **无需安装**，打开即玩
- ✅ 支持所有现代浏览器（Chrome、Firefox、Safari、Edge）
- ✅ 支持 Windows、Mac、Linux 任何平台
- ✅ 长期有效，随时可访问

**操作说明:**
1. 点击上方链接打开游戏
2. 等待游戏加载（约 5-10 秒）
3. 点击 "Start" 按钮开始游戏
4. 使用 **WASD** 键控制角色移动

---

## � 查看源码

### GitHub 仓库

```
💻 GitHub仓库: https://github.com/Jake-yutong/SlimeGobble
```

- 完整的源代码
- 开发历史和提交记录
- 项目文档和说明

**本地运行方法:**
```bash
git clone https://github.com/Jake-yutong/SlimeGobble.git
```bash
git clone https://github.com/Jake-yutong/SlimeGobble.git
cd SlimeGobble
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install pygame numpy
python main.py
```

---

## 📖 游戏介绍

### 🎯 游戏概述
**SlimeGobble** 是一款受经典吃豆人启发的 2D 动作益智游戏。玩家控制可爱的史莱姆 "Mumu" 在迷宫中收集金币，同时躲避智能追逐者（Chaser）。游戏包含 **3 个关卡**，难度递增，配有完整的音效系统和帧动画。

### 🏆 游戏目标
- 🪙 每关收集 **500 分**即可进入下一关
- 🎮 完成全部 **3 关**获得胜利
- ❤️ 避免被敌人抓到（共有 3 条命）

### 操作方式
| 按键 | 功能 |
|------|------|
| W/A/S/D | 上/左/下/右移动 |
| P | 暂停/继续 |
| ESC | 返回主菜单 |
| SPACE | 下一关/重试 |
| R | 重新开始 |

### 游戏机制

**金币系统:**
- 小金币（黄点）: 10分/个
- 大金币（大圆圈）: 50分/个
- 目标分数: 500分/关

**敌人 AI 系统:**
- **关卡 1:** 2 个 Random 敌人（随机移动，速度慢）
- **关卡 2:** 2 个 Chase 敌人 + 1 个 Fast Chase 敌人（追踪玩家，速度递增）
- **关卡 3:** 3 个 Fast Chase 敌人（高速追踪，终极挑战）

**生命系统:**
- 初始 3 条命（屏幕右上角显示）
- 被敌人碰到失去 1 条命并短暂无敌
- 失去所有生命则游戏结束

---

## ✨ 技术亮点

### 🎨 1. 完整的帧动画系统
- 基于 JSON 配置的精灵动画
- 支持 4 方向动画（上下左右）
- 流畅的帧切换效果（8帧/动画）

### 🤖 2. 智能敌人 AI（3种行为模式）
- **Random AI:** 随机游荡，适合新手关卡
- **Chase AI:** 追踪玩家，使用曼哈顿距离算法
- **Fast Chase AI:** 高速追踪，终极挑战
- **混合策略:** 远离时游荡，接近时追击

### 🎮 3. 流畅的操作体验
- 自动转弯对齐系统（像素级精确）
- 墙壁滑动效果（6px 容差）
- 精确的碰撞检测（AABB 算法）
- 短暂无敌时间（被击中后）

### 🎵 4. 完整的音效系统
- 背景音乐循环播放
- 金币收集音效（小金币/大金币不同）
- 关卡胜利/失败音效
- 按键反馈音效

### 🌐 5. Web 部署技术
- **Pygbag:** Python 游戏转 WebAssembly
- **GitHub Pages:** 免费托管，全球 CDN
- **异步游戏循环:** 浏览器优化

---

## 🛠️ 技术实现

### 开发环境
- **编程语言:** Python 3.12
- **主要框架:** Pygame 2.6.1
- **辅助库:** NumPy 2.3.4
- **开发工具:** VS Code, GitHub Codespaces
- **版本控制:** Git + GitHub

### 核心文件说明

| 文件 | 行数 | 功能描述 |
|------|------|---------|
| `main.py` | 40 | 游戏入口，支持 Web 异步运行 |
| `game.py` | 560 | 游戏主逻辑、状态机、关卡管理 |
| `player.py` | 280 | 玩家类、动画系统、移动逻辑 |
| `enemy.py` | 290 | 敌人 AI、三种行为模式 |
| `config.py` | 150 | 游戏配置、3 个关卡地图定义 |

**总代码量:** 约 1,320 行（不含注释和文档）

### 核心类设计

#### Game类（游戏管理器）
```python
class Game:
    - 状态管理: 主菜单/游戏/暂停/完成/胜利/失败
    - 关卡管理: 加载地图、生成敌人、管理金币
    - 碰撞检测: 玩家-金币、玩家-敌人
    - 音效系统: pygame.mixer管理所有音频
    - 渲染系统: 绘制地图、UI、HUD
```

#### Player类（玩家角色）
```python
class Player:
    - 移动控制: WASD键盘输入
    - 碰撞检测: 2像素边距优化
    - 自动对齐: 6像素转弯辅助
    - 动画系统: 兼容JSON格式精灵表
```

#### Enemy类（敌人AI）
```python
class Enemy:
    - 3种AI模式: random/chase/fast_chase
    - 游荡行为: 初始随机方向移动
    - 追踪算法: 曼哈顿距离 + 延迟更新
    - 距离检测: 8格内激活追踪
```

### 关键算法

#### 1. 转弯对齐算法
```python
# 水平转垂直时自动对齐Y轴
grid_center_y = (self.y // TILE_SIZE) * TILE_SIZE + TILE_SIZE // 2
offset_y = self.y + TILE_SIZE // 2 - grid_center_y
if abs(offset_y) <= 6:  # 6像素容差
    self.y = grid_center_y - TILE_SIZE // 2
```

#### 2. 敌人追踪算法
```python
# 计算到玩家的方向
dx = player.x - self.x
dy = player.y - self.y
distance = (dx ** 2 + dy ** 2) ** 0.5

# 距离超过8格时游荡，否则追踪
if distance > TILE_SIZE * 8:
    self.move_random()
else:
    self.move_chase()
```

#### 3. 碰撞检测优化
```python
# 2像素边距减少误判
margin = 2
test_rect = pygame.Rect(
    rect.left + margin,
    rect.top + margin,
    rect.width - margin * 2,
    rect.height - margin * 2
)
```

---

## 📊 开发过程

### 阶段1: 基础框架（Phase 1）
- ✅ 游戏循环和状态管理
- ✅ Player类和基础移动
- ✅ 关卡1地图加载
- ✅ 碰撞检测系统

### 阶段2: 完整功能（Phase 2）
- ✅ 敌人AI系统
- ✅ 音效集成
- ✅ 3个完整关卡
- ✅ 生命系统
- ✅ UI和HUD

### 阶段3: 优化和完善
- ✅ 修复转弯卡墙问题
- ✅ 优化敌人游荡行为
- ✅ 平衡性调整
- ✅ 敌人生成位置优化

### 阶段4: 部署和分发
- ✅ Web版本（Pygbag）
- ✅ 可执行文件打包
- ✅ GitHub Pages部署

---

## 🐛 问题与解决

### 问题1: JSON动画格式兼容性
**问题:** Aseprite导出的JSON格式为字典，代码期望列表
**解决:** 添加类型检测，兼容dict和list两种格式

### 问题2: 玩家转弯卡墙
**问题:** 严格的网格对齐导致转弯困难
**解决:** 实现6像素容差的自动对齐系统

### 问题3: 敌人贴图不显示
**问题:** 只有PNG没有JSON动画文件
**解决:** 修改为直接加载PNG，不依赖JSON

### 问题4: 关卡跳过
**问题:** 分数未重置导致直接完成后续关卡
**解决:** 在关卡切换时重置分数为0

### 问题5: 敌人过于激进
**问题:** 敌人生成位置过近，追踪过于精准
**解决:** 
- 调整生成位置到地图角落
- 添加追踪延迟（每20/10帧更新一次）
- 实现8格追踪范围限制

---

## 📸 游戏截图

（可以添加实际截图）

### 主菜单
展示游戏标题和开始提示

### 关卡1
初级难度，1个随机移动的敌人

### 关卡2
中级难度，2个追踪敌人

### 关卡3
高级难度，3个快速追踪敌人

### 胜利界面
完成全部3关后的胜利画面

---

## 🎯 总结与反思

### 项目亮点
1. **完整的游戏循环** - 从主菜单到胜利/失败的完整流程
2. **智能AI系统** - 3种AI模式，渐进式难度
3. **流畅的操作** - 自动对齐和碰撞优化
4. **良好的代码架构** - OOP设计，模块化清晰
5. **多平台支持** - 本地运行 + 网页版 + 可执行文件

### 技术收获
- Pygame框架的深入使用
- 游戏AI算法设计
- 碰撞检测和物理模拟
- 状态机模式应用
- Git版本控制实践

### 后续改进方向
- 添加更多关卡
- 实现关卡编辑器
- 添加道具系统
- 支持触摸屏控制
- 添加排行榜功能

---

## 📚 参考资源

- Pygame官方文档: https://www.pygame.org/docs/
- 经典吃豆人游戏设计
- Python OOP最佳实践
- GitHub Actions CI/CD

---

## 📞 联系方式

- **GitHub:** https://github.com/Jake-yutong
- **项目地址:** https://github.com/Jake-yutong/SlimeGobble
- **在线试玩:** https://jake-yutong.github.io/SlimeGobble/

---

**声明:** 本项目为个人学习作业，所有代码均为原创开发。游戏灵感来源于经典吃豆人游戏。
