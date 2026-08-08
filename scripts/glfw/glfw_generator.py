import utils


def filter_file_path(path):
    return "glfw3" in path


def filter_symbol(sym):
    if sym.kind == "func":
        return sym.name.startswith("glfw")
    elif sym.kind == "const":
        return sym.name.startswith("GLFW_")
    elif sym.kind == "struct":
        return sym.name.startswith("GLFW")
    else:
        return False


def rename_symbol(sym):
    if sym.kind == "func":
        return utils.to_snake_case(sym.name[4:])
    elif sym.kind == "const":
        return sym.name[5:]
    elif sym.kind == "struct":
        return sym.name[4].upper() + sym.name[5:]
    elif sym.kind in ("param", "field"):
        return utils.to_snake_case(sym.name)
    else:
        return None
