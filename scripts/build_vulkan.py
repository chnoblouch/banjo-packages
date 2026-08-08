import building

VERSION = "1.4.303"
GIT_TAG = f"v{VERSION}"

# Dependencies:
#   Windows: none
#   Ubuntu: none
#   macOS: none

if __name__ == "__main__":
    building.package_name = "vulkan"

    # if building.is_macos():
    #     exit(0)

    building.git_clone("Vulkan-Headers", "https://github.com/KhronosGroup/Vulkan-Headers.git", GIT_TAG)
    building.git_clone("Vulkan-Loader", "https://github.com/KhronosGroup/Vulkan-Loader.git", GIT_TAG)
    
    headers_install_dir = building.cmake_build("Vulkan-Headers")

    install_dir = building.cmake_build("Vulkan-Loader", configure_args=[
        f"-DVULKAN_HEADERS_INSTALL_DIR={headers_install_dir}/share/cmake/VulkanHeaders"
    ])

    if building.is_windows():
        library_name = "vulkan-1.lib"
    elif building.is_linux():
        library_name = f"libvulkan.so.{VERSION}"
    elif building.is_macos():
        library_name = "libvulkan.dylib"
    
    building.copy_libraries(install_dir / "lib", [library_name])

    building.copy_license(building.get_path("Vulkan-Headers/LICENSE.md"), "vulkan-headers")
    building.copy_license(building.get_path("Vulkan-Loader/LICENSE.txt"), "vulkan-loader")

    building.generate_bindings(headers_install_dir / "include", "vulkan")
