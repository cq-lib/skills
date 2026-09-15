# Cqlib Skills

[English](README.md) | [简体中文](README.zh-CN.md)

面向 Cqlib 量子计算生态的 AI Agent Skills。接口说明以对应仓库的源码为依据，
不假定 PyPI 上已发布相同版本。

## Skills 与源码仓库

| Skill | 语言接口 | 适用范围 | 上游仓库 |
|---|---|---|---|
| [cqlib](skills/cqlib/SKILL.md) | Python / Rust / C | 核心电路、参数；以及各语言实际暴露的模拟、编译、格式、设备和误差缓解能力 | [cq-lib/cqlib](https://github.com/cq-lib/cqlib) |
| [cqlib-tianyan](skills/cqlib-tianyan/SKILL.md) | Python / Rust / C | 认证、后端、QCIS 提交、轮询、校准及结果处理 | [cq-lib/cqlib-tianyan](https://github.com/cq-lib/cqlib-tianyan) |
| [cqlib-pulse](skills/cqlib-pulse/SKILL.md) | Python | 脉冲 QCIS、波形、通道时序及云端波形可视化 | [cq-lib/cqlib-pulse](https://github.com/cq-lib/cqlib-pulse) |
| [cqlib-qaoa](skills/cqlib-qaoa/SKILL.md) | Python | QUBO/Ising 映射、本地优化及天衍执行 | [cq-lib/cqlib-qaoa](https://github.com/cq-lib/cqlib-qaoa) |
| [cqlib-vqe](skills/cqlib-vqe/SKILL.md) | Python | 本地 VQE、化学预处理及天衍能量估计 | [cq-lib/cqlib-vqe](https://github.com/cq-lib/cqlib-vqe) |

原来的 `cqlib-python` 入口与 C/Rust 指南已统一到 `cqlib`：一个源码仓库对应一个
skill，再按语言加载参考资料。本次核对的核心库 C ABI 仅支持电路构建和参数操作，
并不具备 Python/Rust 的全部功能。Tianyan 的 **main** 分支提供三种语言接口；
其 Cargo 配置依赖核心库的 `develop` 分支，两者不是同一个分支选择。

每个 skill 都提供 GitHub 仓库及相关源码、测试目录的链接。指南不足以解决问题时，
AI 应先检查用户的本地源码，再查阅匹配 commit、tag 或分支的 GitHub 代码；不要假定
PyPI 包已包含这些接口，也不要静默切换版本。无法访问 GitHub 时，应明确说明限制。

## 安装 skills

推荐用 `npx skills` 选择目标 Agent 并安装；需要离线复制或指定任意目录时，使用
仓库自带的 Python 安装脚本。两种方式都只安装 skills，不安装 SDK。
同一个安装目录建议只使用一种方式管理，因为它们的更新和备份机制相互独立。

### 方式一：npx skills

需要 Node.js/npm；从远程 Git 仓库安装还需要 Git 和网络。
[Vercel Skills CLI](https://github.com/vercel-labs/skills#install-a-skill)
支持选择 skill、Agent，以及项目级或用户全局安装。在需要使用 skills 的项目目录中运行：

```shell
# 查看可用入口，不安装
npx skills add cq-lib/skills --full-depth --list

# 安装统一的核心库 skill，在交互提示中选择 Agent
npx skills add cq-lib/skills --full-depth --skill cqlib

# 安装五个库对应的 skills
npx skills add cq-lib/skills --full-depth \
  --skill cqlib cqlib-tianyan cqlib-pulse cqlib-qaoa cqlib-vqe
```

根目录 `SKILL.md` 是整套仓库的导航入口。CLI 默认发现根 skill 后就停止向下查找，
因此以上命令使用 `--full-depth`，并明确选择各库的名称。列表中还会出现
`cqlib-ecosystem`，不要将它与五个库的 skills 重复安装。从仓库根路径安装时，
避免使用 `--all` 或 `--skill '*'`。具体行为见
[发现逻辑源码](https://github.com/vercel-labs/skills/blob/main/src/skills.ts)。

默认安装范围是当前项目。例如，给 Codex 做用户全局安装：

```shell
npx skills add cq-lib/skills --full-depth \
  --skill cqlib cqlib-tianyan --agent codex --global
```

Claude Code 可以使用 `--agent claude-code`，也可以在交互界面选择 Agent。
`--copy` 表示复制文件而不是使用符号链接；继续安装前，请核对 CLI 提示的目标目录和
覆盖信息。这些参数属于 `npx skills`，不适用于本仓库的 Python 安装脚本。

GitHub 安装命令获取的是 `cq-lib/skills` 已发布的仓库内容，不包含本地未提交的修改。
如果当前改动还未推送，或者 `--list` 中仍然只有 `cqlib-python`，请先从本地安装。
在本仓库根目录运行：

```shell
npx skills add ./skills --list
npx skills add ./skills --skill cqlib cqlib-tianyan
```

直接指定 `./skills` 只会发现五个库的 skills，不需要 `--full-depth`。
若要安装到其他项目，在那个项目中运行命令，并将 `./skills` 替换为本仓库
`skills/` 目录的绝对路径。使用 fork 或未合并分支时，指定对应的 GitHub 仓库或
tree URL，不要假定上游已经包含这些改动。

### 方式二：仓库自带的 Python 安装脚本

需要 Python 3.10+，仅依赖标准库。脚本不下载包、不构建 SDK、不修改 Agent 配置，
也不提交云任务。从本仓库运行，或使用脚本的绝对路径。

将 `/path/to/agent/skills` 替换为目标 Agent 使用的 skills 目录。
必须明确提供目标目录，脚本不会默认选择全局安装。

```shell
python3 scripts/install_skills.py --list
python3 scripts/install_skills.py --target /path/to/agent/skills --dry-run
python3 scripts/install_skills.py --target /path/to/agent/skills
```

只安装部分 skills 时，重复指定 `--skill`：

```shell
python3 scripts/install_skills.py --target /path/to/agent/skills \
  --skill cqlib --skill cqlib-tianyan
```

脚本复制完整的 skill 目录，包括参考资料、示例和界面元数据。移动本仓库不会影响
已安装的副本；更新时需要重新运行脚本。默认拒绝覆盖已有目标，备份更新使用：

```shell
python3 scripts/install_skills.py --target /path/to/agent/skills \
  --skill cqlib --replace
```

旧安装保存在目标目录旁的 `skills-backups/` 中，按时间创建子目录；如果目标目录
不是名为 `skills`，备份目录名为 `<目标目录名>-backups/`。备份位于 skill 发现目录
之外，实际路径会打印出来。恢复时，先移开新安装，再把对应备份移回原路径。

对于已有的 `cqlib-python`、`cqlib-rust`、`cqlib-c` 安装，脚本只提示，不删除。
确认合并后的 `cqlib` 符合需要后，请将旧入口移出 Agent 的发现目录，避免重复加载。
其他 skills 不受影响。安装后按所用 Agent 的要求重新加载。

SDK 的源码构建方式见各语言指南；这个脚本**只安装 skills**。

## 根入口与调用方式

根目录 [SKILL.md](SKILL.md) 供直接读取仓库的 AI 使用，按库和语言选择所需指南，
不作为第六个 skill 与五个库一起安装。文件名使用规范的大写 `SKILL.md`。

对于支持 `$skill-name` 显式调用的 Agent：

```text
$cqlib 使用 Rust 绑定电路参数，并验证状态概率。
$cqlib 使用生成的头文件编写 C 示例，正确处理对象释放。
$cqlib-tianyan 编写 C 语言 QCIS 提交程序，但不要提交真实任务。
$cqlib-pulse 构建脉冲序列，在本地检查各通道时序。
$cqlib-qaoa 求解带权 MaxCut，验证目标函数符号和比特顺序。
$cqlib-vqe 运行不依赖化学预处理的最小本地 VQE 示例。
```

不支持 skill 自动发现的 Agent，可以读取根 `SKILL.md` 和完整仓库，或者直接接收
选定的 skill 目录。只上传入口文件会遗漏参考资料。直接调用模型 API 时，需要由调用方
将相关文件提供给模型；调用字符串本身不会让模型获得本地文件访问能力。

## 目录与示例

```text
SKILL.md                    仓库级导航入口
scripts/
  install_skills.py          按需安装、预览、备份更新
  validate_skills.py         链接、语法和可选的本地示例检查
tests/                      安装器和 Tianyan 模板的 mock 测试
skills/
  cqlib/                    Python / Rust / C 按需导航
  cqlib-tianyan/             Python / Rust / C 执行指南
  cqlib-pulse/
  cqlib-qaoa/
  cqlib-vqe/
```

每个独立 skill 包含 `SKILL.md`、`agents/openai.yaml`、按任务拆分的 `references/`，
以及 `assets/` 下的示例模板。使用时只加载与当前任务相关的参考资料。

可离线运行的示例：

- [核心 Rust](skills/cqlib/assets/rust/core_workflow.rs)：参数绑定、非对称状态的比特顺序、基门编译及 QCIS 往返转换。
- [核心 C](skills/cqlib/assets/c/circuit_parameters.c)：参数所有权、电路绑定及错误返回值。
- [脉冲时序](skills/cqlib-pulse/assets/pulse_timeline.py)：通道时钟、屏障及 QCIS 往返转换。
- [QAOA MaxCut](skills/cqlib-qaoa/assets/maxcut.py)：枚举验证目标函数、比特顺序及有限次数的本地优化。
- [最小 VQE](skills/cqlib-vqe/assets/minimal_vqe.py)：具有已知基态能量的单比特变分问题。

Tianyan 提供 [Python](skills/cqlib-tianyan/assets/submit_qcis.py)、
[Rust](skills/cqlib-tianyan/assets/submit_qcis.rs) 和
[C](skills/cqlib-tianyan/assets/submit_qcis.c) 提交模板。
使用有效参数和凭据运行这些模板会提交真实云任务。模板不嵌入密钥，也不会在轮询超时后
自动重新提交。执行前应确认后端、shots、校准模式和提交授权。

## 验证与维护

不依赖 SDK 的检查：

```shell
python3 scripts/validate_skills.py
python3 -m unittest discover -s tests -v
```

在已经安装源码版 Python SDK 及其依赖的环境中，可以运行预先限定的本地示例：

```shell
python3 scripts/validate_skills.py --offline-examples
```

该命令执行核心 Python 片段和 Pulse/QAOA/VQE 示例，不运行云任务提交模板。
C/Rust 示例需要按照对应语言指南，针对匹配的源码和头文件单独编译。
如果环境中有 `skill-creator`，还可以使用其 `quick_validate.py` 验证根入口和各 skill。

[tianyan_c_null.c](tests/tianyan_c_null.c) 针对实际 Tianyan C ABI 测试
NULL、错误和资源释放路径，不加载凭据或构造客户端。使用 Tianyan 生成的头文件及库
进行编译链接，再在本地运行；链接配置与 C 提交模板相同。

本次核对使用的本地源码版本：

| 仓库 | 核对的 commit |
|---|---|
| cqlib (main) | `1d0a2c4` |
| cqlib-tianyan (main) | `4bd2b79` |
| cqlib-pulse | `63bdd3e` |
| cqlib-qaoa | `c3c952d` |
| cqlib-vqe | `b173554` |

这些是核对基线，不是强制锁定的依赖版本。上游接口变化时，应同时检查公共导出、
类型存根或生成头文件、实现及相关测试。Rust 用户若要与 Tianyan 共享 `Circuit`，
必须确保依赖解析到同一来源、同一版本的核心 crate；仅包名和版本号相同并不够。

离线验证与真实云端联调应分别说明：mock 和编译不能证明后端可用、认证有效或硬件行为
正确。分子化学示例还需要额外的可选化学依赖。

修改安装命令、skill 名称、支持的接口或核对基线时，请同步维护中英文 README。
Skill 指令保留一套统一维护的内容，不因 README 翻译而复制出两套 skills。
