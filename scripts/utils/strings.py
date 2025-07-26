def get_file_name(profile_name):
    return (
        profile_name.replace("/", "-")
        .replace("[", "(")
        .replace("]", ")")
        # TODO: This triggers to often, how to be more specific?
        .replace("HDR10Plus", "HDR10+")
    )
