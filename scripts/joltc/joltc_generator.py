import utils


def filter_symbol(sym):
    return sym.name.startswith("JPH_")


def rename_symbol(sym):
    if sym.kind == "func":
        return utils.to_snake_case(sym.name[4:])
    elif sym.kind in ("field", "param"):
        return utils.to_snake_case(sym.name)
    elif sym.kind == "enum_variant":
        if sym.name[0] != "_":
            prefix = sym.enum_common_prefix_len
            return utils.to_snake_case(sym.name[prefix:]).upper()
        elif sym.name.endswith("_Count"):
            return "COUNT"
        elif sym.name.endswith("_Force32"):
            return "FORCE32"
    else:
        return sym.name[4:]


def enum_variants_with_common_prefix(variants):
    return [v for v in variants if v[0] != "_"]
