# Agent 如何操作 Blender

## 默认：后台 Blender + bpy；工作副本与视觉反馈

先找可执行文件 `blender --version`；macOS 上若未加入 PATH，定位已安装 app 的 `Contents/MacOS/` 可执行文件；Windows 用安装目录中的 `blender.exe`。以实际版本查 [CLI 参数](https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html)、[Python API](https://docs.blender.org/api/current/)、[Operators 与上下文](https://docs.blender.org/api/current/info_gotchas_operators.html)、[BMesh](https://docs.blender.org/api/current/bmesh.html)。`bpy` 运行在 Blender 自带的 Python 里，默认不要用系统 Python 安装另一套 Blender。

先对输入运行随技能安装的只读脚本。`$_S` 替换为实际技能目录，`$BLENDER` 为已经找到的 Blender 可执行文件：

```sh
"$BLENDER" -b --disable-autoexec --python-exit-code 1 \
  --python "$_S/scripts/inspect_blender.py" -- input.blend out/before.json --vrm
```

输入还支持 `.fbx`、`.glb`、`.gltf` 与 `.vrm`。`.vrm` 自动启用已安装扩展；普通未绑定网格不需要 `--vrm`。报告输出原始网格顶点、多边形及三角面、UV、材质、形态键、Armature Modifier、权重粗检、场景单位和贴图引用，不尝试修复，不保存场景；已有 JSON 不会覆盖。报告不统计修改器后的最终面数，也不能凭“无零权重”断言没有串权，骨父接的刚性饰件可以没有蒙皮。

编辑另写阶段性脚本，先读输入，只把结果另存到新路径：

```sh
"$BLENDER" -b --disable-autoexec input.blend --python-exit-code 1 \
  --python stage.py -- --out out/next.blend
```

- 优先用数据 API 改可精确描述的对象、网格、UV、骨和顶点组；用名称加类型、绑定关系与地标确认对象。需 `bpy.ops` 时显式设活动对象/选择、视图层与模式；检查 `poll()` 和返回值 `{'FINISHED'}`。后台没有交互视口，绘制类/吸附类操作不能靠模拟按键或凭空构造 `VIEW_3D`。别在已有 Shape Keys 的原网格上运行拓扑清理。
- 用 `matrix_world` / 逆矩阵在对象、骨骼和世界空间转换，把头身比、碰撞半径、骨点单位说清楚。脚本同时记录改动的对象/区域及数量；先前后同机位正、侧、背、斜视和细节图，再用代表姿势检查。姿态网格用 `evaluated_get(depsgraph)` 检查，不要用静态基础顶点冒充已变形结果。灯光与相机只在临时场景或副本里改。
- 对视觉上难以确定的边界，先做候选面/骨位置的高亮截图，不能可靠定位时切到交互界面确认。无需为此安装 MCP：可打开同一工作副本，使用 Scripting → Python Console/Text Editor；Info 编辑器或右键 Copy Python Command（若提供）可找 operator，先核查入参。只有宿主已授权且能隔离本地连接，才考虑用现成 Blender MCP 看交互视口；不把桥接当后台依赖。人工接手时交付副本、确切菜单、目标对象和待改/待验的角度，拿回新文件后重跑对照。

## 关键动作对照

| 环节 | 脚本入口及验收 | 人工路径 |
|---|---|---|
| 导入与报告 | `bpy.ops.import_scene.gltf` / `.fbx`；对照 `.dimensions`、`mesh.polygons`、`calc_loop_triangles()`、UV、贴图与基线 | 文件 → 导入；视图 → 视角；Statistics / Wireframe |
| 网格与 UV | 局部 `bmesh.ops.remove_doubles` 或 `holes_fill`，只传审核的顶点/边，重算法线并比前后面数；用每个 polygon 的 loop 更新新面的 UV，不覆盖邻区 | 网格编辑模式 → Mesh → Clean Up → Merge by Distance；边界补面与 UV Editor，详见 `$_S/references/blender.md` |
| 修贴图 | 查实际 Base Color 源图和 UV；复制图后按像素区/UV 岛遮罩修改，检查共享材质、色彩空间、PNG 和整体颜色。读取节点/赋纹理用数据 API；别在后台调用依赖鼠标的笔刷 | Texture Paint / UV Editor 手动取样、克隆、涂抹；另存并打包 |
| 拟合与绑定 | 骨点先来自经核对的正侧视地标，再转换到 Armature 局部；Edit Mode 调 `arm.data.edit_bones`，绑定新网格时 `bpy.ops.object.parent_set(type='ARMATURE_AUTO')`，活动对象为骨架；现有绑定优先 `vertex_groups[...]` 仅修改许可范围 | VRM Humanoid 骨架 → 编辑模式拟合 → 物体模式先网格后骨架 → Object → Parent → Armature Deform → With Automatic Weights |
| 局部权重 | 显式选择顶点 ID；`VertexGroup.add(..., 'REPLACE')` / `.remove(...)`，仅归一化受影响的变形骨组，锁定的组不动；核对选区外无变化，姿态后再存 | Weight Paint → 面/顶点遮罩、Draw/Smooth、Weights → Normalize；刚性附件可在 Vertex Groups 精确 Assign/Remove |
| 弹簧与眨眼 | 见下节 RNA 路径；导出后对照扩展数据，同时在运行时用相同动作和时间步试摆动、眨眼 | VRM 面板 → Spring Bone / Expressions；定位与逐步验证见 `$_S/references/rig-and-expressions.md` |

## VRM 扩展：发现接口、选择对象、验证导出

从 [安装指南](https://vrm-addon-for-blender.info/en-us/installation/)、[脚本示例](https://vrm-addon-for-blender.info/en-us/scripting-api/)、[导出 UI](https://vrm-addon-for-blender.info/en-us/ui/export_scene.vrm/) 查。后台与图形进程的扩展状态可不同。通过 `addon_utils.modules()` 发现当前安装的实际模块名（旧版 `io_scene_vrm` 或 `bl_ext.<repo>.vrm`），只在该进程 `bpy.ops.preferences.addon_enable(module=name)`，不要保存用户偏好；确认 `hasattr(bpy.types.Armature, 'vrm_addon_extension')` 及 `bpy.ops.export_scene.vrm.get_rna_type()`。不要假定 `--factory-startup` 会加载扩展。扩展找不到或装了多个版本时，由操作者在 Edit → Preferences → Get Extensions/Add-ons 核对，明确用哪个再继续。

- **人形映射和元信息**：`ext = arm.data.vrm_addon_extension`; VRM 1.0 查 `ext.vrm1.humanoid.human_bones`，如 `hips.node.bone_name` 赋真实骨名。核对必需骨、不同槽不重复占用和层级。`ext.vrm1.meta` 写用户确认的名称、缩略图和许可，不能以放宽许可掩盖导出警告。
- **Spring Bone**：从 `ext.spring_bone1` 读取/编辑 `colliders`、`collider_groups`、`springs`，用扩展对应添加操作创建 collider（不要只造一个空物体），依次关联父骨、局部偏移和半径、collider UUID、group UUID、joints 骨名及参数。示例入口 `bpy.ops.vrm.add_spring_bone1_collider(armature_object_name=arm.name)`；从当前扩展的 `bl_rna.properties` / `get_rna_type()` 和 [Spring Bone 源码](https://github.com/saturday06/VRM-Addon-for-Blender/tree/main/src/io_scene_vrm/editor/spring_bone1) 确认版本差异。扩展面板预览不等于导出或宿主模拟。
- **Blink**：`obj.shape_key_add()` 后编辑指定 key block，VRM 1.0 中在 `ext.vrm1.expressions.preset.blink` 的 `morph_target_binds` 指定实际网格对象、Shape Key 名和权重。确认绑定引用不是旧网格副本。可查[表达式属性源码](https://github.com/saturday06/VRM-Addon-for-Blender/blob/main/src/io_scene_vrm/editor/vrm1/property_group.py)；二值切换仅在视觉需要且宿主确认支持时开启。
- **MToon**：`material.vrm_addon_extension.mtoon1` 保留原基色/纹理引用，再改遮光与描边属性；不要因为节点截图正确就断言 VRM 导出保留了设置。以扩展脚本示例和目标灯光核对。
- **导出**：显式识别唯一目标骨架和网格，清除临时姿态。调用 `bpy.ops.export_scene.vrm(filepath=...)`；若版本支持，传 `armature_object_name=arm.name`，限制导出范围并复查。断言返回值与文件，然后在新进程重导入并复查。可检查 VRM/GLB JSON 的 `extensions.VRMC_vrm`（Humanoid/Expressions）、`extensions.VRMC_springBone`（joint/碰撞引用）、`materials[].extensions.VRMC_materials_mtoon`；不要用“扩展名字存在”代替内容检查。VRM 0.x 用对应版本字段。若要导出 VRMA，按[扩展动画文档](https://vrm-addon-for-blender.info/en-us/animation/)检查 `bpy.ops.export_scene.vrma` 及宿主支持；普通 glTF 动画不等同 VRMA。
