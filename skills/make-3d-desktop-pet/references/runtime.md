# 卡通材质与桌面实装

## 先用目标显示条件调 MToon

人工：Material Properties → VRM MToon，保留 Base Color 的已批准贴图。关 Overlays、固定灯光，调 Shading → Shade Color / Shading Toony / Shading Shift，分别检查暗部色、明暗边界软硬、亮暗分界位置。Toony 0.9 可作较硬的对比起点，非通用最佳值。默认无描边；需描边时用 Outline Width Mode → World Coordinates 或宿主支持的模式，逐渐增加细线并选匹配角色色调的颜色。`Shift` 可细拖数值；右键 Reset to Default Value 可恢复单项。实际显示尺寸看眼睛和服装细节，线不能吃掉眼、手指与细饰。Agent 路径见 `$_S/references/blender-agent.md`。

## 运行时接入：先预览，后部署

- 用目标 OS、实际版本和宿主文档确认 VRM 0.x / 1.0、Humanoid、Expressions、Spring Bone、MToon 和独立动作支持。未知宿主时先询问目标，别把 VRMA 当所有桌宠软件的通用格式。
- **Agent**：寻找宿主已有的测试预览、导入命令或公开 API；用同版本的已知可用 VRM 做阳性对照，独立 VRMA 也用已知可用动作测通。若只有 GUI，打开授权的独立/测试配置或给操作者精确步骤，获取截图或录屏、加载日志和同一组事件结果。不要覆盖当前用户模型、活动配置或真实部署；模拟预览不是桌面运行测试。
- **Mate Engine 人工路径**：Windows 的[发布页](https://github.com/shinyflvre/Mate-Engine/releases)／[Wiki](https://github.com/shinyflvre/Mate-Engine/wiki)。左键拖桌宠；右键打开轮盘 → Settings → Model → Import（部分版本标为 VRM / ME）→ 选择 `.vrm` → 从列表切换到新模型。名称、作者、缩略图取自 VRM Meta；测试版保留可辨认名称。移除测试项需确认当前版本操作，若 Delete 是长按确认，核对所选项后再操作，不在验证前移除可用基线。按界面退出后重开验收。Settings → Appearance → Character Size；Window Behavior 中查看 Start on Boot、Always on Top、Sit on Window and Taskbar 及 Sitting Height Offset；Dance → 齿轮 → 选检测到的应用 → Add。轮盘的月亮是 Ambient Light，和 AO 是独立设置。菜单标签按版本核对。

## 验收矩阵

| 测试项 | 验收 |
|---|---|
| 首次加载、切换与重启 | 显示正确角色、贴图、朝向、脚底和缩略图，重启后能再次加载。失败先用已知可用模型区分安装和资产问题。 |
| 宿主诊断 | 单独记录 VRM 版本、面数与骨骼状态（如 `Bones: Failure`）。能加载和播放待机也不代表骨骼诊断通过；有警告时与同版本已知良品比较并保留原始状态。 |
| 待机与代表动作 | 同机位录待机循环与代表动作；头、鞋、衣物和手指跟随，不明显脱离或跳帧；宿主自带动作和独立动作分开记。 |
| 弹簧骨与表情 | 拖动、快速停下、转身后发尾自然收敛，无明显穿臂。眨眼随头并能恢复睁眼；表情和摆动分别记录，不从导出成功推断。 |
| 实际大小、环境光 | 小尺寸眼睛及标志清晰。对比环境光遮蔽、场景灯、氛围光；先固定照明辨别材质问题，后决定是否开特效闪光。 |
| 窗口与性能 | 拖拽、置窗、缩放、隐藏重开和窗口行为符合需求，测动作运行 FPS 后再定帧率上限。开机启动、音量和其它持久设置须按用户需求调整。 |
| 音乐与附加行为（可选） | Dance 的应用列表中加入实际使用的播放器/浏览器；真实播放、暂停和停止分别测触发与恢复。有声音但不跳先查白名单，不改模型。外观模式及夜间配色按需预览。 |

交付阶段 `.blend`、贴图、版本化 `.vrm` 与实际需要的动作，附导入方法和验收记录。每项记 `通过 / 失败 / 待测`，注明材料版本、宿主、OS、窗口尺寸、动作和证据。正式部署经授权后再改目标配置，并保留可切回的基线。
