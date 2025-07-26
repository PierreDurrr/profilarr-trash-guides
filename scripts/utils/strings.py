def get_file_name(profile_name):
    return profile_name.replace("/", "-").replace("[", "(").replace("]", ")")
