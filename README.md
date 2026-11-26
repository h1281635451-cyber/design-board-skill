# Design Board Prompts V2

完整 V2 现已发布，仓库入口由 Lite 升级为 `design-board-prompts-v2`。

## 本次更新

- 默认规划一张综合主展板，整合核心概念、主视觉、设计亮点与应用，供独立阅读和提交；分展板展开细节。
- 默认生成完整带字效果稿，标题、说明、图例均入画。确认整体效果后按需提供无字底图或素材。
- 用户或赛事固定总张数时，主展板计入总数，不额外超额。

## 安装与调用

下载仓库 ZIP 后，将解压文件夹命名为 `design-board-prompts-v2`，复制到你的 Skills 目录。已有 Lite 安装时可移走旧版，避免同时触发。

```sh
git clone https://github.com/h1281635451-cyber/design-board-skill.git design-board-prompts-v2
```

调用：`使用 $design-board-prompts-v2，为我的项目规划综合主展板与分展板，先输出完整带字效果稿提示词。`

完整流程见 [SKILL.md](SKILL.md)。赛事规则需核对当届官方来源，不承诺图像模型完全一致或中文零错误。历史 Lite 示例保留作参考；与当前入口冲突时以 V2 为准。

采用 [MIT License](LICENSE)。
