#!/bin/bash
# AI 与产业互联网研究系统 - GitHub 自动同步脚本
# 用法：./sync-github.sh [commit_message]
#
# 首次使用需要配置：
# 1. 设置环境变量：export GITHUB_TOKEN="ghp_xxxxx"
# 2. 或配置 SSH 密钥

set -e

REPO_DIR="$HOME/.openclaw/workspace/ai-industry-research"
REMOTE_URL="https://github.com/socriticality/ai-industry-research.git"
BRANCH="main"

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}🔄 GitHub 自动同步脚本${NC}"
echo "================================"

cd "$REPO_DIR"

# 检查认证方式
if [ -n "$GITHUB_TOKEN" ]; then
    REMOTE_URL="https://socriticality:${GITHUB_TOKEN}@github.com/socriticality/ai-industry-research.git"
    echo "✅ 使用 GITHUB_TOKEN 认证"
elif ssh -T git@github.com &>/dev/null; then
    REMOTE_URL="git@github.com:socriticality/ai-industry-research.git"
    echo "✅ 使用 SSH 认证"
else
    echo -e "${RED}❌ 未配置认证${NC}"
    echo ""
    echo "请选择以下一种方式："
    echo ""
    echo "1️⃣  设置环境变量:"
    echo "    export GITHUB_TOKEN=\"ghp_xxxxx\""
    echo ""
    echo "2️⃣  配置 SSH 密钥:"
    echo "    ssh-keygen -t ed25519"
    echo "    然后添加公钥到 GitHub"
    exit 1
fi

# 检查 git 状态
if [ -z "$(git status --porcelain)" ]; then
    echo -e "${YELLOW}⚠️  没有需要提交的更改${NC}"
else
    echo "📝 添加文件..."
    git add -A
    
    MESSAGE="${1:-Auto-sync: $(date '+%Y-%m-%d %H:%M')}"
    echo "💾 提交：$MESSAGE"
    git commit -m "$MESSAGE"
fi

# 确保分支名正确
git branch -M main 2>/dev/null || true

# 设置远程
git remote set-url origin "$REMOTE_URL" 2>/dev/null || git remote add origin "$REMOTE_URL"

# 推送
echo "🚀 推送到 GitHub..."
if git push origin main --force 2>&1; then
    echo -e "${GREEN}✅ 同步成功！${NC}"
    echo "📦 仓库：https://github.com/socriticality/ai-industry-research"
else
    echo -e "${RED}❌ 推送失败${NC}"
    exit 1
fi
