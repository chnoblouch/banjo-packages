import utils


def filter_symbol(sym):
    return sym.name.startswith(("SDL_", "IMG_", "TTF_"))


def rename_symbol(sym):
    if sym.name.startswith("SDL_"):
        sym.name = sym.name[4:]
    
    if sym.name.startswith("IMG_"):
        if sym.kind == "func":
            sym.name = "img_" + sym.name[4:]
        elif sym.kind in ("struct", "union", "enum"):
            sym.name = "IMG" + sym.name[4:]
        elif sym.kind != "const":
            sym.name = sym.name[4:]
    if sym.name.startswith("TTF_"):
        if sym.kind == "func":
            sym.name = "ttf_" + sym.name[4:]
        elif sym.kind in ("struct", "union", "enum"):
            sym.name = "TTF" + sym.name[4:]
        elif sym.kind != "const":
            sym.name = sym.name[4:]

    if sym.kind == "func":
        sym.name = utils.to_snake_case(sym.name)
    elif sym.kind == "enum":
        prefix = utils.common_prefix_len([variant.name for variant in sym.variants])
        
        for variant in sym.variants:
            variant.name = variant.name[prefix:]
    
    sym.name = sym.name.replace("__", "_")
