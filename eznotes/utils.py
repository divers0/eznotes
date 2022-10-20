def executable_exists(name):
    from shutil import which

    return which(name) is not None
