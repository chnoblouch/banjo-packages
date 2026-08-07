import utils


def filter_symbol(sym):
    return sym.name.startswith("JPH_")


def rename_symbol(sym):
    sym.name = sym.name[4:]

    if sym.kind == "func":
        sym.name = utils.to_snake_case(sym.name)
        rename_params(sym.params)
    elif sym.kind == "struct":
        for field in sym.fields:
            field.name = utils.to_snake_case(field.name)
    elif sym.kind == "enum":
        prefix = utils.common_prefix_len([v.name for v in sym.variants if v.name[0] != "_"])
        
        for variant in sym.variants:
            if variant.name[0] != "_":
                variant.name = utils.to_snake_case(variant.name[prefix:]).upper()
            elif variant.name.endswith("_Count"):
                variant.name = "COUNT"
            elif variant.name.endswith("_Force32"):
                variant.name = "FORCE32"


def rename_params(params):
    for param in params:
        if param.name is not None:
            param.name = utils.to_snake_case(param.name)
