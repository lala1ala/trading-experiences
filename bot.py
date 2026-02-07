"""
交易经验记录 Discord Bot
使用 GitHub Issues 存储和检索交易经验
"""

import os
import re
import discord
from github import Github, GithubException
from datetime import datetime
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GITHUB_TOKEN = os.getenv("GH_PAT")  # GitHub Actions 中用 GH_PAT
REPO_NAME = os.getenv("REPO_NAME")  # 格式: username/repo

# Discord 配置
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

# GitHub 配置
github = Github(GITHUB_TOKEN)
repo = github.get_repo(REPO_NAME)


# ========== 工具函数 ==========

def create_issue_content(raw_thoughts, background, good, bad, lessons, price="", trend=""):
    """生成 Issue 内容"""
    content = f"""## 原话

{raw_thoughts}

## 市场背景

"""

    if price:
        content += f"- **价格**：{price}\n"
    if trend:
        content += f"- **趋势**：{trend}\n"

    content += f"{background}\n"

    content += f"""
## 做得好的地方

{good}

## 做得不好的地方

{bad}

## 核心教训

{lessons}

---

📅 记录时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}
🤖 由 Discord Bot 自动创建
"""
    return content


def parse_tags(tags_str):
    """解析标签字符串"""
    if not tags_str:
        return []
    # 分割并清理标签
    tags = [t.strip() for t in tags_str.replace('，', ' ').replace(',', ' ').split()]
    # 移除空标签
    return [t for t in tags if t]


def create_github_issue(title, content, labels):
    """在 GitHub 创建 Issue"""
    try:
        # 确保标签存在
        existing_labels = [label.name for label in repo.get_labels()]
        for label in labels:
            if label not in existing_labels:
                repo.create_label(label, "0075ca")

        issue = repo.create_issue(
            title=title,
            body=content,
            labels=labels
        )
        return issue.html_url
    except Exception as e:
        print(f"创建 Issue 失败: {e}")
        return None


def search_issues(query, labels=None):
    """搜索 GitHub Issues"""
    try:
        # 构建搜索查询
        q = f"repo:{REPO_NAME} {query}"
        if labels:
            for label in labels:
                q += f" label:{label}"

        issues = github.search_issues(q, state="open")
        return issues
    except Exception as e:
        print(f"搜索失败: {e}")
        return []


# ========== Discord 事件 ==========

@bot.event
async def on_ready():
    print(f'✅ Bot 已启动: {bot.user}')
    print(f'📦 连接到仓库: {REPO_NAME}')


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # 命令: !帮助
    if message.content in ['!帮助', '!help', '!h']:
        help_text = """
📖 **交易经验记录 Bot 使用指南**

**记录经验**
```
!记录
```
我会引导你一步步输入信息

**搜索经验**
```
!搜索 关键词
!搜索 标签:逃顶
!搜索 BTC 标签:失败
```

**查看最近记录**
```
!最近
```

**统计**
```
!统计
```
        """
        await message.channel.send(help_text)

    # 命令: !记录
    elif message.content.startswith('!记录'):
        # 进入记录模式
        await message.channel.send("""📝 **开始记录交易经验**

请依次回复以下问题（你可以慢慢输入，完成后我会创建记录）：

**第1步**：请输入【当时的原话】
> 你当时真实的想法，一字不改，不要美化

直接回复即可，我会等待你的输入...
        """)

        # 等待用户输入（这里用简化版，实际可以用状态机或 view）
        # 为了简化，我们让用户一次性发送所有信息

    # 命令: !快速记录（一次性输入）
    elif message.content.startswith('!快速记录'):
        await message.channel.send("""📝 **快速记录模板**

请复制以下模板，填好后发送：

```
!记录 标题

原话：
[当时的真实想法]

市场背景：
[价格、趋势、成交量...]

做得好：
- [点1]
- [点2]

做得不好：
- [点1]
- [点2]

核心教训：
[最重要的教训]

标签：[空格分隔，如：BTC 逃顶 失败]
```
        """)

    # 命令: !搜索
    elif message.content.startswith('!搜索'):
        query = message.content.replace('!搜索', '').strip()

        if not query:
            await message.channel.send("❌ 请输入搜索关键词")
            return

        await message.channel.send(f"🔍 正在搜索：`{query}`...")

        issues = search_issues(query)

        if issues.totalCount == 0:
            await message.channel.send("❌ 没有找到相关经验")
            return

        # 构建结果
        result = f"✅ 找到 **{issues.totalCount}** 条相关经验\n\n"

        count = 0
        for issue in issues:
            count += 1
            if count > 5:  # 只显示前5条
                break

            # 提取原话部分
            body = issue.body
            raw_match = re.search(r'## 原话\n(.*?)(?=\n##|\n---|$)', body, re.DOTALL)
            raw_thoughts = raw_match.group(1).strip() if raw_match else "无原话"

            # 截取前100字
            raw_preview = raw_thoughts[:100] + "..." if len(raw_thoughts) > 100 else raw_thoughts

            result += f"**{count}. {issue.title}**\n"
            result += f"🏷️ {', '.join([l.name for l in issue.labels])}\n"
            result += f"📅 {issue.created_at.strftime('%Y-%m-%d')}\n"
            result += f"> {raw_preview}\n"
            result += f"🔗 {issue.html_url}\n\n"

        await message.channel.send(result[:2000])

    # 命令: !最近
    elif message.content.startswith('!最近'):
        count = 5
        args = message.content.split()
        if len(args) > 1 and args[1].isdigit():
            count = int(args[1])

        issues = repo.get_issues(state='open', sort='created', direction='desc')

        result = f"📋 **最近 {count} 条记录**\n\n"

        for i, issue in enumerate(issues[:count]):
            result += f"**{i+1}. {issue.title}**\n"
            result += f"🏷️ {', '.join([l.name for l in issue.labels])}\n"
            result += f"📅 {issue.created_at.strftime('%Y-%m-%d')}\n"
            result += f"🔗 {issue.html_url}\n\n"

        await message.channel.send(result)

    # 命令: !统计
    elif message.content == '!统计':
        # 统计标签
        issues = repo.get_issues(state='open')

        label_counts = {}
        total = 0

        for issue in issues:
            total += 1
            for label in issue.labels:
                label_counts[label.name] = label_counts.get(label.name, 0) + 1

        result = f"📊 **经验统计**\n\n"
        result += f"总记录数：**{total}** 条\n\n"

        if label_counts:
            result += "**标签分布：**\n"
            for label, count in sorted(label_counts.items(), key=lambda x: x[1], reverse=True):
                result += f"- {label}: {count} 条\n"

        await message.channel.send(result)


# ========== 主程序 ==========

if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("❌ 错误: 未设置 DISCORD_TOKEN 环境变量")
        exit(1)

    if not GITHUB_TOKEN:
        print("❌ 错误: 未设置 GITHUB_TOKEN 环境变量")
        exit(1)

    if not REPO_NAME:
        print("❌ 错误: 未设置 GITHUB_REPO 环境变量")
        exit(1)

    bot.run(DISCORD_TOKEN)
