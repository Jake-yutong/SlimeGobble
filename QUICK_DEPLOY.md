# 🚀 5分钟快速部署到浏览器

## 第一步：上传素材（2分钟）

在Mac终端执行：

```bash
cd /Users/liyutong/Desktop/SlimeGobble

# 复制素材文件
cp /Users/liyutong/Desktop/assets/*.png assets/
cp /Users/liyutong/Desktop/assets/*.json assets/
cp /Users/liyutong/Desktop/assets/*.wav assets/

# 提交到GitHub
git add assets/
git commit -m "添加素材文件"
git push
```

## 第二步：自动部署（3分钟）

```bash
# 安装部署工具
pip install pygbag

# 运行自动化脚本
chmod +x deploy_web.sh
./deploy_web.sh
```

选择选项 `3` 或 `4` 部署到GitHub Pages。

## 第三步：访问游戏

等待3-5分钟后访问：

**https://jake-yutong.github.io/SlimeGobble/**

---

## 🆘 遇到问题？

### 素材没上传成功？
检查文件：
```bash
ls -la assets/
```
应该看到所有PNG、JSON、WAV文件。

### 部署失败？
查看详细步骤：[WEB_DEPLOYMENT.md](WEB_DEPLOYMENT.md)

### 需要帮助？
告诉我错误信息，我会帮你解决！
