#!/bin/bash
# Cron Scheduler 示例脚本
# 演示如何创建不同类型的定时任务

echo "=== Cron Scheduler 示例 ==="
echo ""

# 示例 1: 每天 2 点同步到 GitHub (北京时间)
echo "示例 1: 每天 2 点同步到 GitHub"
echo "北京时间 02:00 = UTC 18:00 (前一天)"
cat << 'EOF' > /tmp/github-sync.json
{
  "name": "Daily GitHub Sync",
  "schedule": {
    "kind": "cron",
    "expr": "0 18 * * *",
    "tz": "UTC"
  },
  "payload": {
    "kind": "systemEvent",
    "text": "REMINDER: Run git sync - cd /root/.openclaw/workspace && git add -A && git commit -m '例行化备份' && git push origin main"
  },
  "sessionTarget": "main",
  "enabled": true
}
EOF

# 示例 2: 每天 20:30 给 tech 发消息 (北京时间)
echo ""
echo "示例 2: 每天 20:30 给 tech 发消息"
echo "北京时间 20:30 = UTC 12:30"
cat << 'EOF' > /tmp/tech-reminder.json
{
  "name": "Daily tech reminder",
  "schedule": {
    "kind": "cron",
    "expr": "30 12 * * *",
    "tz": "UTC"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "给tech (ou_5c7144a360f68b2db0e434749f5a9945) 发送飞书消息：要下班了。使用 message tool 发送。"
  },
  "sessionTarget": "isolated",
  "enabled": true,
  "delivery": {
    "mode": "announce"
  }
}
EOF

# 示例 3: 一次性提醒
echo ""
echo "示例 3: 一次性会议提醒"
echo "2026-02-10 14:00 UTC = 2026-02-10 22:00 北京时间"
cat << 'EOF' > /tmp/one-time-reminder.json
{
  "name": "Meeting Reminder",
  "schedule": {
    "kind": "at",
    "at": "2026-02-10T14:00:00Z"
  },
  "payload": {
    "kind": "systemEvent",
    "text": "会议提醒：下午 2 点的技术评审"
  },
  "sessionTarget": "main",
  "enabled": true
}
EOF

# 示例 4: 每 2 小时检查一次
echo ""
echo "示例 4: 每 2 小时检查一次 (7200000ms = 2 小时)"
cat << 'EOF' > /tmp/hourly-check.json
{
  "name": "Bi-hourly Check",
  "schedule": {
    "kind": "every",
    "everyMs": 7200000
  },
  "payload": {
    "kind": "agentTurn",
    "message": "检查系统状态，如果有问题立即通知用户。"
  },
  "sessionTarget": "isolated",
  "enabled": true
}
EOF

# 示例 5: 工作日 9 点提醒
echo ""
echo "示例 5: 工作日 9 点提醒 (UTC 01:00, 北京时间 09:00)"
cat << 'EOF' > /tmp/workday-reminder.json
{
  "name": "Workday Reminder",
  "schedule": {
    "kind": "cron",
    "expr": "0 1 * * 1-5",
    "tz": "UTC"
  },
  "payload": {
    "kind": "systemEvent",
    "text": "REMINDER: 开始工作，检查待办事项"
  },
  "sessionTarget": "main",
  "enabled": true
}
EOF

echo ""
echo "=== 示例任务配置已生成 ==="
echo ""
echo "如何使用这些示例："
echo "1. 使用 OpenClaw cron tool 添加任务："
echo "   cron add --job @/tmp/github-sync.json"
echo ""
echo "2. 或者直接在对话中描述需求，AI 会自动创建任务"
echo ""
echo "3. 查看所有任务："
echo "   cron list --includeDisabled"
echo ""
echo "4. 查看任务运行历史："
echo "   cron runs <jobId>"
echo ""
echo "5. 立即运行任务（测试）："
echo "   cron run <jobId>"
echo ""
echo "6. 删除任务："
echo "   cron remove <jobId>"
echo ""
echo "注意事项："
echo "- 所有时间都是 UTC，北京时间需要减去 8 小时"
echo "- systemEvent 适用于简单提醒，sessionTarget 必须是 main"
echo "- agentTurn 适用于复杂任务，sessionTarget 必须是 isolated"
echo "- 发送飞书消息时需要指定正确的 User ID"
