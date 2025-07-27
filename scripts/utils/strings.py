def get_safe_name(name):
    return (
        name.replace("/", "-")
        .replace("[", "(")
        .replace("]", ")")
        .replace("HDR10Plus", "HDR10+")
        .replace("10 bit", "10bit")
        .replace("Atmos", "ATMOS")
    )


def get_name(service, name):
    return f"{service.capitalize()} - {get_safe_name(name)}"


def get_regex_pattern_name(service, regex_pattern_name):
    return get_name(service, regex_pattern_name).replace("Not ", "")
