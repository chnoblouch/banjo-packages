import building

# Dependencies:
#   Windows: none
#   Ubuntu: xorg-dev libwayland-dev libxkbcommon-dev wayland-protocols extra-cmake-modules
#   macOS: none

if __name__ == "__main__":
    building.git_clone("glfw", "https://github.com/glfw/glfw.git")
    building.cmake_build("glfw", libraries=["glfw3"])
    building.generate_bindings("glfw", "glfw", "include")
