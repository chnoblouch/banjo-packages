import building

VERSION = "1.4.303"
GIT_TAG = f"v{VERSION}"

# Dependencies:
#   Windows: none
#   Ubuntu: none
#   macOS: none

if __name__ == "__main__":
    building.package_name = "vulkan"

    if building.is_macos():
        exit(0)

    building.git_clone("Vulkan-Headers", "https://github.com/KhronosGroup/Vulkan-Headers.git", GIT_TAG)
    building.git_clone("Vulkan-Loader", "https://github.com/KhronosGroup/Vulkan-Loader.git", GIT_TAG)
    
    headers_install_dir = building.cmake_build("Vulkan-Headers")

    install_dir = building.cmake_build("Vulkan-Loader", configure_args=[
        f"-DVULKAN_HEADERS_INSTALL_DIR={headers_install_dir}/share/cmake/VulkanHeaders"
    ])
    
    library_name = "vulkan-1.lib" if building.is_windows() else f"libvulkan.so.{VERSION}" 
    building.copy_libraries(install_dir / "lib", [library_name])
    
    building.generate_bindings(headers_install_dir / "include", "vulkan")
