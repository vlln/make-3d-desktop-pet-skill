# Blender：网格、贴图和第一次 VRM 导出

Agent 的脚本入口与操作对照见 `$_S/references/blender-agent.md`。以下是同一流程的手工路径与判据，快捷键以 Blender 默认键位为例。交接时保存阶段副本，不覆盖原始资产。

## 网格：先判断是网格、UV，还是材质

1. **导入和摆正。** 文件 → 导入 → FBX 或 glTF/GLB。用 View → Viewpoint 的 Front/Right/Back 和材质预览确认朝向。仅有侧转时才绕 Z 校正（例如某些 FBX 需要 −90°，不是固定规则）。核对脚底高度、尺寸、镜像方向、材质与纹理。通过 Edit → Preferences → Get Extensions 安装 [VRM 扩展](https://extensions.blender.org/add-ons/vrm/)，N 侧栏查 VRM 页。
2. **重合点。** 编辑模式、顶点选择，Mesh → Clean Up → Merge by Distance（也可 `M` → 按距离合并）。先用小阈值和局部导入块验证。记录合并数，确认原本独立的发片、手指和 UV 边界没粘起来；处理已有绑定或形态键的网格前先备份，不做全局重焊。
3. **删除错误赘物。** 取消旧选择再悬停 `L`；或先选一个种子顶点 → Select → Select Linked → Linked（`Ctrl+L`）。确认只选中错误孤岛，并保留原画中真实的非对称饰件。孤岛可删除，若 `L` 连带整片有效头发，则转局部面选，必要时用 Select → Select More/Less 扩一圈；别整片删掉。
4. **补洞只改局部。** 编辑模式删除局部错误面后选边界环，简单小洞用 Face → New Face from Edges（`F`）封面；非平面或弯折关节补可变形的面环。检查法线与轮廓。若补的位置突然出现跨区图案，先检查新面的 UV，不要直接往脸或头发整片重画。
5. **只重展补片。** UV Editing → 选新面 → UV Sync Selection（视版本可开关验证对应关系）→ View → Frame Selected 定位 → UV → Unwrap。缩小并放到相邻同色区或预留空位（空位需补色并留 padding）；检查邻面 UV 不变、纹理 mip 缩小不串色。没有必要为细碎缺陷整体改布线。

## 贴图：先取无光基色，再遮罩修补

先切实体视图的 Shading 下拉 → Lighting: Flat，Color: Texture（或直接在 Image Editor 取原 Base Color）。不要吸场景灯下的材质预览色。Texture Paint 用邻近基色修色斑，软笔刷/低 Strength 做交融；重复花纹用 Clone，默认键位 `Shift+右键` 在 3D 视图定位克隆源；小范围色彩过渡可 Smear，拉过头就撤销或回补。`Shift+X`、`F` 分别是默认键位的取色和改笔刷大小，必要时看工具提示，避免用错键位。

发丝与脸相贴时，编辑模式先用连通块或局部面选出发片；有需要可临时切 Studio 照明看清选区。回 Texture Paint 启用 Face Selection Masking，验证遮罩只允许画目标面。关掉不需要的镜像绘制，并确认没有重叠 UV，否则未选中的面仍可能共享被修改的像素。修完关闭遮罩。Image Editor → Image → Save As 写新贴图，File → External Data → Pack Resources 打包，重开核对。切回 Material Preview，比原材质、MToon 和实际桌宠尺寸；只修仍可辨认的色斑/溢色，卡通弱化的视觉瑕疵可不修，但不能跳过真实穿模或断裂。

## 骨架拟合：先大关节，再指骨

- 3D 视图 `N` → VRM → Create VRM Model（创建 VRM 模型，标签以扩展版本为准）添加 Humanoid/T-Pose 骨架；也可在 Add → Armature 查支持的 VRM 模板。物体模式整体缩放，Viewport Display → In Front。进入骨架编辑模式，对称角色开 X-Axis Mirror，非对称时关掉。Root 是整体移动的父级，不把它错当髋骨移进躯干。
- **正面**定位大腿根、膝、髋/脊柱、胸、肩、肘、腕。用 Viewport Overlays → Wireframe 找被衣物遮住的关节布线；判据是转轴贴近解剖位置，不是骨头都等长。**侧面**从脚踝/脚掌往上核对前后深度、膝弯、脊柱和颈。侧视重叠时 `L` 选链，`Shift+H` 仅显示选中，`Alt+H` 恢复。头骨关键是根在颈部旋转中心，末端长度不决定头部权重。贴图眼不要求一定有独立眼球骨。
- **手部**先用 `L` 整链平移对位，再顶视对逐指关节；吸附菜单选 Volume（合适时用体积中心），移动时用 `Ctrl` 临时吸附，微调深度时关闭吸附。圆柱状手指/胳膊适用；贴得太紧的手指须检查是否吸到邻指。近掌指节通常较长，按造型定数值，不复制等距假关节。交叉检查顶部、侧面及单指内弯，手腕不能把邻指带动。

## 自动权重与最小实装验证

在物体模式选择网格，再选骨架使其活动：Object → Parent → Armature Deform → With Automatic Weights（`Ctrl+P`）。切 Pose Mode，逐一转头/腕、试腿脚与弯单指；把帽饰/头发脱离、鞋变形、串指逐项截图。先 Pose → Clear Transform → All 回到基准，再检查 VRM Humanoid 必填映射、左右、层级、元数据。

File → Export → VRM，另存标为 `rig-smoke` 的试版，在目标桌面软件加载并跑内置待机和代表动作。流程能跑通即进入权重修复，不必等所有视觉瑕疵消失。失败先查格式、版本、坐标、地图与材质依赖。非人形在工作开始前查运行时自定义骨架与 GLB 等格式支持，勿为了通过 Humanoid 盲填不存在的肢体。
