import building

SDL_VERSION = "release-3.4.0"
SDL_IMAGE_VERSION = "release-3.4.0"
# SDL_MIXER_VERSION = "release-2.8.1"
SDL_TTF_VERSION = "release-3.2.2"
# SDL_NET_VERSION = "release-2.2.0"

LIBRARIES = [
    ("SDL", "SDL3"),
    ("SDL_image", "SDL3_image"),
    # ("SDL_mixer", "SDL3_mixer"),
    ("SDL_ttf", "SDL3_ttf"),
    # ("SDL_net", "SDL3_net"),
]

BINDINGS_REPLACEMENTS = [
    ("const FLT_EPSILON: i64 = 1.1920928955078125e-07f;", "const FLT_EPSILON: f64 = 0.00000011920928955078125;"),
    ("const PI_D: i64 = 3.141592653589793238462643383279502884;", "const PI_D: f64 = 3.141592653589793238462643383279502884;"),
    ("const PI_F: i64 = 3.141592653589793238462643383279502884f;", "const PI_F: f32 = 3.141592653589793238462643383279502884;"),
    ("const ALPHA_OPAQUE_FLOAT: i64 = 1.0f;", "const ALPHA_OPAQUE_FLOAT: f64 = 1.0;"),
    ("const ALPHA_TRANSPARENT_FLOAT: i64 = 0.0f;", "const ALPHA_TRANSPARENT_FLOAT: f64 = 0.0;"),
    ("const STANDARD_GRAVITY: i64 = 9.80665f;", "const STANDARD_GRAVITY: f64 = 9.80665;"),
]

BINDINGS_APPEND = """const WINDOW_FULLSCREEN: u64 = 0x0000000000000001;
const WINDOW_OPENGL: u64 = 0x0000000000000002;
const WINDOW_OCCLUDED: u64 = 0x0000000000000004;
const WINDOW_HIDDEN: u64 = 0x0000000000000008;
const WINDOW_BORDERLESS: u64 = 0x0000000000000010;
const WINDOW_RESIZABLE: u64 = 0x0000000000000020;
const WINDOW_MINIMIZED: u64 = 0x0000000000000040;
const WINDOW_MAXIMIZED: u64 = 0x0000000000000080;
const WINDOW_MOUSE_GRABBED: u64 = 0x0000000000000100;
const WINDOW_INPUT_FOCUS: u64 = 0x0000000000000200;
const WINDOW_MOUSE_FOCUS: u64 = 0x0000000000000400;
const WINDOW_EXTERNAL: u64 = 0x0000000000000800;
const WINDOW_MODAL: u64 = 0x0000000000001000;
const WINDOW_HIGH_PIXEL_DENSITY: u64 = 0x0000000000002000;
const WINDOW_MOUSE_CAPTURE: u64 = 0x0000000000004000;
const WINDOW_MOUSE_RELATIVE_MODE: u64 = 0x0000000000008000;
const WINDOW_ALWAYS_ON_TOP: u64 = 0x0000000000010000;
const WINDOW_UTILITY: u64 = 0x0000000000020000;
const WINDOW_TOOLTIP: u64 = 0x0000000000040000;
const WINDOW_POPUP_MENU: u64 = 0x0000000000080000;
const WINDOW_KEYBOARD_GRABBED: u64 = 0x0000000000100000;
const WINDOW_VULKAN: u64 = 0x0000000010000000;
const WINDOW_METAL: u64 = 0x0000000020000000;
const WINDOW_TRANSPARENT: u64 = 0x0000000040000000;
const WINDOW_NOT_FOCUSABLE: u64 = 0x0000000080000000;

const GPU_TEXTUREUSAGE_SAMPLER: u32 = 0x00000001;
const GPU_TEXTUREUSAGE_COLOR_TARGET: u32 = 0x00000002;
const GPU_TEXTUREUSAGE_DEPTH_STENCIL_TARGET: u32 = 0x00000004;
const GPU_TEXTUREUSAGE_GRAPHICS_STORAGE_READ: u32 = 0x00000008;
const GPU_TEXTUREUSAGE_COMPUTE_STORAGE_READ: u32 = 0x00000010;
const GPU_TEXTUREUSAGE_COMPUTE_STORAGE_WRITE: u32 = 0x00000020;
const GPU_TEXTUREUSAGE_COMPUTE_STORAGE_SIMULTANEOUS_READ_WRITE: u32 = 0x00000040;

const GPU_BUFFERUSAGE_VERTEX: u32 = 0x00000001;
const GPU_BUFFERUSAGE_INDEX: u32 = 0x00000002;
const GPU_BUFFERUSAGE_INDIRECT: u32 = 0x00000004;
const GPU_BUFFERUSAGE_GRAPHICS_STORAGE_READ: u32 = 0x00000008;
const GPU_BUFFERUSAGE_COMPUTE_STORAGE_READ: u32 = 0x00000010;
const GPU_BUFFERUSAGE_COMPUTE_STORAGE_WRITE: u32 = 0x00000020;

const GPU_SHADERFORMAT_PRIVATE: u32 = 0x00000001;
const GPU_SHADERFORMAT_SPIRV: u32 = 0x00000002;
const GPU_SHADERFORMAT_DXBC: u32 = 0x00000004;
const GPU_SHADERFORMAT_DXIL: u32 = 0x00000008;
const GPU_SHADERFORMAT_MSL: u32 = 0x00000010;
const GPU_SHADERFORMAT_METALLIB: u32 = 0x00000020;

const GPU_COLORCOMPONENT_R: u32 = 0x00000001;
const GPU_COLORCOMPONENT_G: u32 = 0x00000002;
const GPU_COLORCOMPONENT_B: u32 = 0x00000004;
const GPU_COLORCOMPONENT_A: u32 = 0x00000008;
"""

# Dependencies:
#   Windows: perl, nasm
#   Ubuntu: none
#   macOS: none

if __name__ == "__main__":
    building.package_name = "sdl"

    building.git_clone("SDL", "https://github.com/libsdl-org/SDL.git", SDL_VERSION)
    building.git_clone("SDL_image", "https://github.com/libsdl-org/SDL_image.git", SDL_IMAGE_VERSION)
    # building.git_clone("SDL_mixer", "https://github.com/libsdl-org/SDL_mixer.git", SDL_MIXER_VERSION)
    building.git_clone("SDL_ttf", "https://github.com/libsdl-org/SDL_ttf.git", SDL_TTF_VERSION, recursive=True)
    # building.git_clone("SDL_net", "https://github.com/libsdl-org/SDL_net.git", SDL_NET_VERSION)

    cmake_args = ["-DBUILD_SHARED_LIBS=OFF", "-DCMAKE_POSITION_INDEPENDENT_CODE=ON"]
    sdl_install_path = building.cmake_build("SDL", cmake_args)
    library_name = f"SDL3-static.lib" if building.is_windows() else f"libSDL3.a"
    building.copy_libraries(sdl_install_path / "lib", [library_name])

    sdl_cmake_path = sdl_install_path / "cmake" if building.is_windows() else sdl_install_path / "lib" / "cmake" / "SDL3"

    cmake_args = ["-DBUILD_SHARED_LIBS=OFF", "-DCMAKE_POSITION_INDEPENDENT_CODE=ON", f"-DSDL3_DIR={sdl_cmake_path}", "-DSDLIMAGE_VENDORED=OFF"]
    sdl_image_install_path = building.cmake_build("SDL_image", cmake_args)
    library_name = f"SDL3_image-static.lib" if building.is_windows() else f"libSDL3_image.a"
    building.copy_libraries(sdl_image_install_path / "lib", [library_name])

    cmake_args = ["-DBUILD_SHARED_LIBS=OFF", "-DCMAKE_POSITION_INDEPENDENT_CODE=ON", f"-DSDL3_DIR={sdl_cmake_path}", "-DSDLTTF_VENDORED=ON"]
    sdl_ttf_install_path = building.cmake_build("SDL_ttf", cmake_args)
    library_name = f"SDL3_ttf-static.lib" if building.is_windows() else f"libSDL3_ttf.a"
    building.copy_libraries(sdl_ttf_install_path / "lib", [library_name])

    include_dirs = [
        sdl_install_path / "include",
        sdl_image_install_path / "include",
        sdl_ttf_install_path / "include",
    ]

    building.generate_bindings(include_dirs, "sdl")
    building.copy_license(building.get_path("SDL/LICENSE.txt"))

    # TODO: Remove this as soon as these bugs in bindgen have been fixed.
    bindings_path = building.get_package_path() / "src" / "sdl.bnj"
 
    with open(bindings_path) as f:
        bindings_source = f.read()
    
    for old, new in BINDINGS_REPLACEMENTS:
        bindings_source = bindings_source.replace(old, new, 1)

    bindings_source += BINDINGS_APPEND

    with open(bindings_path, "w") as f:
        f.write(bindings_source)
