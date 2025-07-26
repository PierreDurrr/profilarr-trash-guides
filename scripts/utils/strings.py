def get_file_name(profile_name):
    return (
        profile_name.replace("/", "-")
        .replace("[", "(")
        .replace("]", ")")
        .replace("HDR10Plus", "HDR10+")
        .replace("10 bit", "10bit")
        .replace("Atmos", "ATMOS")
    )
