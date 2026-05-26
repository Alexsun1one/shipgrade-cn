#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=False)


def ensure_safe_target(path: Path) -> None:
    temp_root = Path(tempfile.gettempdir()).resolve()
    resolved = path.resolve()
    if temp_root not in resolved.parents and resolved != temp_root:
        raise SystemExit(f"refuse to clean non-temp demo target: {resolved}")
    if not resolved.name.startswith("shipgrade-demo"):
        raise SystemExit(f"refuse to clean non-demo target: {resolved}")


def write_fake_completion(path: Path) -> None:
    path.write_text(
        "# Fake Completion\n\n"
        "## 已完成\n结果: 看起来好了。\n\n"
        "## 验证证据\n验证: 应该通过。\n\n"
        "## 来源和许可证\n来源: 当前项目。许可证: 未引入外部代码。\n\n"
        "## 风险边界\n风险: 可能还有问题。\n\n"
        "## 禁止事项\n不要复制 secret token cookie session。\n\n"
        "## 接手入口\n下一步: TODO。\n",
        encoding="utf-8",
    )


def write_good_handoff(path: Path, project: Path) -> None:
    task = project / ".shipgrade" / "task-brief.md"
    agents = project / "AGENTS.md"
    claude = project / "CLAUDE.md"
    cursor = project / ".cursor" / "rules" / "shipgrade.mdc"
    path.write_text(
        "# ShipGrade Demo Handoff\n\n"
        "## 已完成\n"
        f"交付: 已生成 `{task}`、`{agents}`、`{claude}`、`{cursor}` 四个可打开入口。\n\n"
        "## 验证证据\n"
        f"- `python3 tools/shipgrade_init.py {project}` 成功, exit: `0`。\n"
        f"- `python3 tools/shipgrade_doctor.py {path}` 成功, exit: `0`。\n\n"
        "## 来源和许可证\n"
        "来源: ShipGrade CN 本仓库自带模板。许可证: 未引入外部正文或第三方代码。\n\n"
        "## 风险边界\n"
        "已知限制: demo 只证明初始化、接线和 doctor 验收链路,不声称远程 GitHub Actions 已运行。\n\n"
        "## 禁止事项\n"
        "禁止复制 secret token cookie session auth private key 或浏览器资料进入产物。\n\n"
        "## 接手入口\n"
        f"接手: 打开 `{project / '.shipgrade' / 'handoff.md'}` 继续填真实项目上下文。\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the 30-second ShipGrade CN demo.")
    parser.add_argument("--target", default=str(Path(tempfile.gettempdir()) / "shipgrade-demo-project"), help="demo project directory under the system temp folder")
    parser.add_argument("--clean", action="store_true", help="remove the generated demo project after printing proof")
    args = parser.parse_args()

    target = Path(args.target).expanduser()
    ensure_safe_target(target)
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)

    init = run([sys.executable, "tools/shipgrade_init.py", str(target)])
    if init.returncode != 0:
        raise SystemExit(init.stdout + init.stderr)

    fake = target / "fake-completion.md"
    write_fake_completion(fake)
    fake_check = run([sys.executable, "tools/shipgrade_doctor.py", str(fake)])
    if fake_check.returncode == 0:
        raise SystemExit("demo failed: doctor accepted fake completion\n" + fake_check.stdout)

    handoff = target / "accepted-handoff.md"
    write_good_handoff(handoff, target)
    good_check = run([sys.executable, "tools/shipgrade_doctor.py", str(handoff)])
    if good_check.returncode != 0:
        raise SystemExit(good_check.stdout + good_check.stderr)

    expected_files = [
        ".shipgrade/task-brief.md",
        ".shipgrade/quality-gate.md",
        ".shipgrade/handoff.md",
        "AGENTS.md",
        "CLAUDE.md",
        ".cursor/rules/shipgrade.mdc",
        "fake-completion.md",
        "accepted-handoff.md",
    ]
    missing = [rel for rel in expected_files if not (target / rel).exists()]
    if missing:
        raise SystemExit("demo failed: missing " + ", ".join(missing))

    print("shipgrade-demo-ok")
    print(f"target={target}")
    print("created=" + ",".join(expected_files))
    print("fake_rejection=" + fake_check.stdout.strip().splitlines()[-1])
    print("accepted=" + good_check.stdout.strip().splitlines()[-1])
    print("next=open " + str(target / ".shipgrade" / "task-brief.md"))
    if args.clean:
        shutil.rmtree(target)
        print("cleaned=true")
    else:
        print("note=demo project kept for inspection; rerun overwrites only this temp demo directory")


if __name__ == "__main__":
    main()
