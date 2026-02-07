# 交易经验记录 Discord Bot

一个简单的 Discord Bot，帮助你记录和检索交易经验。数据存储在 GitHub Issues 中，跨设备访问，永不丢失。

## 特点

- ✅ 保留原话，不美化
- ✅ 结构化记录（原话、背景、复盘、教训）
- ✅ 标签分类，快速检索
- ✅ 跨设备访问（Discord + GitHub）
- ✅ 无需自己的服务器

---

## 快速开始

### 1. 创建 GitHub 仓库

1. 在 GitHub 创建一个新仓库（如 `trading-experiences`）
2. 记下仓库名：`username/trading-experiences`

### 2. 创建 Discord Bot

1. 访问 https://discord.com/developers/applications
2. 点击 "New Application" → 创建应用
3. 在 "Bot" 页面创建 Bot，复制 **Token**
4. 在 "OAuth2" → "URL Generator" 选中 `bot` 和 `Send Messages`
5. 生成的链接在浏览器打开，邀请 Bot 到你的服务器

### 3. 生成 GitHub Token

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token" → 选择 "Tokens (classic)"
3. 勾选 `repo` 权限（完整的仓库访问权限）
4. 生成并复制 Token

### 4. 配置 Secrets

在你的 GitHub 仓库中，进入 **Settings** → **Secrets and variables** → **Actions**，添加以下 Secrets：

| Name | Value |
|------|-------|
| `DISCORD_TOKEN` | 你的 Discord Bot Token |
| `GITHUB_TOKEN` | 你的 GitHub Personal Access Token |
| `GITHUB_REPO` | 你的仓库名（如 `username/trading-experiences`）|

### 5. 启动 Bot

**方式一：本地运行（开发测试）**

```bash
# 克隆代码
git clone https://github.com/your-username/trading-experiences.git
cd trading-experiences

# 安装依赖
pip install -r requirements.txt

# 复制配置文件
cp .env.example .env

# 编辑 .env，填入你的 tokens
# DISCORD_TOKEN=...
# GITHUB_TOKEN=...
# GITHUB_REPO=...

# 运行 bot
python bot.py
```

**方式二：GitHub Actions（推荐）**

1. 将代码推送到 GitHub 仓库
2. 进入 **Actions** 页面
3. 选择 "Discord Trading Journal Bot" workflow
4. 点击 "Run workflow"

⚠️ **注意**：GitHub Actions 有 6 小时运行限制，适合测试使用。

如需 24/7 运行，建议使用免费平台：
- [Render](https://render.com/)
- [Railway](https://railway.app/)
- [Fly.io](https://fly.io/)

---

## 使用指南

在 Discord 中发送命令：

### 记录经验

```
!快速记录
```

然后按模板填写：

```
!记录 BTC 逃顶失败

原话：
已经涨三天了，肯定到顶了，再不空就踏空了！

市场背景：
- 价格：$44,500
- 趋势：连续 3 天大涨
- 成交量：持续放大

做得好：
- 设置了止损
- 及时离场

做得不好：
- 在放量上涨时做空
- 被 FOMO 情绪影响

核心教训：
不要在放量上涨时做空，放量通常意味着趋势延续。

标签：BTC 逃顶 失败案例 FOMO
```

### 搜索经验

```
!搜索 逃顶
!搜索 标签:BTC
!搜索 FOMO
```

### 查看最近

```
!最近
!最近 10
```

### 统计

```
!统计
```

---

## 记录模板（遵循提示词原则）

每条记录包含以下部分：

### 1. 原话（最重要）
- **一字不改**，保留当时真实想法
- 不要事后美化
- 包括负面情绪、错误判断

### 2. 市场背景
- 价格、趋势、成交量
- 市场情绪
- 技术指标

### 3. 复盘
- **做得好的地方**
- **做得不好的地方**

### 4. 核心教训
- 1-2 句最重要的话
- 可以直接引用原话

---

## 高级功能

### 条件触发提醒（需开发）

可以添加监控功能，当市场条件满足时自动推送相关经验：

```python
# 伪代码示例
if current_price > 45000 and daily_change > 5%:
    relevant_lessons = search_issues("标签:逃顶 标签:BTC")
    send_to_discord(f"🔔 提醒：历史中有 {len(relevant_lessons)} 条逃顶经验")
```

### AI 匹配（需开发）

使用 AI 分析当前市场，自动匹配最相关的历史经验。

---

## 数据安全

- ✅ 数据存储在你自己的 GitHub 仓库
- ✅ 可以设为私有仓库
- ✅ GitHub 提供版本控制，永不丢失
- ✅ 支持导出为 Markdown

---

## 常见问题

**Q: GitHub Actions 会一直运行吗？**
A: 不会，有 6 小时限制。如需 24/7 运行，建议用 Render/Railway 等免费平台。

**Q: 可以用私有仓库吗？**
A: 可以，GitHub Token 只需要访问你的仓库即可。

**Q: 如何备份？**
A: 数据就在你的 GitHub 仓库，可以直接 clone 或导出。

**Q: 支持图片附件吗？**
A: GitHub Issues 支持图片，可以上传交易截图。

---

## License

MIT
