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

    return False


def rename_symbol(sym):
    if sym.kind == "func":
        sym.name = sym.name[4:]
    elif sym.kind == "const":
        sym.name = sym.name[5:]
    elif sym.kind == "struct":
        sym.name = sym.name[4].upper() + sym.name[5:]

        for field in sym.fields:
            field.name = utils.to_snake_case(field.name)
