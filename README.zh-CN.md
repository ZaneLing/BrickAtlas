<p align="center">
  <img src="docs/media/brick-atlas-mark.svg" width="760" alt="Brick Atlas 动态积木标识">
</p>

<h1 align="center">Brick Atlas</h1>

<p align="center">
  用于探索 LDraw 模型、检查单块积木、查看拼装说明和自由创作的桌面端三维工作空间。
</p>

<p align="center">
  <a href="README.md">English</a> · <strong>简体中文</strong>
</p>

## 功能演示

### 1. 三维展开：0% → 100% → 0%

https://github.com/user-attachments/assets/77e02f26-285b-4b47-a3f5-080b395bf07f

### 2. 分步拼装

https://github.com/user-attachments/assets/8f964a18-3408-4908-aced-dff1d4d4a31e

### 3. Create：图片生成积木

https://github.com/user-attachments/assets/46452ae9-0480-4387-ad05-a8f0d9dddd14

### 4. 自由 DIY

https://github.com/user-attachments/assets/175498ed-8c62-4598-a748-9ffaaef4f89b

## 主要功能

- 浏览 15 个来源可追溯的真实 LDraw 模型，支持高清物理渲染、旋转、缩放、平移、视角切换和三维展开。
- 选择任意积木，查看零件编号、颜色、尺寸、子装配和三维形状；支持搜索、隐藏、隔离、同类高亮和 X-Ray。
- 在中央三维画布中逐步播放拼装过程，并查看高清静态入位图、当前步骤零件和 PDF 说明书。
- 在线拼装游戏会校验步骤、型号、颜色、数量和 90° 方向，保存中途进度，并在完成后显示勾选标识。
- Compose 可将飞机、船、车辆、建筑、角色、动物、底板和散件组合成新场景。
- DIY 提供 78 种零件、18 种颜色和 12 个小组件，支持旋转待放或已放置积木、自动叠放、碰撞与支撑检查、撤销和重做。
- Create 默认先通过公开 TripoSR 或 Stable Fast 3D 服务生成真实 GLB 网格，再在 Worker 中体素化和积木化；也提供明确标注的本地深度、多视图备用方案。
- 导出 PDF 拼装说明、BOM CSV、LDraw、JSON 和最高 12K 图片。
- 整个界面支持中英文切换。

Brick Atlas 面向宽度至少 1180 px 的桌面浏览器。

## 页面

- `/` 模型目录与自动三维功能演示
- `/explore/:modelId` 模型探索
- `/build/:modelId` 动态拼装说明
- `/assemble` 分级手动拼装目录
- `/assemble/:modelId` 带材料和方向校验的拼装游戏
- `/compose` 组件、底板和散件组建
- `/diy` 无限底板自由拼搭
- `/create` 照片转三维网格再转积木

## 本地运行

需要 Node.js 22 或更新版本：

```bash
npm ci
npm run dev
```

打开 `http://127.0.0.1:5173`。本地功能不需要数据库或私有后端。

Create 默认使用可匿名调用的公开 TripoSR CPU 服务。官方 ZeroGPU 服务可在有匿名额度时使用，也可以在页面临时输入 Hugging Face Token 以获得更多额度；Token 只保存在当前页面内存中，不会写入项目或浏览器存储。照片只会在用户点击“生成真实三维网格”后发送到所选公开服务。

## 图片转积木

默认流程为：

```text
现实物品照片
→ 公开 Image-to-3D 服务
→ 真实 GLB 三角网格
→ Worker 网格体素化
→ 积木打包、步骤、BOM 和 LDraw
```

用户可以在原始网格和积木结果之间切换，并下载中间 GLB。公开服务不可用时会显示真实错误，不会把本地深度外壳伪装成网格结果。详细说明见 [图片转积木流程](docs/IMAGE_TO_BRICKS.md)。

## 模型与许可

模型资源来自 [LDraw Official Model Repository](https://library.ldraw.org/omr/sets)，项目保留每个模型的来源、作者、许可、下载地址和哈希记录。

代码使用 MIT 许可证。模型与 LDraw 零件适用各自的许可证。Brick Atlas 是非官方社区项目，与 LEGO Group 无附属、赞助或认可关系。

## 验证

```bash
npm run check
npm run test:e2e -- --project=desktop-chrome
npm audit
```

测试范围和已知限制见 [工程审计](docs/ENGINEERING_AUDIT.md)。
