#!/bin/bash
# 每天凌晨2点自动同步工作区到 GitHub

set -e

WORKSPACE="/root/.openclaw/workspace"
cd "$WORKSPACE"

# 添加所有更改（包括删除的文件）
git add -A

# 检查是否有变更
if git diff --cached --quiet; then
    echo "No changes to commit. Exiting."
    exit 0
fi

# 提交
COMMIT_TIME=$(date '+%Y-%m-%d %H:%M:%S')
git commit -m "Auto-sync at $COMMIT_TIME"

# 检查是否是第一次推送（远程分支不存在）
if ! git ls-remote --heads origin master &>/dev/null; then
    echo "First push: forcing to overwrite remote..."
    git push -u origin master --force
else
    # 正常推送
    echo "Pushing changes to remote..."
    git push origin master
fi

echo "Sync completed at $COMMIT_TIME"
