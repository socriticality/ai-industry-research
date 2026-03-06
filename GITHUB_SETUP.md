# GitHub 同步配置说明

## 当前状态

| 项目 | 状态 |
|------|------|
| 仓库创建 | ✅ https://github.com/socriticality/ai-industry-research |
| Token 类型 | ❌ Fine-grained (不支持 git push) |
| 代码推送 | ⚠️ 需要配置 |

---

## 问题

**Fine-grained tokens 不支持 git push 操作**

虽然 API 调用正常，但 git 推送会返回 403 错误。这是 GitHub 的限制。

---

## 解决方案

### 方案 1：创建 Classic Token（最简单）

1. 访问：https://github.com/settings/tokens/new
2. **选择 "Generate new token (classic)"**
3. Token 名称：`ai-research-git-push`
4. 过期时间：建议 90 天
5. **权限：勾选 `repo` (Full control of private repositories)**
6. 创建后复制 token
7. 更新 `sync-github.sh` 中的 token

```bash
# 编辑 sync-github.sh，替换 token 行
REMOTE_URL="https://socriticality:YOUR_NEW_CLASSIC_TOKEN@github.com/socriticality/ai-industry-research.git"
```

### 方案 2：配置 SSH 密钥（推荐，更安全）

```bash
# 1. 生成 SSH 密钥
ssh-keygen -t ed25519 -C "socriticality@users.noreply.github.com"
# 一路回车即可

# 2. 查看公钥
cat ~/.ssh/id_ed25519.pub

# 3. 复制公钥内容，添加到 GitHub
# https://github.com/settings/keys
# 点击 "New SSH key"

# 4. 测试连接
ssh -T git@github.com

# 5. 切换远程为 SSH
cd ~/.openclaw/workspace/ai-industry-research
git remote set-url origin git@github.com:socriticality/ai-industry-research.git

# 6. 推送
git push -u origin main
```

### 方案 3：使用 GitHub CLI

```bash
# 安装 gh (如果还没有)
# https://cli.github.com/

# 登录
gh auth login

# 推送
cd ~/.openclaw/workspace/ai-industry-research
git push -u origin main
```

---

## 推荐

**方案 2 (SSH 密钥)** 最安全且一劳永逸。

**方案 1 (Classic Token)** 最快，但需要定期更新 token。

---

## 自动同步设置

配置完成后，添加 cron 任务：

```bash
crontab -e
```

添加：
```
0 2 * * * cd /home/ecs-user/.openclaw/workspace/ai-industry-research && ./sync-github.sh "Nightly sync" >> /tmp/github-sync.log 2>&1
```

---

## 当前可手动同步

在配置好认证之前，可以手动：
1. 下载代码压缩包
2. 在 GitHub 仓库页面上传
