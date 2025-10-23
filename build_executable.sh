#!/bin/bash
# SlimeGobble 可执行文件打包脚本

set -e

echo "🎮 SlimeGobble 可执行文件打包工具"
echo "===================================="
echo ""

# 检查是否在正确的目录
if [ ! -f "main.py" ]; then
    echo "❌ 错误: 请在项目根目录运行此脚本"
    exit 1
fi

# 检查Python环境
if [ ! -d "venv" ]; then
    echo "❌ 错误: 虚拟环境不存在"
    echo "请先创建虚拟环境: python -m venv venv"
    exit 1
fi

echo "🔧 激活虚拟环境..."
source venv/bin/activate

echo "📦 安装PyInstaller..."
pip install pyinstaller

echo ""
echo "🏗️  开始打包..."
echo ""

# 清理之前的构建
rm -rf build/ dist/ *.spec

# 打包命令
pyinstaller --name="SlimeGobble" \
    --windowed \
    --onefile \
    --add-data="assets:assets" \
    --icon=assets/icon.icns \
    --noconfirm \
    main.py

echo ""
echo "✅ 打包完成！"
echo ""
echo "📁 可执行文件位置:"
echo "   Mac: dist/SlimeGobble.app"
echo ""
echo "📦 分发说明:"
echo "   1. 压缩dist文件夹中的应用"
echo "   2. 分享给其他Mac用户"
echo "   3. 双击即可运行游戏"
echo ""
echo "⚠️  注意事项:"
echo "   - Mac用户首次打开可能需要: 右键 → 打开"
echo "   - Windows用户需要在Windows系统上重新打包"
echo ""
