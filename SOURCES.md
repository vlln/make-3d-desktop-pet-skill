# 开发与验证记录

## 0.4.1

- 在 `providers.md` 增加「用途决定档位」：桌宠走智能拓扑，打印/展示向功能（高精度档、8K、多色打印、自动拆件、水密修复）默认不选；已有高面数成品降面用 [Meshy Remesh](https://docs.meshy.ai/en/api/remesh) 或 Tripo retopology，不在 Blender 全局抽面。补记 Meshy 单图 `smart-topology` 为三角面为主、多图无智能拓扑，与 Tripo P 系列四边面优先不同。依据 [Remesh API](https://docs.meshy.ai/en/api/remesh) 与[官方重拓扑指南](https://www.meshy.ai/zh/tutorials/ai-retopology-guide)。接口能力以 2026-11 文档为准，使用前按对应页面复核现行字段。

## 0.4.0

- 在生成网格前增加图像验收关卡：保留批准基准，用同视角对照比例与身份，分开检查多视图一致性和重建条件，明确通过、局部复审或退回。不需要为已合格的原图重绘。
- 公开版仅收录自编文档、脚本、原发布链接与时间点。第三方归档仍在本地项目内，并排除在 Git 与 Skill 安装包之外。

## 0.3.0

- 修订起因：初版保留了主流程，但省略了若干故障判据和人工路径，也没有交代 Agent 如何访问服务和 Blender。按[八集复核记录](docs/tutorial-evidence/coverage.md)逐集对照转写与抽样画面，把操作和判据写回各阶段；案例读数与未证实的解释留在项目资料。
- 云接口依据：[Tripo v3 P 系列](https://developers.tripo3d.ai/en/docs/generation-multiview-to-model/p)、[Tripo CLI](https://developers.tripo3d.ai/en/docs/cli)、[Tripo Blender MCP](https://github.com/Tripo-Developer/tripo-mcp)、[Meshy CLI](https://docs.meshy.ai/en/api/cli)、[Meshy AI/MCP](https://docs.meshy.ai/en/api/ai)、[Meshy 多图](https://docs.meshy.ai/en/api/multi-image-to-3d)及 [Retexture](https://docs.meshy.ai/en/api/retexture)。本机临时安装 Tripo CLI 0.11.2 与 Meshy CLI 0.8.7，验证子命令帮助、Tripo 离线正背图映射和 P 系列请求体、Meshy `make --dry-run` 的 `requests_made: 0`。未登录、上传、收费或实调 MCP。
- Blender 依据：[命令行参数](https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html)、[Python API](https://docs.blender.org/api/current/)、[VRM 扩展脚本示例](https://vrm-addon-for-blender.info/en-us/scripting-api/)及[格式规范](https://github.com/vrm-c/vrm-specification)。本机 Blender 5.2.4 / VRM 扩展 4.10.5：后台启动时发现扩展但未注册，进程内启用后对既有模型做 `.blend` 与 `.vrm` 只读检查、另存 VRM 和新进程重导入；重导入识别 7 个网格、21 根骨、202,895 三角面和 4 张打包图片。另测合成 GLB 与报告禁止覆盖。结构测试不替代变形、物理或桌面验收；未重做角色或修改部署。

## 0.2.0

- 技能按制作阶段组织。每阶段给出可执行操作、适用条件和验收标准。

## 0.1.0

- 首版覆盖图像输入、拓扑、贴图、VRM 蒙皮、物理、表情和实装。
- 以已有鲸鱼娘三视图、源模型与 macOS 运行时为例演练技能路由。尚待用新角色实测生成到实装的完整流程。
