#!/usr/bin/env python3
"""Validate the midterm's public chapter hierarchy and compiled contents."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = {
    "01-purpose": [
        ("chapter", "研究目的及意义"),
        ("section", "研究背景与目标"),
        ("section", "研究目的"),
        ("section", "研究意义"),
        ("subsection", "理论意义"),
        ("subsection", "实践意义"),
    ],
    "02-route": [
        ("chapter", "技术路线"),
        ("section", "总体研究思路"),
        ("section", "主要技术环节"),
        ("subsection", "数据收集与预处理"),
        ("subsection", "研究方法的实施"),
        ("subsection", "结果验证与评价"),
        ("section", "技术路线图"),
    ],
    "03-progress": [
        ("chapter", "论文进展情况说明"),
        ("section", "已完成的研究任务"),
        ("section", "研究进度与原计划对照"),
        ("section", "阶段性研究与验证工作"),
        ("subsection", "已开展的实验或分析"),
        ("subsection", "主要结果及其分析"),
    ],
    "04-achievements": [
        ("chapter", "已取得的阶段性成果"),
        ("section", "阶段性研究成果"),
        ("section", "学术论文及其他成果"),
        ("section", "成果证明材料"),
    ],
    "05-challenges": [
        ("chapter", "目前存在的问题和困难"),
        ("section", "当前存在的问题"),
        ("section", "研究面临的困难"),
        ("section", "原因分析及对研究进度的影响"),
    ],
    "06-plan": [
        ("chapter", "下阶段研究计划及主要措施"),
        ("section", "下一阶段研究任务"),
        ("section", "主要实施措施"),
        ("section", "进度安排与预期成果"),
    ],
}
HEADING_RE = re.compile(r"^\s*\\(chapter|section|subsection)\{([^{}]+)\}", re.MULTILINE)
INCLUDE_RE = re.compile(r"\\include\{contents/([^{}]+)\}")


def check(root: Path, toc: Path | None = None) -> None:
    main = (root / "main.tex").read_text(encoding="utf-8")
    expected_names = list(STRUCTURE)
    included = INCLUDE_RE.findall(main)
    if included != expected_names:
        raise ValueError(f"Chapter inclusion order mismatch: {included!r}")

    actual_files = sorted(p.stem for p in (root / "contents").glob("*.tex"))
    if actual_files != sorted(expected_names):
        raise ValueError(f"Unexpected chapter files: {actual_files!r}")

    for filename, headings in STRUCTURE.items():
        data = (root / "contents" / f"{filename}.tex").read_text(encoding="utf-8")
        actual = HEADING_RE.findall(data)
        if actual != headings:
            raise ValueError(f"{filename}: expected {headings!r}, got {actual!r}")

    if r"\bibmatter*" not in main or r"\printbibliography" not in main:
        raise ValueError("Missing the bibliography section")

    if toc is not None:
        toc_lines = toc.read_text(encoding="utf-8").splitlines()
        position = -1
        for headings in STRUCTURE.values():
            for level, heading in headings:
                prefix = f"\\contentsline {{{level}}}"
                candidates = [
                    i for i, line in enumerate(toc_lines)
                    if i > position and line.startswith(prefix) and heading in line
                ]
                if not candidates:
                    raise ValueError(f"Table of contents is missing {level}: {heading}")
                position = candidates[0]
        if not any(
            line.startswith(r"\contentsline {chapter}") and "参考文献" in line
            for line in toc_lines[position + 1:]
        ):
            raise ValueError("Table of contents is missing the bibliography")

    print("PASS: six chapters, complete subsection hierarchy, bibliography")


if __name__ == "__main__":
    try:
        if len(sys.argv) == 1:
            check(ROOT)
        elif len(sys.argv) == 3:
            check(Path(sys.argv[1]), Path(sys.argv[2]))
        else:
            raise ValueError("Usage: check-structure.py [project-root main.toc]")
    except (OSError, ValueError) as error:
        raise SystemExit(str(error)) from error
