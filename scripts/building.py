from pathlib import Path
import subprocess
import shutil
import os
import platform


def git_clone(name, url):
    path = Path(name, f"{name}-upstream")

    if not path.is_dir():
        subprocess.run(["git", "clone", url, str(path)])


def host_target():
    target_arch = None
    target_os = None
    target_env = None

    machine = platform.machine().lower()
    if machine in ("x86_64", "amd64"):
        target_arch = "x86_64"
    elif machine in ("aarch64", "arm64"):
        target_arch = "aarch64"

    system = platform.system().lower()
    if system == "windows":
        target_os = "windows"
        target_env = "msvc"
    elif system == "linux":
        target_os = "linux"
        target_env = "gnu"
    elif system == "darwin":
        target_os = "macos"

    return (target_arch, target_os, target_env)


def cmake_build(name, args=[], libraries=[], target=host_target()):
    target_arch, target_os, target_env = target

    target_string = f"{target_arch}-{target_os}"
    if target_env:
        target_string += f"-{target_env}"

    path = Path(name, f"{name}-upstream")
    build_path = Path(path, "build", target_string)
    install_path = Path(path, "install", target_string)

    subprocess.run([
        "cmake", str(path),
        f"-B{build_path}",
        f"-GNinja",
        f"-DCMAKE_INSTALL_PREFIX={install_path}"
    ])

    subprocess.run([
        "cmake",
        "--build", str(build_path),
        "--target", "install",
    ])

    package_lib_path = Path(os.pardir, "packages", name, "lib", target_string)
    package_lib_path.mkdir(parents=True, exist_ok=True) 

    for library in libraries:
        file_name = f"{library}.lib" if target_os == "windows" else f"lib{library}.a"
        shutil.copy(install_path / "lib" / file_name, package_lib_path / file_name)


def generate_bindings(name, mod_name, include_dir):
    c_api_path = Path(name, f"{name}_api.c")
    generator_path = Path(name, f"{name}_generator.py")
    include_path = Path(name, f"{name}-upstream", include_dir)

    subprocess.run([
        "banjo", "bindgen", c_api_path,
        f"-I{include_path}",
        "--generator", generator_path,
    ])

    mod_path = Path(os.pardir, "packages", name, "src", f"{mod_name}.bnj")
    shutil.move("bindings.bnj", mod_path)
