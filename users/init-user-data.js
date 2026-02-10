#!/usr/bin/env node

/**
 * 用户数据初始化脚本
 * 为每个用户创建独立的记忆空间
 */

const fs = require('fs');
const path = require('path');

const USERS = {
  tech: {
    userId: "ou_5c7144a360f68b2db0e434749f5a9945",
    botId: "oc_f6d2e6388d34f539dd37a898b6cf00cc",
    name: "tech",
    dir: "/root/.openclaw/workspace/memory/tech",
    timezone: "Asia/Shanghai",
    github: "china10s"
  },
  wwn: {
    userId: "ou_725f66654653d6c7061d5f99eb8f4df7",
    botId: "oc_71e0965d0a667df9afb65f9bbcfb4453",
    name: "wwn",
    dir: "/root/.openclaw/workspace/memory/wwn",
    timezone: "Asia/Shanghai"
  }
};

const MEMORY_DIR = "/root/.openclaw/workspace/memory";

// 创建主记忆目录
if (!fs.existsSync(MEMORY_DIR)) {
  fs.mkdirSync(MEMORY_DIR, { recursive: true });
  console.log(`✅ 创建主记忆目录：${MEMORY_DIR}`);
}

// 为每个用户初始化数据
for (const [user, config] of Object.entries(USERS)) {
  console.log(`\n👤 初始化用户：${user}`);
  
  // 创建用户目录
  if (!fs.existsSync(config.dir)) {
    fs.mkdirSync(config.dir, { recursive: true });
    console.log(`  ✅ 创建目录：${config.dir}`);
  }
  
  // 创建今日记录文件
  const today = new Date().toISOString().split('T')[0];
  const dailyPath = path.join(config.dir, `${today}.md`);
  if (!fs.existsSync(dailyPath)) {
    const dailyContent = `# ${today} - ${config.name} 的每日记录\n\n---\n\n## 会话活动\n\n待记录...\n\n---\n\n## 任务和提醒\n\n待记录...\n\n---\n\n## 重要事项\n\n待记录...\n`;
    fs.writeFileSync(dailyPath, dailyContent, 'utf-8');
    console.log(`  ✅ 创建今日记录：${dailyPath}`);
  }
  
  // 创建用户偏好文件
  const prefsPath = path.join(config.dir, 'preferences.md');
  if (!fs.existsSync(prefsPath)) {
    const prefsContent = `# ${config.name} 的用户偏好\n\n## 个人信息\n- 名称：${config.name}\n- 用户ID：${config.userId}\n- 机器人ID：${config.botId}\n- 时区：${config.timezone}\n${config.github ? `- GitHub：${config.github}` : ''}\n\n## 偏好设置\n\n### 对话风格\n- 待记录...\n\n### 功能偏好\n- 待记录...\n\n---\n\n## 常用命令\n\n待记录...\n`;
    fs.writeFileSync(prefsPath, prefsContent, 'utf-8');
    console.log(`  ✅ 创建用户偏好：${prefsPath}`);
  }
  
  // 创建提醒任务文件
  const remindersPath = path.join(config.dir, 'reminders.md');
  if (!fs.existsSync(remindersPath)) {
    const remindersContent = `# ${config.name} 的提醒任务\n\n## 活跃提醒\n\n### 一次性提醒\n无\n\n### 周期性任务\n无\n\n---\n\n## 已完成提醒\n\n待记录...\n`;
    fs.writeFileSync(remindersPath, remindersContent, 'utf-8');
    console.log(`  ✅ 创建提醒任务：${remindersPath}`);
  }
}

// 创建一个用户索引文件
const indexPath = path.join(MEMORY_DIR, 'INDEX.md');
const indexContent = `# 用户数据索引\n\n## 用户列表\n\n### tech\n- 用户ID：${USERS.tech.userId}\n- 机器人ID：${USERS.tech.botId}\n- 数据目录：${USERS.tech.dir}\n- 时区：${USERS.tech.timezone}\n- GitHub：${USERS.tech.github}\n\n### wwn\n- 用户ID：${USERS.wwn.userId}\n- 机器人ID：${USERS.wwn.botId}\n- 数据目录：${USERS.wwn.dir}\n- 时区：${USERS.wwn.timezone}\n\n## 数据目录结构\n\n\`\`\nmemory/\n├── tech/\n│   ├── YYYY-MM-DD.md       # 每日记录\n│   ├── preferences.md       # 用户偏好\n│   └── reminders.md         # 提醒任务\n└── wwn/\n    ├── YYYY-MM-DD.md       # 每日记录\n    ├── preferences.md       # 用户偏好\n    └── reminders.md         # 提醒任务\n\`\`\`\n\n## 隐私规则\n\n- ❌ 不在回复中提及其他用户\n- ❌ 不读取其他用户的文件\n- ❌ 不泄露其他用户的信息\n- ✅ 只访问和回复当前用户的数据\n`;
fs.writeFileSync(indexPath, indexContent, 'utf-8');
console.log(`\n✅ 创建用户索引：${indexPath}`);

console.log('\n✅✅✅ 用户数据初始化完成！');
console.log('\n📋 下一步：更新 USER.md 和 SOUL.md，引用用户数据路径');
