#!/bin/bash
# 同步工作区代码到 Skill 目录

SKILL_DIR="$HOME/.npm-global/lib/node_modules/openclaw/skills/ai-industry-research"
WORKSPACE_DIR="$HOME/.openclaw/workspace/ai-industry-research"

echo "🔄 同步工作区 → Skill..."

# 复制模块
cp -r "$WORKSPACE_DIR/scrapers" "$SKILL_DIR/"
cp -r "$WORKSPACE_DIR/storage" "$SKILL_DIR/"
cp -r "$WORKSPACE_DIR/generator" "$SKILL_DIR/"
cp -r "$WORKSPACE_DIR/config" "$SKILL_DIR/"
cp "$WORKSPACE_DIR/requirements.txt" "$SKILL_DIR/"

# 不复制存储数据（这些在用户工作区）
echo "✓ 代码已同步"
echo ""
echo "📁 Skill 目录：$SKILL_DIR"
echo "📁 工作区目录：$WORKSPACE_DIR"
