# 制作 3D 桌宠

从一张角色原图或多视图开始，在 Tripo 或 Meshy 生成可绑定的网格，在 Blender 修整、绑定和导出，并在桌面软件里验收。也可从已有的图片、网格或 VRM 接着做。

| Skill | 用途 |
|---|---|
| [make-3d-desktop-pet](skills/make-3d-desktop-pet/SKILL.md) | 从参考图、网格或 VRM 起步；支持 Tripo/Meshy 官方接口和 Blender 后台操作，保留人工路径，覆盖绑定、物理、表情和桌面验收 |

## 安装与使用

在克隆后的仓库根目录执行（需要 [skit](https://github.com/vlln/skit)）：

```sh
skit install . --all
```

使用时可直接说「根据这张三视图制作可在我的桌面运行的 3D 桌宠」，也可指定一个环节，如「检查这组生成图有没有拉长身体，能不能拿去建模」或「排查这个 VRM 的头发穿模」。

本项目是 Agent Skill，不是桌宠播放器。只审图不需要 Blender 或云账号；修模和导出 VRM 使用 Blender 与 VRM 扩展；仅在需要云端生成时才配置 Tripo 或 Meshy。能否播放独立动作及触发弹簧和表情，以目标桌宠软件为准。

## 参考视频

小红书《3D 桌宠制作全流程》系列。

1. [从 0 到 1 做出你的专属桌宠](https://xhslink.cn/o/7QUZTP91N7N)
2. [Tripo 生成模型](https://xhslink.cn/o/9KlgNHm148k)
3. [模型和贴图处理](https://xhslink.cn/o/1p2Mk2n31BZ)
4. [VRM 骨骼搭建](https://xhslink.cn/o/1jUNQumCESG)
5. [权重修复](https://xhslink.cn/o/6mGpz6TYwlm)
6. [弹簧骨骼和碰撞体](https://xhslink.cn/o/1sPTuAnIlVx)
7. [表情制作](https://xhslink.cn/o/AltfpD8J5d8)
8. [桌宠软件](https://xhslink.cn/o/AF8ilwOOZic)

[八集复核记录](docs/tutorial-evidence/coverage.md)按原片时间整理操作、判断与适用边界。[开发与验证记录](SOURCES.md)列出官方接口来源和实测范围。公开仓库与安装包均不分发第三方关键帧、原声片段或转写。

## 许可

本项目自编文档和脚本按 [MIT](LICENSE) 授权。引用的视频与配套角色资产的权利归各自权利人。
