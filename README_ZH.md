# 数独小组作业：完成情况与使用说明

本目录是一份可运行、可检查的作业草稿。核心求解器、网页和五道概念题已完成。
提交前，请小组一起理解代码和文字回答，并补齐真实成员资料。

## 当前状态

Group 7、四位成员姓名及三位已提供的学号已写入 Notebook。CHOOG SHENG HONG 的学号及所有成员的实际贡献仍待确认；
不会把拟定任务写成已完成工作，也不会把未联系上的成员写成已完成测试。

本地使用独立 Jupyter 内核执行全部代码单元，真实输出保存在 Notebook；
详细验证范围见 `VALIDATION.md` 和 `validation_outputs` 中的机器可读记录。
公网应用已通过独立浏览器功能检查：https://daphnezhang627-cell-it5005-group7-sudoku-sudoku-app-lkd5pg.streamlit.app/

最终提交仍需要 CHOOG SHENG HONG 的学号和确认后的实际贡献；真实网页链接已写入 Notebook。
`Group7_DRAFT.zip` 仅供查看，不能直接提交；资料和部署验证齐全后才生成 `Group7.zip`。

## 文件用途

| 文件 | 用途 | 是否属于老师要求的三个提交文件 |
| --- | --- | --- |
| Sudoku_Assignment.ipynb | 实验代码、输出、五题分析、资料与部署链接 | 是 |
| sudoku_solver.py | 两种知识库、FC/BC求解、实际证明记录 | 是 |
| sudoku_app.py | 题目选择、棋盘、计时、单格查询、推理回放 | 是 |
| logic_.py、utils.py | 老师提供的辅助库，内容保持不变 | 否，运行和部署需要 |
| puzzles.json | 老师提供的五道题和用于核对的标准答案 | 否，运行和部署需要 |
| requirements.txt | 网页的Python依赖 | 否，部署需要 |
| requirements-notebook.txt | 执行Notebook所需的额外依赖 | 否，本地运行使用 |
| README_ZH.md、VALIDATION.md | 使用说明和验证记录 | 否 |

`logic_.py`、`utils.py` 和 `puzzles.json` 已与项目根目录中的老师文件逐字节比对，内容一致。

## 本地运行：建议Python 3.12

以下Windows命令在解压后的文件夹内，用命令提示符（CMD）执行。

```bat
py -3.12 -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements-notebook.txt
python -m streamlit run sudoku_app.py
```

打开终端给出的本地网址即可操作。停止网页时，在终端按 Ctrl+C。
如果电脑已有其他Python安装，需要确认当前选择的是Python 3.12的环境。

Linux/macOS的环境激活命令是：

```sh
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-notebook.txt
python -m streamlit run sudoku_app.py
```

要使用浏览器中的Jupyter Notebook界面，可在同一环境另行安装并启动：

```sh
python -m pip install notebook
python -m notebook
```

打开 `Sudoku_Assignment.ipynb`，从第一个代码单元开始顺序运行。
计时和全部候选值检查可能需要几分钟；前向推理通常明显慢于本版本的后向推理。
Notebook 的归结/模型检查实验每种方法最多运行约 30 秒。
已删去较长的 Windows 专用代码；用简短的 psutil 监测在驻留内存超过 768 MiB 时停止子进程。
这是采样监测阈值，并非操作系统的硬性内存上限。实验已重新执行，观察结果以当前输出为准。
不要把超时或资源错误当成逻辑查询的False结果。

## 网页怎么使用

1. 选择 Puzzle 1–5 中的一道题。
2. 选择 Backward chaining 或 Forward chaining，按 Solve puzzle。
3. 灰底粗体是题目给定的数字，青色是推导出的数字。
4. 输入 Row / Column / Value，按 Check and explain。
5. 下方用 Proof step 滑块回放实际的证明过程，展开 Supporting facts 查看依据。
6. 如果一个候选数字不能成立，网页会尝试显示排除它的证明。
   单纯“没有证明”不等于已经证明它的否定，界面区分了这两种情况。

## 部署步骤（依据老师提供的部署指南）

1. 准备你们小组的GitHub账号/仓库。
2. 将 `sudoku_app.py`、`sudoku_solver.py`、`logic_.py`、`utils.py`、
   `puzzles.json`、`requirements.txt` 放在仓库根目录。
   **网页部署不需要公开包含姓名学号的Notebook。**
3. 前往 https://share.streamlit.io ，通过GitHub登录。
4. 创建应用，选择仓库、分支和入口 `sudoku_app.py`。
5. 使用Python 3.12运行环境；依赖版本见 `requirements.txt`。
6. 部署完成后，打开真实网址验证按钮，再复制网址到Notebook最后。

具体页面按钮可能会更新，以平台实际显示为准。本次公共部署已完成，并经过独立浏览器检查。

## 实现说明：小组答辩时需要理解

- 一般知识库直接编码每格恰好一个数字和同行、同列、同宫排他约束。
- Horn知识库使用显式的 Is / Not 原子，以及“排除”和“最后候选”规则。
- `Not1_2_3` 是一个正命题符号，表达“(1,2)不能填3”，不是Python的 `not`。
- 前向推理调用老师的 `pl_fc_entails`；为了避免反复扫描所有规则，在学生文件中
  用 `PropDefiniteKB` 的子类增加了前提索引，老师的库没有改动。
- 后向推理自己实现，按目标查规则、递归证明前提；用表保存待处理目标和已证明事实。
  循环本身不能当作证据，只有得到事实支持的规则才会产生新结论。
- 递归到64层时把后续目标暂存并稍后继续，避免Python调用栈过深。
- 同一次整盘BC求解会复用已经证明的前提；老师的FC函数每次候选查询重新建立计数器。
  因此计时比较体现了这两个具体实现，不能泛化成“BC一定比FC快”。
- 两种求解器都只读givens。标准答案仅由Notebook测试使用。
- 这套规则不保证解决任意数独；若推理不足，会说明无法确定某格，不猜测、不抄答案。
- Naked Pairs 是第四题的规则编码示例，未悄悄加入主求解器改变实验基线。

## 本次执行方式

使用父目录的独立 `.venv`，通过 nbclient 启动新的 Python 3.12 Jupyter 内核，
在本项目目录顺序执行 Notebook。`tests/run_notebook.py` 可重复这一过程。
`tests/test_inference.py` 覆盖 BC 循环、缓存、随机 Horn KB 对照和真实证明依赖；
`tests/test_app.py` 使用 Streamlit AppTest 检查按钮及会话状态；
`tests/test_browser.cjs` 对本机实际网页执行 Edge 浏览器检查并保存截图。
另已运行 tests/test_public.cjs 验证真实公共部署，记录见 validation_outputs/public_deployment.json。
