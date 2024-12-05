from pathlib import Path
import sys
import shutil


TARGETS = [
    ("x86_64-windows-msvc", "X86_64", "WINDOWS"),
    ("x86_64-linux-gnu", "X86_64", "LINUX"),
    ("aarch64-macos", "AARCH64", "MACOS"),
]


if __name__ == "__main__":
    name = sys.argv[1]
    
    for target, source_arch, source_os in TARGETS:
        src_dir = Path("packages", f"{name}-{target}")
        dst_dir = Path("packages", name)

        if (src_dir / "src").exists():
            shutil.copytree(src_dir / "src", dst_dir / "src", dirs_exist_ok=True)

        if (src_dir / "lib").exists():
            shutil.copytree(src_dir / "lib", dst_dir / "lib", dirs_exist_ok=True)
