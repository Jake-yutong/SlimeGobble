# 🌐 浏览器部署指南

## 方案概述

本游戏使用 **Pygbag** 将Pygame游戏转换为WebAssembly，可以在浏览器中运行。

## 📋 部署步骤

### 第一步：上传素材文件 ✅

1. **在Mac本地操作**
   ```bash
   cd /Users/liyutong/Desktop/SlimeGobble
   
   # 复制所有素材到项目的assets文件夹
   cp /Users/liyutong/Desktop/assets/*.png assets/
   cp /Users/liyutong/Desktop/assets/*.json assets/
   cp /Users/liyutong/Desktop/assets/*.wav assets/
   
   # 提交到GitHub
   git add assets/
   git commit -m "添加游戏素材文件"
   git push
   ```

2. **验证上传**
   - 访问 https://github.com/Jake-yutong/SlimeGobble/tree/main/assets
   - 确认所有PNG、JSON、WAV文件都在

### 第二步：安装Pygbag

在Mac本地：
```bash
cd /Users/liyutong/Desktop/SlimeGobble
source venv/bin/activate  # 激活虚拟环境
pip install pygbag
```

### 第三步：构建Web版本

```bash
# 在项目根目录运行
pygbag main.py
```

这会：
1. 打包游戏代码和素材
2. 创建 `build/web` 文件夹
3. 启动本地Web服务器
4. 自动打开浏览器测试

### 第四步：在浏览器测试

Pygbag会自动打开浏览器，访问：
```
http://localhost:8000
```

你应该能看到游戏在浏览器中运行！

### 第五步：部署到GitHub Pages（免费托管）

#### 5.1 准备GitHub Pages

在Mac终端：
```bash
cd /Users/liyutong/Desktop/SlimeGobble

# 创建gh-pages分支
git checkout --orphan gh-pages
git rm -rf .

# 构建Web版本（生成到build/web）
pygbag --build main.py

# 复制构建文件到根目录
cp -r build/web/* .

# 提交并推送
git add .
git commit -m "Deploy to GitHub Pages"
git push origin gh-pages
```

#### 5.2 启用GitHub Pages

1. 访问 https://github.com/Jake-yutong/SlimeGobble/settings/pages
2. 在 "Branch" 下选择 `gh-pages` 分支
3. 点击 "Save"
4. 等待几分钟

#### 5.3 访问游戏

你的游戏将发布在：
```
https://jake-yutong.github.io/SlimeGobble/
```

## 🚀 快速部署脚本

我已经为你创建了自动化脚本 `deploy_web.sh`，只需运行：

```bash
cd /Users/liyutong/Desktop/SlimeGobble
chmod +x deploy_web.sh
./deploy_web.sh
```

## 📱 其他部署选项

### 选项1: itch.io（游戏分发平台）
1. 注册 https://itch.io
2. 创建新项目，选择 "HTML" 类型
3. 上传 `build/web` 文件夹的所有内容
4. 设置为 "This file will be played in the browser"

### 选项2: Netlify（免费托管）
1. 注册 https://www.netlify.com
2. 拖拽 `build/web` 文件夹到Netlify
3. 获得类似 `https://your-game.netlify.app` 的链接

### 选项3: 直接分享HTML文件
```bash
# 打包成zip
cd build/web
zip -r slimegobble-web.zip *
```
发送zip文件，解压后用浏览器打开 `index.html`

## ⚠️ 注意事项

### 音频兼容性
浏览器对音频有限制，可能需要用户交互后才能播放。建议：
- 首次点击开始游戏后才播放音乐
- 使用 `.ogg` 格式替代 `.wav`（更好的浏览器支持）

### 性能优化
- 素材文件尽量压缩（使用TinyPNG等工具）
- JSON文件可以最小化
- 总大小建议 < 10MB

### 测试清单
- [ ] 游戏能在Chrome中运行
- [ ] 游戏能在Firefox中运行
- [ ] 游戏能在Safari中运行
- [ ] 移动设备能访问（但键盘操作可能有问题）
- [ ] 所有贴图正确显示
- [ ] 音效可以播放（需要点击后）

## 🆘 故障排查

### 问题1: 素材加载失败
- 确认 `assets/` 文件夹在项目根目录
- 检查文件名大小写是否匹配
- 查看浏览器控制台错误信息

### 问题2: Pygbag构建失败
```bash
# 升级到最新版本
pip install --upgrade pygbag

# 清理缓存重新构建
rm -rf build/
pygbag --clean main.py
```

### 问题3: GitHub Pages不显示
- 等待5-10分钟让GitHub处理
- 检查 Settings → Pages 是否正确配置
- 确认 gh-pages 分支存在

## 📞 需要帮助？

如果遇到问题，请告诉我：
1. 错误信息（截图或复制）
2. 在哪一步遇到问题
3. 浏览器控制台的错误日志

我会帮你解决！
