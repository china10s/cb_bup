/**
 * 入站消息路由器
 * 当主会话收到消息时，spawn 子会话处理，实现用户隔离和并发
 */

const USER_SESSIONS = {
  // 技术的用户 ID
  tech: {
    userId: "ou_5c7144a360f68b2db0e434749f5a9945",
    botId: "oc_f6d2e6388d34f539dd37a898b6cf00cc",
    name: "tech",
    sessionLabel: "tech_feishu_dm"
  },
  // wwn 的用户 ID
  wwn: {
    userId: "ou_725f66654653d6c7061d5f99eb8f4df7",
    botId: "oc_71e0965d0a667df9afb65f9bbcfb4453",
    name: "wwn",
    sessionLabel: "wwn_feishu_dm"
  }
};

/**
 * 根据消息来源识别用户
 */
function identifyUser(message) {
  const from = message?.from || message?.origin?.from || message?.senderId;

  for (const [key, config] of Object.entries(USER_SESSIONS)) {
    if (from === config.userId || from === `feishu:${config.userId}`) {
      return { key, config };
    }
  }

  return null;
}

/**
 * 创建用户特定的系统提示
 */
function createUserSystemPrompt(userConfig) {
  return `
你正在处理 ${userConfig.name} 的消息。

重要规则：
1. 只回复给 ${userConfig.name}，不要泄露其他用户的信息
2. 使用你的默认人设和风格与 ${userConfig.name} 对话
3. ${userConfig.name} 的用户 ID 是 ${userConfig.userId}
4. ${userConfig.name} 的飞书机器人 ID 是 ${userConfig.botId}

${userConfig.name} 的偏好（如果有的话）：
- 时区：Asia/Shanghai
- GitHub：china10s（仅对 tech）

保持自然、友好的对话风格。就像你平时那样回复即可。
  `.trim();
}

/**
 * 路由消息到子会话
 * 返回 true 如果应该 spawn 子会话，false 如果应该在主会话直接处理
 */
function shouldRouteToSubAgent(message) {
  // 如果消息明确指示不需要路由，直接处理
  if (message?.routing === "direct") {
    return false;
  }

  // 识别用户
  const user = identifyUser(message);
  if (!user) {
    console.log("[InboundRouter] 未知用户，在主会话处理");
    return false;
  }

  // 已知用户，路由到子会话
  console.log(`[InboundRouter] 识别到用户 ${user.config.name}，路由到子会话`);
  return true;
}

/**
 * 获取子会话的 session key
 */
function getSubAgentSessionKey(userConfig) {
  return `agent:main:feishu_dm_${userConfig.userId}`;
}

/**
 * 获取子会话的标签
 */
function getSubAgentLabel(userConfig) {
  return userConfig.sessionLabel;
}

// 导出供其他模块使用
module.exports = {
  identifyUser,
  createUserSystemPrompt,
  shouldRouteToSubAgent,
  getSubAgentSessionKey,
  getSubAgentLabel,
  USER_SESSIONS
};
