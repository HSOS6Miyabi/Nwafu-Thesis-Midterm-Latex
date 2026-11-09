# 西北农林科技大学硕士／博士研究生进展报告 LaTeX 模板

适用于西北农林科技大学硕士、博士研究生学位论文中期考核的进展报告。模板继承[开题报告 LaTeX 模板](https://github.com/HSOS6Miyabi/Nwafu-Thesis-Proposal-Latex)的封面尺寸、字号、字段布局、目录、正文和参考文献排版，使用 [nwafuthesis](https://ctan.org/pkg/nwafuthesis) 文档类。

封面标题为**进展报告**，考核小组签名及日期字段采用**中期考核**表述。学位类型根据 `type=master` 或 `type=doctor` 自动显示；页眉分别显示**西北农林科技大学硕士进展报告**或**西北农林科技大学博士进展报告**。

## 使用方法

1. 安装 XeLaTeX、latexmk、Biber、nwafuthesis 和所需字体。建议使用 TeX Live 2026，文档类使用 v2.17 或更新版本。
2. 在 `main.tex` 中选择 `type=master` 或 `type=doctor`，以及 `oneside` 或 `twoside`。
3. 将 `cover/information.example.tex` 复制为 `cover/information-private.tex`，在本地填写年级、论文中英文标题、学院、专业、研究生姓名与学号、指导教师、考核小组人员和日期。私人信息文件已由 `.gitignore` 排除。
4. 依次编辑 `contents/` 下六个章节文件。参考文献保存在 `bib/references.bib`。
5. 在仓库根目录运行 `latexmk -xelatex main.tex`，生成 `main.pdf`。更复杂的 TikZ 绘图可使用 `bash scripts/build-fast.sh` 进行缓存编译。

## 正文章节

| 章节 | 文件 | 示例内容 |
| --- | --- | --- |
| 一、研究目的及意义 | `contents/01-purpose.tex` | 研究背景与目标、研究目的、理论意义与实践意义 |
| 二、技术路线 | `contents/02-route.tex` | 总体研究思路、技术环节、技术路线图 |
| 三、论文进展情况说明 | `contents/03-progress.tex` | 已完成的研究任务、计划对照、阶段性验证 |
| 四、已取得的阶段性成果 | `contents/04-achievements.tex` | 阶段性研究结果、论文及其他成果、证明材料 |
| 五、目前存在的问题和困难 | `contents/05-challenges.tex` | 未解决的问题、实际困难、原因及影响 |
| 六、下阶段研究计划及主要措施 | `contents/06-plan.tex` | 后续任务、实施措施、进度安排与预期成果 |

六章之后按原模板格式排版参考文献。示例正文均为通用说明，请根据实际研究工作填写。图表、公式、交叉引用、双语题注和文献引用等排版方法参见 [examples/README.md](examples/README.md)。

## 版式及编译检查

- **单面模式**：第 1 页为封面，第 2 页为目录；其后为正文。
- **双面模式**：第 1 页为封面，第 2 页为空白页，第 3 页为目录；新章节按照文档类规则分页。
- **封面标题**：中英文论文标题均使用 22 pt 字号、1.5 倍行距，标题组之间保留 9.5 mm 间距。当英文标题过长时，自动适当缩小英文标题内部行距。
- **字体选择**：自动优先使用可用的 Times New Roman、SimSun 和 SimHei 字体，缺失时回退到 XITS、FandolSong 和 FandolHei；数学字体为 XITS Math。
- **页眉**：自动随硕士／博士类型及单双面设置切换，目录与正文一致。

运行以下命令执行本地检查：

```bash
bash scripts/test-gitignore.sh
python3 scripts/check-structure.py
python3 scripts/check-references.py .
bash scripts/test-cache-latexmk.sh
bash scripts/test-build.sh
bash scripts/test-frontmatter-header.sh
bash scripts/test-running-header.sh
bash scripts/test-cover-extended.sh
bash scripts/test-examples.sh
```

GitHub Actions 的 [LaTeX CI](.github/workflows/latex-ci.yml) 自动编译硕士单面、硕士双面、博士双面及独立排版用例，检查封面、页眉、目录、章节结构、字体和交叉引用，并提供 4 份 PDF 构建产物。测试只使用公开的占位个人信息，不会读取 `cover/information-private.tex`。

编译产生的中间文件、日志、PDF 和缓存目录已由 `.gitignore` 排除。图表素材 PDF 可放入 `figures/` 或 `assets/` 中，以便正常纳入版本管理。

## 许可及说明

模板中新编写的内容采用 [MIT License](LICENSE)；外部文档类及第三方字体遵循各自许可。本仓库是非官方模板，最终报告格式请以学校当期要求为准。
