# deploy-package（FunctionWeb 部署适配包）

供 trae-deploy 的 function-web 运行时使用：把本目录下的 4 个文件与站点
`public/`（仓库根目录即发布站点）一起作为部署源打包。

## 文件
- `build.sh`：构建脚本。`mkdir -p dist`，把 `public/` 与 `server.js`、`run.sh`、`package.json` 全部拷入 `dist/`，并 `chmod 755 dist/run.sh`。
- `run.sh`：运行时启动脚本。`exec node server.js`，前台运行并透传退出码。
- `server.js`：零依赖 Node.js 静态服务，服务 `__dirname/public`，按 `PORT` 注入、绑定 `0.0.0.0`，支持 MIME / 条件请求 / 字节范围。
- `package.json`：声明 node >=20 与 `npm start`。

## 运行契约
- 远程构建：执行 `build.sh` 产出 `dist/`（自包含，无外部依赖、无 node_modules）。
- 远程运行：以 `dist/` 为工作目录执行 `run.sh`，`server.js` 服务 `dist/public`，端口取 `runtime.port`（8000）。
- 修复历史：此前 V23 的包源只有 ~1.7KB（未含站点内容），导致 `./run.sh: No such file or directory`；本包将内容与服务脚本一并置入 `dist/`，解决该问题。

> 站点内容不在此目录内，直接取自仓库根（即已发布的静态站点）。部署源 = 本目录 4 文件 + 仓库根的 public/ 结构。
