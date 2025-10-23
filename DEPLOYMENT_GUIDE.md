# 🎮 SlimeGobble 浏览器部署完全指南

## 📋 目录
- [概述](#概述)
- [方案对比](#方案对比)
- [详细步骤](#详细步骤)
- [部署位置选择](#部署位置选择)
- [常见问题](#常见问题)

---

## 概述

你的游戏现在可以通过以下方式运行：
1. ✅ **本地运行**（当前）- 在Mac上用Python运行
2. 🆕 **浏览器运行**（新增）- 任何人都能在线玩

---

## 方案对比

### 方案A: GitHub Pages（免费，推荐）⭐

**优点:**
- ✅ 完全免费
- ✅ 自动托管，无需维护服务器
- ✅ 访问链接简洁：`https://jake-yutong.github.io/SlimeGobble/`
- ✅ 直接从GitHub部署，版本管理方便

**缺点:**
- ⏰ 部署后需要等待3-5分钟生效
- 📦 有100MB大小限制（你的游戏远小于此）

**适合:** 长期托管，分享给朋友

---

### 方案B: itch.io（游戏平台）

**优点:**
- ✅ 专业游戏分发平台
- ✅ 可以设置价格或免费下载
- ✅ 有玩家社区和评论系统
- ✅ 支持游戏更新版本管理

**缺点:**
- 📝 需要注册账号
- 🎨 需要准备游戏封面图和描述

**适合:** 想让更多人玩到你的游戏，建立游戏作品集

**网址:** https://itch.io

---

### 方案C: Netlify（拖拽部署）

**优点:**
- ✅ 超简单，拖拽文件即可
- ✅ 自动生成随机链接
- ✅ 可以自定义域名

**缺点:**
- 🔗 免费版链接较长且随机
- 📦 每月100GB流量限制

**适合:** 快速分享给特定的人测试

**网址:** https://www.netlify.com

---

## 详细步骤

### 🎯 推荐流程：GitHub Pages部署

#### 第一步：上传素材（必须）

在Mac终端：

```bash
cd /Users/liyutong/Desktop/SlimeGobble

# 复制素材到项目的assets文件夹
cp /Users/liyutong/Desktop/assets/*.png assets/
cp /Users/liyutong/Desktop/assets/*.json assets/
cp /Users/liyutong/Desktop/assets/*.wav assets/

# 查看复制结果
ls -la assets/

# 应该看到：
# Player back.png, Player front.png, Player left.png, Player right.png
# Player back.json, Player front.json, Player left.json, Player right.json
# Chaser back.png, Chaser front.png, Chaser left.png, Chaser right.png
# coin.wav, win.wav, lose.wav, tap.wav

# 提交到GitHub
git add assets/
git commit -m "添加游戏素材文件"
git push
```

**验证:** 访问 https://github.com/Jake-yutong/SlimeGobble/tree/main/assets 确认文件都上传了

---

#### 第二步：安装Pygbag

```bash
# 激活虚拟环境
cd /Users/liyutong/Desktop/SlimeGobble
source venv/bin/activate

# 安装Pygbag（WebAssembly打包工具）
pip install pygbag
```

---

#### 第三步：本地测试（可选但推荐）

```bash
# 在浏览器中测试游戏
pygbag main.py
```

这会：
1. 自动打开浏览器
2. 显示游戏运行界面
3. 确认所有素材加载正确

测试完成按 `Ctrl+C` 停止。

---

#### 第四步：自动部署

**方法1: 使用自动化脚本（最简单）**

```bash
chmod +x deploy_web.sh
./deploy_web.sh
```

选择：
- 选项 `1`: 本地测试
- 选项 `2`: 只构建不部署
- 选项 `3`: 直接部署到GitHub Pages ⭐
- 选项 `4`: 完整流程（测试+构建+部署）

**方法2: 手动执行命令**

```bash
# 构建Web版本
pygbag --build main.py

# 切换到部署分支
git checkout -b gh-pages

# 复制构建文件
cp -r build/web/* .
touch .nojekyll

# 提交并推送
git add .
git commit -m "Deploy to GitHub Pages"
git push origin gh-pages --force

# 返回主分支
git checkout main
```

---

#### 第五步：启用GitHub Pages

1. 访问 https://github.com/Jake-yutong/SlimeGobble/settings/pages
2. 在 **"Source"** 下拉菜单选择 `gh-pages` 分支
3. 点击 **"Save"**
4. 等待3-5分钟

---

#### 第六步：访问游戏！

打开浏览器访问：

```
https://jake-yutong.github.io/SlimeGobble/
```

🎉 你的游戏现在在线了！

---

## 部署位置选择

### 你需要上传素材的地方：

```
/Users/liyutong/Desktop/SlimeGobble/assets/
```

这个文件夹必须包含：
- ✅ 12个PNG文件（玩家+敌人）
- ✅ 8个JSON文件（玩家动画）
- ✅ 4个WAV文件（音效，可选）

### 游戏将部署到：

- **GitHub存储**: `https://github.com/Jake-yutong/SlimeGobble`
- **在线游玩**: `https://jake-yutong.github.io/SlimeGobble/`

---

## 常见问题

### Q1: 素材上传后找不到？

**A:** 检查路径是否正确：
```bash
cd /Users/liyutong/Desktop/SlimeGobble
ls -la assets/
```

如果文件在，但GitHub上看不到：
```bash
git add assets/ -f
git commit -m "强制添加素材"
git push
```

---

### Q2: 部署后游戏打不开？

**A:** 常见原因：
1. **等待时间不够** - GitHub Pages需要3-5分钟生效
2. **分支未选择** - 确认Settings→Pages选择了`gh-pages`分支
3. **浏览器缓存** - 按`Ctrl+Shift+R`强制刷新

检查部署状态：
```
https://github.com/Jake-yutong/SlimeGobble/deployments
```

---

### Q3: 素材显示不出来？

**A:** 可能原因：
1. **文件名大小写** - 确保文件名完全匹配（如`Player front.png`）
2. **路径问题** - 已修复为相对路径，应该没问题
3. **文件损坏** - 重新复制素材文件

查看浏览器控制台错误：
- 按 `F12` 打开开发者工具
- 查看 Console 标签的红色错误

---

### Q4: 想更新游戏怎么办？

**A:** 修改代码后重新部署：

```bash
# 1. 在main分支修改代码
git add .
git commit -m "更新游戏"
git push

# 2. 重新运行部署脚本
./deploy_web.sh
# 选择选项3

# 3. 等待几分钟访问
```

---

### Q5: 能在手机上玩吗？

**A:** 可以访问但体验不好：
- ✅ 手机浏览器能打开网页
- ❌ 手机没有WASD键盘
- 💡 后续可以添加触摸屏控制

---

### Q6: 音效不播放？

**A:** 浏览器限制：
- 大多数浏览器要求用户交互后才能播放音频
- 解决方案：点击"开始游戏"按钮后才播放背景音乐
- 建议使用 `.ogg` 格式代替 `.wav`（兼容性更好）

---

### Q7: 游戏运行很慢？

**A:** 优化建议：
1. **压缩图片** - 使用 TinyPNG 等工具压缩PNG
2. **减小分辨率** - 素材尺寸不要太大
3. **清理缓存** - 重新构建：`pygbag --clean main.py`

---

### Q8: 想分享给朋友，如何自定义域名？

**A:** GitHub Pages支持自定义域名：

1. 购买域名（如 `slimegobble.com`）
2. 在仓库根目录添加 `CNAME` 文件：
   ```
   echo "slimegobble.com" > CNAME
   ```
3. 在域名提供商设置DNS指向：
   ```
   CNAME记录: www -> jake-yutong.github.io
   A记录: @ -> 185.199.108.153
   ```

---

## 🎯 快速参考

### 完整部署命令（复制粘贴版）

```bash
# 一键完成所有步骤
cd /Users/liyutong/Desktop/SlimeGobble
cp /Users/liyutong/Desktop/assets/* assets/
git add assets/ config.py
git commit -m "添加素材+修改路径"
git push
source venv/bin/activate
pip install pygbag
chmod +x deploy_web.sh
./deploy_web.sh  # 选择选项3或4
```

---

## 📞 需要帮助？

遇到问题请告诉我：
1. 🖼️ 错误截图
2. 📝 完整的错误信息
3. 🔍 在哪一步遇到问题
4. 💻 浏览器控制台的日志（F12）

我会帮你快速解决！

---

## 🎉 成功后

分享链接给朋友：
```
https://jake-yutong.github.io/SlimeGobble/
```

或者制作二维码：
1. 访问 https://www.qrcode-monkey.com/
2. 输入你的游戏链接
3. 下载二维码图片
4. 分享给朋友扫码即可游玩！

祝部署顺利！🚀
