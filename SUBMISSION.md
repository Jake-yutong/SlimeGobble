# SlimeGobble - 游戏作业提交文档

**开发者:** Jake-yutong  
**项目类型:** Python游戏开发  
**开发时间:** 2025年10月  

---

## 🎮 游戏试玩方式

### 方式1: 在线试玩（最方便）⭐⭐⭐⭐⭐

```
🌐 网址: https://jake-yutong.github.io/SlimeGobble/
```

- ✅ 打开浏览器即可游玩
- ✅ 无需安装任何软件
- ✅ 支持Windows/Mac/Linux

**操作说明:**
1. 点击上方链接
2. 等待游戏加载（约5-10秒）
3. 按空格键开始游戏
4. 使用WASD键控制角色

---

### 方式2: 下载可执行文件（体验最佳）⭐⭐⭐⭐⭐

```
📦 下载地址: https://github.com/Jake-yutong/SlimeGobble/releases
```

**Mac用户:**
1. 下载 `SlimeGobble-Mac.zip`
2. 解压缩
3. 右键 → 打开（首次需要）
4. 开始游戏

**Windows用户:**
1. 下载 `SlimeGobble-Windows.zip`
2. 解压缩
3. 双击 `SlimeGobble.exe`
4. 开始游戏

---

### 方式3: 查看源码（适合代码评审）

```
💻 GitHub仓库: https://github.com/Jake-yutong/SlimeGobble
```

- 完整的源代码
- 开发历史和提交记录
- 项目文档和说明

**本地运行方法:**
```bash
git clone https://github.com/Jake-yutong/SlimeGobble.git
cd SlimeGobble
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install pygame numpy
python main.py
```

---

## 📖 游戏说明

### 游戏背景
SlimeGobble是一款受经典吃豆人启发的益智游戏。玩家扮演可爱的史莱姆"Mumu"，在迷宫中收集金币，同时躲避邪恶的追击者（Chaser）。

### 游戏目标
- 每关收集**500分**即可进入下一关
- 完成全部**3关**获得胜利
- 避免被敌人抓到（共有3条命）

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

**敌人系统:**
- **关卡1:** 1个敌人，随机移动，速度慢
- **关卡2:** 2个敌人，追踪玩家，速度中等
- **关卡3:** 3个敌人，快速追踪，难度最高

**生命系统:**
- 初始3条命
- 被敌人碰到失去1条命
- 失去所有生命则游戏结束

---

## 🎨 游戏特色

### 1. 渐进式难度设计
- 关卡1: 新手友好，敌人移动缓慢
- 关卡2: 适中难度，需要策略走位
- 关卡3: 高难度挑战，考验反应速度

### 2. 智能敌人AI
- **随机AI:** 关卡1敌人随机游荡
- **追踪AI:** 关卡2/3敌人会追踪玩家
- **距离检测:** 远离玩家时游荡，接近时追击
- **路径规划:** 使用曼哈顿距离算法找最短路径

### 3. 流畅的操作体验
- 自动转弯对齐系统
- 墙壁滑动效果
- 精确的碰撞检测
- 6像素容差，减少卡墙

### 4. 完整的游戏循环
- 主菜单 → 游戏 → 暂停 → 关卡完成 → 胜利/失败
- 完善的状态管理
- 音效和背景音乐支持

---

## 🛠️ 技术实现

### 开发环境
- **编程语言:** Python 3.12
- **主要框架:** Pygame 2.6.1
- **辅助库:** NumPy 2.3.4
- **开发工具:** VS Code, GitHub Codespaces
- **版本控制:** Git + GitHub

### 项目架构

```
SlimeGobble/
├── main.py          # 游戏入口
├── game.py          # 游戏主逻辑（500+ 行）
├── player.py        # 玩家类（300+ 行）
├── enemy.py         # 敌人类（300+ 行）
├── config.py        # 配置和地图数据
└── assets/          # 游戏素材
    ├── Player*.png  # 玩家精灵图
    ├── Chaser*.png  # 敌人精灵图
    └── *.wav        # 音效文件
```

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
