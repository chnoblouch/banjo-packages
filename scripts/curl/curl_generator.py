import utils


def filter_symbol(sym):
    if sym.kind == "func":
        return sym.name.startswith("curl_")
    elif sym.kind == "const":
        return sym.name.startswith("CURL")
    elif sym.kind in ("struct", "enum"):
        return sym.name.startswith(("curl_", "CURL"))
    else:
        return True


def rename_symbol(sym):
    if sym.kind == "func":
        return utils.to_snake_case(sym.name[5:])
    elif sym.kind == "const":
        return sym.name[5:] if sym.name[4] == "_" else sym.name[4:]
    elif sym.kind in ("struct", "enum"):
        stripped = sym.name[5:] if sym.name[4] == "_" else sym.name[4:]
        return stripped[0].upper() + stripped[1:]
    elif sym.kind in ("param", "field"):
        return utils.to_snake_case(sym.name)
    elif sym.kind == "enum_variant":
        return sym.name[sym.enum_common_prefix_len:]
    else:
        return None
