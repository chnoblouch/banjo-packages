import building

VERSION = "3.4"

# Dependencies:
#   Windows: none
#   Ubuntu: xorg-dev libwayland-dev libxkbcommon-dev wayland-protocols extra-cmake-modules
#   macOS: none

if __name__ == "__main__":
    building.package_name = "glfw"
    building.git_clone("glfw", "https://github.com/glfw/glfw.git", VERSION)
    
    install_path = building.cmake_build("glfw")

    library_name = "glfw3.lib" if building.is_windows() else "libglfw3.a"
    building.copy_libraries(install_path / "lib", [library_name])
    
    building.generate_bindings(install_path / "include", "glfw")
