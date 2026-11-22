# Tripo 与 Meshy：从参考图到本地资产

## 先确认实际接口、授权与成本

- 有可用网格就先本地验收。确需生成时，默认用官方 CLI 的显式子命令；要精确指定视角/字段或没有 CLI 时用 REST。已有官方 MCP 才优先复用；界面独占功能走网页或交给操作者。不要逆向网页接口或复用网页 cookie。
- 先用 `--help`、MCP `tools/list` 和对应 REST 页面核对模型、能力、请求字段、限制。CLI 默认值与 REST 可能不同。关键能力（四边面、裸网格、保留 UV、单次生成）无法表达时换已确认的接口，勿静默降级或打开自动拆件。
- 提交前记录服务、区域、帐号/额度、允许外传的文件、按视角的哈希、模型标识、参数、预计次数和费用。无授权只写计划。安装与登录由宿主授权，登录验证码交给用户；凭据从宿主管理的注入渠道获取，不打印密钥、签名链接或 data URI，不把私图发布为公网 URL。允许调用不等于允许购买额度或开订阅。
- 先提交一次并保存任务类型和 ID，再有界轮询同一任务。查询超时不是生成失败。创建请求送出后响应丢失，先查看任务历史或账户任务，无法确认就停，不能自动重发或切平台再提交。对查询用服务商规定的间隔/退避；读取失败详情、实际扣费，保留原始文件并尽快下载有时效的资产。

## Tripo

查 [官方 CLI](https://developers.tripo3d.ai/en/docs/cli)、[鉴权与区域](https://developers.tripo3d.ai/en/docs/authentication)、[计费](https://developers.tripo3d.ai/en/docs/billing)、[版本](https://developers.tripo3d.ai/en/docs/models-and-versions)。从 [单图 P 系列](https://developers.tripo3d.ai/en/docs/generation-image-to-model/p) / [多图 P 系列](https://developers.tripo3d.ai/en/docs/generation-multiview-to-model/p) 查智能拓扑，从对应 H 系列页面查高精度选项；不要把 v2 的 `/task` 信封和字段套到 v3。

**CLI**：用 `tripo whoami`、`tripo balance` 核对已授权的账号。显式用 `tripo generate image-to-model` 或 `tripo generate multiview-to-model`，后者按文件名提示或位置分配视角；命名为 `front.png`、`back.png`、`left.png`、`right.png`，若有歧义用下面的具名 REST。以下为一次需授权的示例；先以 `--help` 和 P 系列文档复核模型与参数：

```sh
tripo generate multiview-to-model ./front.png ./back.png --model P2-20260801 \
  -p face_limit=10000 -p quad=true -p texture=false -p pbr=false --no-wait --json --no-open
tripo task watch "$TASK_ID" --download -o ./out/tripo --json --no-open
```

**REST v3**：全球端点 `https://openapi.tripo3d.ai/v3`；区域按鉴权文档。以 Bearer 鉴权。小图用 `POST /files` 的 multipart `file` 上传 PNG/JPEG，取 `data.file_token`；私有原图无需公开。单图 `POST /generation/image-to-model` 传字符串 `input`；多图 `POST /generation/multiview-to-model` 用具名对象数组，至少两张且含正面；不要把背面放进第二个位置参数冒充左侧。示例请求体：

```json
{"inputs":[{"front":"file_EXAMPLE_FRONT"},{"back":"file_EXAMPLE_BACK"}],"model":"P2-20260801","face_limit":10000,"quad":true,"texture":false,"pbr":false}
```

保存 `data.task_id`，用 [GET `/tasks/{id}`](https://developers.tripo3d.ai/en/docs/task-query) 查；`success` 后下载 `data.output.model_url`（按实际返回格式保存）。`failed` / `cancelled` 停。几何通过后可用 [POST `/models/texture`](https://developers.tripo3d.ai/en/docs/models-texture) 对原任务 ID 贴图；若已在本地修形，必须基于修好的副本或在本地烘焙，不要套回旧几何。先在界面或文档确认四边面在所选导出格式下保留；GLB 底层为三角网格，保留四边编辑拓扑优先用 FBX/源 `.blend`。

**MCP**：官方 CLI 的 `tripo mcp` 是 stdio，默认提供聚合的 make/task/balance/history，需精确操作时查 `tripo mcp --help` 与完整工具集的实际模式。另有 [Tripo Blender MCP](https://github.com/Tripo-Developer/tripo-mcp)，依赖 Tripo Blender 插件和运行中的 Blender，不能当成通用 `bpy` 或假定支持当前所有 API 参数。不要把可执行代码的 Blender 桥暴露到网络。

**人工兜底**：[Tripo Studio](https://www.tripo3d.ai/app/home) → 智能拓扑 → 上传正面 → 把已有背/侧图放进对应槽（只有缺图且获准时才生成并审核补视图）→ 通用设置 → 选 P 系列、四边面、生成数量；若已授权比较多个档位，关闭「使用相同面数」，分别填预算。提交前确认模型与输入的可见性、次数和额度。生成并用统计/线框对比候选后，只有局部坏形才选「局部重试／重塑」；将黄色空间框包住缺陷，从斜侧确认深度，运行后切换「上一版本／当前版本」，检查周围和实际面数，满意才保存修改，否则继续编辑或保留原版；该操作不能用通用 Retopology 当作等价替代。确认几何后「生成贴图」选分辨率，核查颜色溢出，再「导出」选带纹理格式和 Blender 预设（若提供）。

## Meshy

从 [Agent 文档索引](https://docs.meshy.ai/llms.txt)、[CLI](https://docs.meshy.ai/en/api/cli)、[AI/MCP](https://docs.meshy.ai/en/api/ai)、[模型表](https://docs.meshy.ai/en/api/models) 和[费用](https://docs.meshy.ai/en/api/pricing) 查。端点页可加 `.md` 读取纯文本。注意普通多图、单图智能拓扑和批量独立出图是不同入口。

**CLI**：`meshy doctor` 检环境；使用已授权配置，需登录时走 `meshy auth login`，无浏览器 Agent 按官方文档请用户完成设备授权。`meshy make --dry-run` 用于预估对应 make 链，不能替代显式端点的计费核对。示例提交一次无贴图的多视图草模（以下需授权；支持时用本地任务流水号 `--operation-id`）：

```sh
meshy multi-image-to-3d create --image-urls ./front.png,./back.png \
  --should-texture false --target-formats glb --async --format json
meshy multi-image-to-3d wait "$TASK_ID" -o ./out/meshy --format json
```

从创建结果取 `result.submission.task_id`，从查询结果读 `result.task.status`；`ok: true` 只表示 CLI 执行成功。超时恢复同 ID，创建结果未知则先 `meshy <resource> list`。导出贴图等附属文件用 `--all-assets`（见当前帮助）。

**REST**：全球端点 `https://api.meshy.ai/openapi/v1`，用 Bearer 鉴权。[单图](https://docs.meshy.ai/en/api/image-to-3d) `POST /image-to-3d` 传 `image_url`；[多图](https://docs.meshy.ai/en/api/multi-image-to-3d) `POST /multi-image-to-3d` 传 `image_urls`（1–4 张、受支持的 data URI 或已授权可公开直链；支持首张作正面的模型要将正面放第一）。裸网格设 `should_texture:false`，需要时设 `target_formats:["glb"]`；多图的 `geometry_resolution` 是几何档位，不是贴图解析度。单图智能拓扑用 `model_type:"smart-topology"`、匹配的 `ai_model` 和 `target_polycount`（目标三角面数），不能直接照搬到多图。取响应 `result` 为 ID，按同类型 `GET /<resource>/<id>` 或官方 SSE 查询；`SUCCEEDED` 后下载 `model_urls.glb` 与所需的 `texture_urls`，`FAILED` / `CANCELED` 停。

**分阶段贴图**：几何确认后可用 [Retexture](https://docs.meshy.ai/en/api/retexture) 传成功的 Meshy API `input_task_id`，或传本地修好资产的 `model_url`（data URI/直链须授权）；已有好 UV 时用 `enable_original_uv:true` 并实测是否保留。单图、多视图或文本风格按文档选一；例如 N1 是 2K 基色，不接 PBR，不能用纯文本。结果即便颜色更对也要对照裂缝、线框、UV、绑定与标识，失败则保留原几何并在本地修贴图。

**MCP**：使用官方 `@meshy-ai/meshy-mcp-server`，由宿主注入 `MESHY_API_KEY`。发现 `meshy_image_to_3d` / `meshy_multi_image_to_3d`、`meshy_get_task_status`、`meshy_download_model` 的现行工具模式，确认下载路径和类型。MCP 不是免费生成入口，权限与计费走同一 API。

**人工兜底**：[Meshy 网页](https://docs.meshy.ai/en/webapp/image-to-3d) → Model → Image to 3D → High Detail 或 Smart Topology → 上传视角、选模型/几何预算 → 生成 → 打开候选转台/线框 → 按需 Remesh/Retexture → Download 并保存所选格式和贴图。界面找不到对应多图槽或费用不明时，不用 Batch Images 代替；交回同样的输入与参数要求。

## 候选交接

用同一授权输入和视角、同一桌面显示尺寸比候选。先看正侧背轮廓、关节、配件遮挡和变形潜力，再比实际三角面、UV 和颜色。记录胜出与淘汰原因、需 Blender 修的区域；保留原始下载、可编辑格式、贴图、已脱敏请求摘要与任务 ID。不能从网页或预览图确认的资产属性，导入后实测。
