# Brick Atlas

非官方积木模型探索与分步拼装工作空间。提供 8 个可追溯 LDraw OMR 模型、逐块积木数据、交互式步骤动画和可导出的 PDF 说明书。

## 立即运行

本机已准备 Node.js 22.23.2。在 macOS 上双击 `Start.command`，或在项目目录执行：

```bash
export PATH="$PWD/.tools/node-v22.23.2-darwin-arm64/bin:$PATH"
npm ci
npm run dev
```

默认地址为 `http://127.0.0.1:5173`。端口占用时 Vite 会选下一个端口，地址以终端为准。也可以执行 `npm run start:local` 后台启动，日志在 `.tools/dev-server.log`。

其他机器安装 Node.js 22+ 后，直接 `npm ci && npm run dev`。应用运行不需要下载完整零件库、不需要后端、不需要 API Key、不需要连接任何第三方 CDN。必须通过 HTTP 或 HTTPS 访问，不能双击 `index.html`。

## 已实现

- 8 个项目、1030 个可追溯积木实例；每块积木使用稳定的 `brick_000001` 格式 ID。
- `/` 项目库、`/explore/:modelId` 探索、`/build/:modelId` 拼装、`/create` 本地预检。
- 独立 `BrickModel` 数据层和 Zustand Viewer Store；Three.js 只消费模型与视图状态。
- OrbitControls 旋转、平移、缩放、五种视角、自动旋转、复原、截图。
- 0% 完整装配，45% 结构分离，100% 每实例独立陈列，连续可逆。
- 六个结构分组显隐、同型号高亮、单实例/同型号/子模型隔离。
- X-Ray、搜索即时高亮、积木尺寸、积木树、Where Used 和逐实例隐藏。
- 分步拼装、暂停/播放、步骤目录、本步零件表、静态步骤图与进度持久化。
- 横向 A4 PDF 说明书导出；每步包括零件清单、数量、静态拼装图和来源声明。
- Full HD、4K、8K 独立渲染截图和 1x/2x/3x 实时像素密度。
- 零件编号、名称、颜色、类别、路径搜索；搜索结果自动显示父组。
- 点选与悬浮、独立关闭详情/清除选择、同型号逐实例导航、CSV 导出。
- 真实材质与条件边线、分组分块加载、Worker 校验和解压。
- 材质合批 + instanceIndex + GPU 状态纹理；CPU 包围盒粗筛和精确拾取。
- 手机底部抽屉、触控防误选、双指缩放、低质量模式、reduced-motion。
- 404/下载校验失败/WebGL 不可用/上下文丢失/React 异常的可恢复错误状态。
- Source & Credits、逐文件署名、来源哈希、可重复离线构建、CI、部署配置。

## 模型与许可

模型包括 5867 Super Speedster、31027 Blue Racer/Kart、31028 Sea Plane/Sailboat、31009 Small Cottage、10014 Caboose 和 10156 LEGO Truck。每个模型的 OMR 来源、作者、固定哈希和许可在 `atlas.config.ts` 及其发布目录的 `provenance.json`、`credits.json` 中记录。

零件库：2026-08-31 的 `complete.zip` 快照；每个依赖单独检查作者与许可，保留原始文件和历史。依赖文件可能同时涉及 CC BY 2.0 与 CC BY 4.0，不统一冒称为一个许可。代码采用 MIT，与模型许可分离。

31009 与 10156 使用 OMR 作者提供的 STEP 元数据。其他模型明确标注为编辑性的结构演示，不冒充 LEGO 官方纸质说明书，也不声称经过实物碰撞或拼搭验证。

## 数据构建

```bash
npm run acquire            # 验证固定哈希，缺少时下载模型及完整库
npm run assets:build       # 依赖闭包、许可检查、manifest、packed MPD、几何分块
npm run assets:validate    # 所有实例、源行、矩阵、哈希、包围盒、顶点身份
npm run assets:reference   # 与原始层级 MPD 的独立加载路径逐实例对照
npm run assets:repro       # 不读完整库、不联网，检查产物逐字节一致
```

`complete.zip` 的在线 URL 会随官方版本更新。哈希不匹配时 `acquire` 会停止，绝不自动接受新版。现有的 `assets-source/ldraw-library/locked/` 已包含该模型所需的完整依赖子集，受 `library-lock.json` 校验，可离线重建。

生成物实际服务目录是 `public/models/<modelId>/`；`assets-built/` 存放构建、基准对照、可复现性、性能及 E2E 报告。压缩几何使用 `.bin` 扩展名，内容是 gzip。

## 验证

```bash
npm run check
npx playwright install firefox webkit
npm run test:e2e
npm run benchmark
npm audit
```

本机 Playwright 使用已安装 Chrome。CI 自动安装 Chromium、Firefox、WebKit。浏览器覆盖桌面 Chrome、移动模拟 Chrome、Firefox 和 WebKit。WebKit 自动化不是已完成真实 Safari 或 iPhone 实机验收的声明。

详见 [验收状态](docs/ACCEPTANCE.md)、[架构](docs/ARCHITECTURE.md)、[部署](docs/DEPLOYMENT.md)。

## 工程目录

```text
atlas.config.ts                 套装标识与来源配置
assets-source/
  set-original/                 不修改的原始 MPD
  ldraw-library/locked/          固定版本依赖子集
  classification.json           可审查的编辑分组规则
  provenance.json               原始素材来源、日期、哈希
  library-lock.json              逐依赖哈希
  license/                      许可原文与来源页快照
src/
  app/                          路由页面、界面、诊断与异常边界
  instructions/                 步骤零件聚合与 PDF 说明书导出
  scene/                        Three.js、GPU 状态与拾取
  explosion/                    双阶段布局与 shelf packing
  model/                        BrickModel、语义类型、查询与显隐规则
  store/                        Zustand Viewer Store 与拼装进度
  ui/                           图标按钮与无障碍弹窗
  workers/                      渐进下载、SHA-256、解压
scripts/                        采集、构建、验证和基准
tests/                          单元、交互、视觉、无障碍与异常测试
public/models/<modelId>/        可发布模型资产与真实预览图
assets-built/                   实测报告
```

## 尚需外部完成

没有使用部署账号，项目**尚未公开上线**。未完成真实手机、已安装 Safari 和独立 LDView 的人工对照，也未接入远程错误收集服务。运行诊断目前只在本次页面内存中保存，可在设置中导出，不上传用户数据。
