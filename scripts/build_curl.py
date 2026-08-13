import subprocess
import building

GIT_TAG = "curl-8_21_0"
OPENSSL_GIT_TAG = "openssl-3.6.3"
ZLIB_GIT_TAG = "v1.3.2"
ZSTD_GIT_TAG = "v1.5.7"

SETOPT_PATCH = """
CURLcode curl_easy_setopt_l(CURL *handle, CURLoption option, long long parameter) {
  return curl_easy_setopt(handle, option, parameter);
}

CURLcode curl_easy_setopt_p(CURL *handle, CURLoption option, void *parameter) {
  return curl_easy_setopt(handle, option, parameter);
}

CURLcode curl_easy_setopt_s(CURL *handle, CURLoption option, const char *parameter) {
  return curl_easy_setopt(handle, option, parameter);
}
"""

# Dependencies:
#   Windows: perl
#   Ubuntu: perl
#   macOS: perl

if __name__ == "__main__":
    building.package_name = "curl"

    building.git_clone("curl", "https://github.com/curl/curl.git", GIT_TAG)
    building.git_clone("openssl", "https://github.com/openssl/openssl.git", OPENSSL_GIT_TAG)
    building.git_clone("zlib", "https://github.com/madler/zlib", ZLIB_GIT_TAG)
    building.git_clone("zstd", "https://github.com/facebook/zstd", ZSTD_GIT_TAG)

    with open(building.get_path("curl/lib/setopt.c"), "r+") as f:
        content = f.read()

        if content.find(SETOPT_PATCH) == -1:
            content += SETOPT_PATCH

            f.seek(0)
            f.write(content)
            f.truncate()

    openssl_path = building.get_path("openssl")
    openssl_install_path = openssl_path / "install" / building.target_string()

    command = [
        "perl",
        "./Configure",
        f"--prefix={openssl_install_path}",
        "no-shared",
    ]

    subprocess.run(command, cwd=openssl_path)

    openssl_make_tool = "nmake" if building.is_windows() else "make"
    subprocess.run([openssl_make_tool, "install"], cwd=openssl_path)

    zlib_install_path = building.cmake_build("zlib", [])
    zstd_install_path = building.cmake_build("zstd/build/cmake", [])

    ssl_library_name = "libssl.lib" if building.is_windows() else "libssl.a"
    crypto_library_name = "libcrypto.lib" if building.is_windows() else "libcrypto.a"
    zlib_library_name = "z.lib" if building.is_windows() else "libz.a"
    zstd_library_name = "zstd.lib" if building.is_windows() else "libzstd.a"

    cmake_args = [
        "-DCURL_USE_PKGCONFIG=OFF",
        "-DBUILD_STATIC_LIBS=ON",
        "-DCURL_USE_OPENSSL=ON",
        f"-DOPENSSL_ROOT_DIR={openssl_install_path}",
        f"-DZLIB_INCLUDE_DIR={zlib_install_path}/include",
        f"-DZLIB_LIBRARY={zlib_install_path}/lib/{zlib_library_name}",
        f"-DZSTD_INCLUDE_DIR={zstd_install_path}/include",
        f"-DZSTD_LIBRARY={zstd_install_path}/lib/{zstd_library_name}",
        "-DUSE_LIBIDN2=OFF",
        "-DUSE_NGHTTP2=OFF",
        "-DCURL_USE_LIBPSL=OFF",
        "-DCURL_BROTLI=OFF",
        "-DCURL_DISABLE_LDAP=ON",
    ]

    install_path = building.cmake_build("curl", cmake_args)
    library_name = "libcurl.lib" if building.is_windows() else "libcurl.a"

    building.copy_libraries(install_path / "lib", [library_name])
    building.copy_libraries(openssl_install_path / "lib", [ssl_library_name, crypto_library_name])
    building.copy_libraries(zlib_install_path / "lib", [zlib_library_name])
    building.copy_libraries(zstd_install_path / "lib", [zstd_library_name])

    building.generate_bindings(install_path / "include", "curl")

    building.copy_license(building.get_path("curl/LICENSES/curl.txt"), "curl")
    building.copy_license(building.get_path("openssl/LICENSE.txt"), "openssl")
    building.copy_license(building.get_path("zlib/LICENSE"), "zlib")
    building.copy_license(building.get_path("zstd/LICENSE"), "zstd")
