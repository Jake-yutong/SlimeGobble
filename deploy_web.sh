#!/bin/bash
# SlimeGobble Web部署自动化脚本

set -e  # 遇到错误立即退出

echo "🎮 SlimeGobble Web部署工具"
echo "=============================="
echo ""

# 检查是否在正确的目录
if [ ! -f "main.py" ]; then
    echo "❌ 错误: 请在项目根目录运行此脚本"
    exit 1
fi

# 检查素材文件
echo "📦 检查素材文件..."
if [ ! -d "assets" ]; then
    echo "❌ 错误: assets文件夹不存在"
    echo "请先上传素材文件到assets/文件夹"
    exit 1
fi

asset_count=$(ls -1 assets/*.png 2>/dev/null | wc -l)
if [ "$asset_count" -lt 12 ]; then
    echo "⚠️  警告: assets文件夹中PNG文件不足12个"
    echo "   当前数量: $asset_count"
    echo "   请确认所有素材已上传"
    read -p "是否继续? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "✅ 素材检查完成"
echo ""

# 检查pygbag是否安装
echo "🔧 检查依赖..."
if ! command -v pygbag &> /dev/null; then
    echo "❌ pygbag未安装"
    echo "正在安装pygbag..."
    pip install pygbag
fi
echo "✅ 依赖检查完成"
echo ""

# 选择操作
echo "请选择操作:"
echo "1) 本地测试 (在浏览器中测试游戏)"
echo "2) 构建Web版本 (生成build/web文件夹)"
echo "3) 部署到GitHub Pages"
echo "4) 全部执行 (测试→构建→部署)"
echo ""
read -p "请输入选项 (1-4): " choice

case $choice in
    1)
        echo ""
        echo "🌐 启动本地测试服务器..."
        echo "游戏将在浏览器中自动打开"
        echo "按 Ctrl+C 停止服务器"
        echo ""
        pygbag main.py
        ;;
    2)
        echo ""
        echo "🏗️  构建Web版本..."
        pygbag --build main.py
        echo ""
        echo "✅ 构建完成！"
        echo "文件位置: build/web/"
        echo ""
        echo "你可以:"
        echo "  - 上传到 itch.io"
        echo "  - 上传到 Netlify"
        echo "  - 打包分享: cd build/web && zip -r slimegobble.zip *"
        ;;
    3)
        echo ""
        echo "🚀 部署到GitHub Pages..."
        echo ""
        
        # 保存当前分支
        current_branch=$(git branch --show-current)
        echo "当前分支: $current_branch"
        
        # 确保主分支是最新的
        echo "📤 推送最新代码到main分支..."
        git add .
        git commit -m "准备Web部署" || echo "没有需要提交的更改"
        git push origin main
        
        # 构建Web版本
        echo "🏗️  构建Web版本..."
        pygbag --build main.py
        
        # 切换到gh-pages分支
        echo "🌿 切换到gh-pages分支..."
        if git show-ref --verify --quiet refs/heads/gh-pages; then
            git checkout gh-pages
            git pull origin gh-pages || true
        else
            git checkout --orphan gh-pages
            git rm -rf . 2>/dev/null || true
        fi
        
        # 复制构建文件
        echo "📋 复制构建文件..."
        cp -r build/web/* .
        
        # 创建.nojekyll文件（GitHub Pages需要）
        touch .nojekyll
        
        # 提交并推送
        echo "📤 推送到GitHub Pages..."
        git add .
        git commit -m "Deploy to GitHub Pages - $(date '+%Y-%m-%d %H:%M:%S')"
        git push origin gh-pages --force
        
        # 切换回原分支
        git checkout "$current_branch"
        
        echo ""
        echo "✅ 部署完成！"
        echo ""
        echo "🌐 访问你的游戏:"
        echo "   https://jake-yutong.github.io/SlimeGobble/"
        echo ""
        echo "⏰ 等待3-5分钟让GitHub处理部署"
        echo "📊 查看状态: https://github.com/Jake-yutong/SlimeGobble/settings/pages"
        ;;
    4)
        echo ""
        echo "🎯 执行完整流程..."
        echo ""
        
        # 测试
        echo "步骤1/3: 本地测试"
        echo "将打开浏览器进行测试，测试完成后按Ctrl+C继续"
        pygbag main.py &
        PID=$!
        echo "按Enter继续到下一步..."
        read
        kill $PID 2>/dev/null || true
        
        # 构建
        echo ""
        echo "步骤2/3: 构建Web版本"
        pygbag --build main.py
        
        # 部署
        echo ""
        echo "步骤3/3: 部署到GitHub Pages"
        current_branch=$(git branch --show-current)
        
        git add .
        git commit -m "准备Web部署" || echo "没有需要提交的更改"
        git push origin main
        
        if git show-ref --verify --quiet refs/heads/gh-pages; then
            git checkout gh-pages
            git pull origin gh-pages || true
        else
            git checkout --orphan gh-pages
            git rm -rf . 2>/dev/null || true
        fi
        
        cp -r build/web/* .
        touch .nojekyll
        
        git add .
        git commit -m "Deploy to GitHub Pages - $(date '+%Y-%m-%d %H:%M:%S')"
        git push origin gh-pages --force
        
        git checkout "$current_branch"
        
        echo ""
        echo "✅ 全部完成！"
        echo "🌐 https://jake-yutong.github.io/SlimeGobble/"
        ;;
    *)
        echo "❌ 无效选项"
        exit 1
        ;;
esac

echo ""
echo "🎉 完成！"
