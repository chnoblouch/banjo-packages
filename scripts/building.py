from pathlib import Path
import subprocess
import shutil
import os
import platform


package_name = None


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


def target_string(target=host_target()):
    arch, os, env = target

    string = f"{arch}-{os}"
    if env:
        string += f"-{env}"
    
    return string


def is_windows():
    return host_target()[1] == "windows"


def is_linux():
    return host_target()[1] == "linux"


def is_macos():
    return host_target()[1] == "macos"


def get_path(directory):
    return Path(package_name, directory)


def get_package_path():
    return Path(os.pardir, "packages", package_name)


def git_clone(name, url, tag, recursive=False):
    path = Path(package_name, name)

    if not path.is_dir():
        command = ["git", "clone", url, str(path)]

        if recursive:
            command.append("--recursive")

        subprocess.run(command)

    subprocess.run(["git", "-C", str(path), "checkout", tag])


def cmake_build(directory, configure_args=[]):
    path = Path(package_name, directory)
    build_path = Path(path, "build", target_string())
    install_path = Path(path, "install", target_string())

    subprocess.run([
        "cmake", str(path),
        f"-B{build_path}",
        f"-GNinja",
        f"-DCMAKE_INSTALL_PREFIX={install_path}",
        *configure_args,
    ])

    subprocess.run([
        "cmake",
        "--build", str(build_path),
        "--target", "install",
    ])

    return install_path.absolute()


def copy_libraries(lib_path, libraries):
    _, target_os, _ = host_target()

    package_lib_path = Path(os.pardir, "packages", package_name, "lib", target_string())
    package_lib_path.mkdir(parents=True, exist_ok=True) 

    for library in libraries:
        shutil.copy(lib_path / library, package_lib_path / library)


def copy_license(license_path):
    package_path = Path(os.pardir, "packages", package_name)
    shutil.copy(license_path, package_path / "LICENSE.txt")


def generate_bindings(include_path, mod_name):
    c_api_path = Path(package_name, f"{package_name}_api.c")
    generator_path = Path(package_name, f"{package_name}_generator.py")

    command = [
        "banjo", "bindgen", c_api_path,
        "--generator", generator_path,
    ]

    if type(include_path) is str:
        command.append(f"-I{include_path}")
    elif type(include_path) is list:
        command.extend(f"-I{path}" for path in include_path)

    subprocess.run(command)

    src_path = Path(os.pardir, "packages", package_name, "src")
    src_path.mkdir(exist_ok=True)

    mod_path = src_path / f"{mod_name}.bnj"
    shutil.move("bindings.bnj", mod_path)
