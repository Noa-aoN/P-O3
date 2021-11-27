import os


def local_directory(memorydrive=r"C:\Users", lookingfor='P-O3', path = ""):
    if path == lookingfor:
        return path
    elif lookingfor in os.listdir(memorydrive):
        return os.path.join(memorydrive,lookingfor)
    if os.path.isfile(os.path.join(memorydrive, path)):
        return None
    try:
        for i in os.listdir(memorydrive):
            result = local_directory(os.path.join(memorydrive, i), lookingfor, i)
            if result is not None:
                return result
        return None
        # os.path.exist(r"C:\Users")
        # os.path.isfile(fpath)
    except:
        return None


print(local_directory())