import building

VERSION = "release-3.2.14"

BINDINGS_REPLACEMENTS = [
    ("const FLT_EPSILON: i64 = 1.1920928955078125e-07f;", "const FLT_EPSILON: f64 = 0.00000011920928955078125;"),
    ("const PI_D: i64 = 3.141592653589793238462643383279502884;", "const PI_D: f64 = 3.141592653589793238462643383279502884;"),
    ("const PI_F: i64 = 3.141592653589793238462643383279502884f;", "const PI_F: f32 = 3.141592653589793238462643383279502884;"),
    ("const ALPHA_OPAQUE_FLOAT: i64 = 1.0f;", "const ALPHA_OPAQUE_FLOAT: f64 = 1.0;"),
    ("const ALPHA_TRANSPARENT_FLOAT: i64 = 0.0f;", "const ALPHA_TRANSPARENT_FLOAT: f64 = 0.0;"),
    ("const STANDARD_GRAVITY: i64 = 9.80665f;", "const STANDARD_GRAVITY: f64 = 9.80665;"),
]

# Dependencies:
#   Windows: none
#   Ubuntu: none
#   macOS: none

if __name__ == "__main__":
    building.package_name = "sdl"
    building.git_clone("SDL", "https://github.com/libsdl-org/SDL.git", VERSION)
    
    install_path = building.cmake_build("SDL", ["-DSDL_STATIC=ON"])

    library_name = "SDL3.lib" if building.is_windows() else "libSDL3.a"
    building.copy_libraries(install_path / "lib", [library_name])
    
    building.generate_bindings(install_path / "include", "sdl")
    building.copy_license(building.get_path("SDL/LICENSE.txt"))

    # TODO: Remove this as soon as these bugs in bindgen have been fixed.
    bindings_path = building.get_package_path() / "src" / "sdl.bnj"
 
    with open(bindings_path) as f:
        bindings_source = f.read()
    
    for old, new in BINDINGS_REPLACEMENTS:
        bindings_source = bindings_source.replace(old, new, 1)

    with open(bindings_path, "w") as f:
        f.write(bindings_source)
