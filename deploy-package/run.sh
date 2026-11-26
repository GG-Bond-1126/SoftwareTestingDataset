#!/bin/sh
set -eu

# 前台启动静态服务并透传退出码；run.sh 与 server.js 同目录（dist/ 内）。
exec node server.js
