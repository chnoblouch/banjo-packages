import building

# Dependencies:
#   Windows: none
#   Ubuntu: xorg-dev libwayland-dev libxkbcommon-dev wayland-protocols extra-cmake-modules
#   macOS: none

if __name__ == "__main__":
    building.package_name = "glfw"
    building.git_clone("glfw", "https://github.com/glfw/glfw.git")
    
    install_path = building.cmake_build("glfw")
    building.copy_libraries(install_path / "lib", ["glfw3"])
    building.generate_bindings(install_path / "include", "glfw")
