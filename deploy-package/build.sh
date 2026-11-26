#!/bin/sh
set -eu

# 自包含静态站点构建：把 public/ 与运行所需文件全部拷入 dist/，
# 运行时以 dist/ 为工作目录，run.sh 与 server.js 都位于 dist/ 内。
mkdir -p dist
cp -R public/. dist/public/
cp server.js run.sh package.json dist/
chmod 755 dist/run.sh
echo "build done: dist/ ready"
