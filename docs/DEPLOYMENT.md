# 部署

当前交付是可运行的本地项目与静态生产构建，未绑定任何公开域名，也未使用用户部署凭据。

## Vercel / Netlify

把 `brick-atlas` 作为站点根目录：

- 安装：`npm ci`
- 构建：`npm run check`
- 发布目录：`dist`
- Node：22.23.2
- 不需要环境变量、数据库或运行时服务端。

仓库中提供 `vercel.json` 与 `netlify.toml`。部署者需要在自己的账户中创建项目并批准公开发布。无需上传 `.tools`、`node_modules` 或完整的零件库 ZIP。

## 普通静态主机

```bash
npm ci
npm run check
npm run preview
```

把 `dist/` 内容发布到 HTTPS 静态站点。必须使用 HTTPS（localhost 除外），因为 Worker 使用 Web Crypto。不要为不存在的 `/models/*` 请求返回 SPA index.html。

缓存要求：

| 路径 | 缓存 |
|---|---|
| `/assets/*` | `public, max-age=31536000, immutable` |
| 含内容哈希的 `/models/*/*.bin` | `public, max-age=31536000, immutable` |
| manifest、credits、provenance JSON | `max-age=0, must-revalidate` |
| index.html | `max-age=0, must-revalidate` |

`.bin` 内部已有 gzip 压缩，由 Worker 手动解压，**不要给这个存储载荷添加 `Content-Encoding: gzip`**。服务器如额外做传输压缩，只能对已有文件再压缩一层并正确设置对应 Content-Encoding。最简单的方法是不额外压缩 `.bin`。

默认根路径 `/`。子目录部署需要设置 Vite `base`，并将部署平台的缓存与安全路径规则对应调整；`BASE_URL` 已用于模型资产与 Worker 下载根路径。

## CI

`.github/workflows/ci.yml` 包含离线数据重建、差异检查、类型检查、单元测试、参考加载对照、四环境 Playwright 和依赖审计。CI 从版本控制中的已锁定依赖子集构建，不下载会变化的完整库。

## 发布前人工门禁

1. 确认目标账号、域名、发布可见范围与素材署名。
2. 在实际 Safari 和至少一台真实手机上旋转、缩放、点选、隔离并复原。
3. 在 LDView/LeoCAD 等外部查看器中加载原始 MPD，与 0% 视图逐角度对照。
4. 检查 HTTPS、安全头、冷缓存、慢网、404、Worker MIME 类型和上下文恢复。
5. 对生产 URL 实测完整加载、交互帧率和内存，记录设备与网络条件。
6. 如需远程监测，先确定接收服务、保留周期与隐私政策，再接入。

## 本地服务器

`Start.command` 前台启动，退出终端或 Ctrl+C 停止。`npm run start:local` 后台启动并输出自己的 PID，可用 `kill <PID>` 停止该项目进程，不应停止其他项目的服务器。脚本会先找空闲端口，避免复用或占用现有服务。
