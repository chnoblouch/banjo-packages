import utils


STDINC_FUNCS = [
    "SDL_abs",
    "SDL_acos",
    "SDL_acosf",
    "SDL_aligned_alloc",
    "SDL_aligned_alloc_zero",
    "SDL_aligned_free",
    "SDL_asin",
    "SDL_asinf",
    "SDL_asprintf",
    "SDL_atan",
    "SDL_atan2",
    "SDL_atan2f",
    "SDL_atanf",
    "SDL_atof",
    "SDL_atoi",
    "SDL_bsearch",
    "SDL_bsearch_r",
    "SDL_calloc",
    "SDL_ceil",
    "SDL_ceilf",
    "SDL_copysign",
    "SDL_copysignf",
    "SDL_cos",
    "SDL_cosf",
    "SDL_crc16",
    "SDL_crc32",
    "SDL_CreateEnvironment",
    "SDL_DestroyEnvironment",
    "SDL_exp",
    "SDL_expf",
    "SDL_fabs",
    "SDL_fabsf",
    "SDL_floor",
    "SDL_floorf",
    "SDL_fmod",
    "SDL_fmodf",
    "SDL_free",
    "SDL_getenv",
    "SDL_getenv_unsafe",
    "SDL_GetEnvironment",
    "SDL_GetEnvironmentVariable",
    "SDL_GetEnvironmentVariables",
    "SDL_GetMemoryFunctions",
    "SDL_GetNumAllocations",
    "SDL_GetOriginalMemoryFunctions",
    "SDL_iconv",
    "SDL_iconv_close",
    "SDL_iconv_open",
    "SDL_iconv_string",
    "SDL_isalnum",
    "SDL_isalpha",
    "SDL_isblank",
    "SDL_iscntrl",
    "SDL_isdigit",
    "SDL_isgraph",
    "SDL_isinf",
    "SDL_isinff",
    "SDL_islower",
    "SDL_isnan",
    "SDL_isnanf",
    "SDL_isprint",
    "SDL_ispunct",
    "SDL_isspace",
    "SDL_isupper",
    "SDL_isxdigit",
    "SDL_itoa",
    "SDL_lltoa",
    "SDL_log",
    "SDL_log10",
    "SDL_log10f",
    "SDL_logf",
    "SDL_lround",
    "SDL_lroundf",
    "SDL_ltoa",
    "SDL_malloc",
    "SDL_memcmp",
    "SDL_memcpy",
    "SDL_memmove",
    "SDL_memset",
    "SDL_memset4",
    "SDL_modf",
    "SDL_modff",
    "SDL_murmur3_32",
    "SDL_pow",
    "SDL_powf",
    "SDL_qsort",
    "SDL_qsort_r",
    "SDL_rand",
    "SDL_rand_bits",
    "SDL_rand_bits_r",
    "SDL_rand_r",
    "SDL_randf",
    "SDL_randf_r",
    "SDL_realloc",
    "SDL_round",
    "SDL_roundf",
    "SDL_scalbn",
    "SDL_scalbnf",
    "SDL_setenv_unsafe",
    "SDL_SetEnvironmentVariable",
    "SDL_SetMemoryFunctions",
    "SDL_sin",
    "SDL_sinf",
    "SDL_size_add_check_overflow",
    "SDL_size_mul_check_overflow",
    "SDL_snprintf",
    "SDL_sqrt",
    "SDL_sqrtf",
    "SDL_srand",
    "SDL_sscanf",
    "SDL_StepBackUTF8",
    "SDL_StepUTF8",
    "SDL_strcasecmp",
    "SDL_strcasestr",
    "SDL_strchr",
    "SDL_strcmp",
    "SDL_strdup",
    "SDL_strlcat",
    "SDL_strlcpy",
    "SDL_strlen",
    "SDL_strlwr",
    "SDL_strncasecmp",
    "SDL_strncmp",
    "SDL_strndup",
    "SDL_strnlen",
    "SDL_strnstr",
    "SDL_strpbrk",
    "SDL_strrchr",
    "SDL_strrev",
    "SDL_strstr",
    "SDL_strtod",
    "SDL_strtok_r",
    "SDL_strtol",
    "SDL_strtoll",
    "SDL_strtoul",
    "SDL_strtoull",
    "SDL_strupr",
    "SDL_swprintf",
    "SDL_tan",
    "SDL_tanf",
    "SDL_tolower",
    "SDL_toupper",
    "SDL_trunc",
    "SDL_truncf",
    "SDL_UCS4ToUTF8",
    "SDL_uitoa",
    "SDL_ulltoa",
    "SDL_ultoa",
    "SDL_unsetenv_unsafe",
    "SDL_UnsetEnvironmentVariable",
    "SDL_utf8strlcpy",
    "SDL_utf8strlen",
    "SDL_utf8strnlen",
    "SDL_vasprintf",
    "SDL_vsnprintf",
    "SDL_vsscanf",
    "SDL_vswprintf",
    "SDL_wcscasecmp",
    "SDL_wcscmp",
    "SDL_wcsdup",
    "SDL_wcslcat",
    "SDL_wcslcpy",
    "SDL_wcslen",
    "SDL_wcsncasecmp",
    "SDL_wcsncmp",
    "SDL_wcsnlen",
    "SDL_wcsnstr",
    "SDL_wcsstr",
    "SDL_wcstol",
    "SDL_wcstoll",
    "SDL_wcstoul",
    "SDL_wcstoull",
]


def filter_symbol(sym):
    return sym.name.startswith(("SDL_", "IMG_", "TTF_"))


def rename_symbol(sym):
    name = sym.name

    if name.startswith("SDL_"):
        name = sym.name[4:]
    
    if name.startswith("IMG_"):
        if sym.kind == "func":
            name = "img_" + name[4:]
        elif sym.kind in ("struct", "union", "enum"):
            name = "IMG" + name[4:]
        elif sym.kind != "const":
            name = name[4:]
    if name.startswith("TTF_"):
        if sym.kind == "func":
            name = "ttf_" + name[4:]
        elif sym.kind in ("struct", "union", "enum"):
            name = "TTF" + name[4:]
        elif sym.kind != "const":
            name = name[4:]

    if sym.kind == "func":
        if sym.name in STDINC_FUNCS:
            return "stdinc_" + utils.to_snake_case(name)
        else:
            return utils.to_snake_case(name)
    elif sym.kind == "param":
        return utils.to_snake_case(name)
    elif sym.kind == "enum_variant":
        prefix = sym.enum_common_prefix_len
        
        while sym.name[prefix - 1] != "_":
            prefix -= 1

        return sym.name[prefix:]
    else:
        return name
