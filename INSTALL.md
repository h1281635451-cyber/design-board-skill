# 新手安装与使用教程 / Beginner Installation

## 方法一：下载 ZIP（最适合新手）

1. 打开 [Design Board Skill GitHub 仓库](https://github.com/h1281635451-cyber/design-board-skill)，点击 **Code → Download ZIP**。
2. 解压下载文件。
3. 将解压后的仓库文件夹重命名为 `design-board-prompts-v2`。
4. 把整个文件夹复制到 Codex Skills 目录。
5. 重新启动 Codex，或刷新可用 Skills。
6. 输入以下内容测试：

```text
使用 $design-board-prompts-v2，帮我判断一个设计项目处于什么阶段。
```

必须复制整个文件夹，不能只复制 `SKILL.md`；`references/` 是运行依赖。

## 方法二：Git 克隆

在 Skills 目录的上一级运行：

```powershell
git clone https://github.com/h1281635451-cyber/design-board-skill.git design-board-prompts-v2
```

上述命令会将仓库克隆到名为 `design-board-prompts-v2` 的本地目录，使目录名与 Skill 名称保持一致。

## 常见 Skills 目录

实际位置以你的 Codex 配置为准。常见个人目录为：

```text
Windows: %USERPROFILE%\.codex\skills\design-board-prompts-v2
macOS/Linux: ~/.codex/skills/design-board-prompts-v2
```

如果使用自定义 `CODEX_HOME`，请安装到该目录下的 `skills/design-board-prompts-v2`。

## 首次使用

推荐输入完整上下文：

```text
使用 $design-board-prompts-v2。
我是本科生，项目是一个面向夜间骑行的智能尾灯，目前有草图和外观模型，没有用户测试，想参加国内设计比赛。请用深入模式，每轮只问一个关键问题。
```

快速出稿：

```text
使用 $design-board-prompts-v2，快速模式。根据现有信息规划 2 张展板；未知内容用“待补”标记，不要生成虚构数据。
```

## 更新

ZIP 安装：下载新版本，先备份你自己修改过的文件，再用新版本完整替换 Skill 文件夹。

Git 安装：确认没有未保存的本地修改后，在仓库目录运行：

```powershell
git pull --ff-only
```

项目自己的 `project-brief.md` 应放在项目目录，不要放入 Skill 文件夹，以免更新时被覆盖。

## 故障排查

### Skill 没有出现

- 确认文件夹名是 `design-board-prompts-v2`；
- 确认目录根部直接包含 `SKILL.md`，没有多套一层文件夹；
- 重新启动或刷新 Codex；
- 运行 `python scripts/validate_lite.py` 检查完整性。

### 提示缺少引用文件

你可能只复制了 `SKILL.md`。重新复制完整仓库，确保 `references/` 和 `examples/` 存在。

### 赛事规则与官网不同

以当届官方通知和报名系统为准。Lite 只做基础识别；将官方文件交给 Codex，并要求按明确年份更新当前项目判断。

### 图像文字或结构出错

改用“素材生成 + Figma/PPT/Illustrator 排版”路径。长中文、数据图表和尺寸线不应完全交给图像模型。

## 卸载

关闭 Codex 后，删除 `design-board-prompts-v2` Skill 文件夹，再重新启动 Codex。删除 Skill 不会自动删除你保存在其他项目目录的项目简报或生成文件。

## English quick install

Download or clone [the GitHub repository](https://github.com/h1281635451-cyber/design-board-skill), rename the folder to `design-board-prompts-v2`, and place the complete folder in your Codex Skills directory. For Git, run `git clone https://github.com/h1281635451-cyber/design-board-skill.git design-board-prompts-v2`. Restart or refresh Codex, then invoke `$design-board-prompts-v2`. Keep `references/` beside `SKILL.md`; the Skill is not a single-file installation.
