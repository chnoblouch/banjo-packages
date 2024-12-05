import utils


def filter_symbol(sym):
    if sym.kind == "func":
        return sym.name.startswith("vk")
    elif sym.kind == "struct" or sym.kind == "enum":
        return sym.name.startswith("Vk") and not sym.name.endswith("_T")
    else:
        return False


def rename_symbol(sym):
    if sym.kind == "func":
        sym.name = sym.name[2:]
    if sym.kind == "struct" or sym.kind == "enum":
        sym.name = sym.name[2:] if sym.name.startswith("Vk") else sym.name
    elif sym.kind == "field":
        sym.name = utils.to_snake_case(sym.name)
    elif sym.kind == "enum_variant":
        enum_name = sym.enum.name.replace("KHR", "")
        enum_name = enum_name.replace("FlagBits", "")

        prefix = ""
        for i, char in enumerate(enum_name):
            if i == 0:
                prefix += char.upper()
                continue

            if char.isupper() and enum_name[i - 1].islower():
                prefix += "_"
            prefix += char.upper()
            
        if sym.name.startswith(prefix):
            sym.name = sym.name[len(prefix) + 1:]
        elif sym.name.startswith("VK_"):
            sym.name = sym.name[3:]
        else:
            sym.name = sym.name
    else:
        sym.name = sym.name
