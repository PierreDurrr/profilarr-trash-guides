def get_name(service, profile_name):
    safe_profile_name = (
        profile_name.replace("/", "-")
        .replace("[", "(")
        .replace("]", ")")
        .replace("HDR10Plus", "HDR10+")
        .replace("10 bit", "10bit")
        .replace("Atmos", "ATMOS")
    )
    return f"{service.capitalize()} - {safe_profile_name}"
