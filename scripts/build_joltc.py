import building

VERSION = "v5.6.0"
JOLTC_COMMIT = "886e088675bae3a086f8318c7803f8ee962c2f2c"

# Dependencies:
#   Windows: none
#   Ubuntu: none
#   macOS: none

if __name__ == "__main__":
    building.package_name = "joltc"
    building.git_clone("JoltPhysics", "https://github.com/jrouwe/joltphysics", VERSION)
    building.git_clone("joltc", "https://github.com/amerkoleci/joltc.git", JOLTC_COMMIT)

    with open(building.get_path("joltc/CMakeLists.txt"), "r+") as f:
        content = f.read()
        index = content.find("install(FILES $<TARGET_PDB_FILE:")

        if content[index - 2] != "#":
            content = content[:index] + "# " + content[index:]
            f.seek(0)
            f.write(content)
            f.truncate()

    configure_args = [
        "-DJPH_BUILD_SHARED=OFF",
        "-DJPH_USE_DX12=OFF",
        "-DJPH_USE_VK=OFF",
        "-DJPH_USE_MTL=OFF",
    ]

    install_path = building.cmake_build("joltc", configure_args)

    jolt_library_name = ("Joltd.lib", "Jolt.lib") if building.is_windows() else "libJolt.a"
    joltc_library_name = ("joltcd.lib", "joltc.lib") if building.is_windows() else "libjoltc.a"

    building.copy_libraries(install_path / "lib", [jolt_library_name, joltc_library_name])

    building.copy_license(building.get_path("JoltPhysics/LICENSE"), "jolt")
    building.copy_license(building.get_path("joltc/LICENSE"), "joltc")

    building.generate_bindings(building.get_path("joltc/include"), "joltc")
