import utils


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
        if name[0].islower():
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
