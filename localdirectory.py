import os


def local_directory(memorydrive=r"C:\Users", lookingfor='P-O3', path = ""):
    try:
        if path == lookingfor:
            return path
        elif lookingfor in os.listdir(memorydrive):
            return os.path.join(memorydrive,lookingfor)
        if os.path.isfile(os.path.join(memorydrive, path)):
            return None
        for i in os.listdir(memorydrive):
            result = local_directory(os.path.join(memorydrive, i), lookingfor, i)
            if result is not None:
                return result
        return None
        # os.path.exist(r"C:\Users")
        # os.path.isfile(fpath)
    except:
        return None


try1 = local_directory(r"C:\Users")
try2 = local_directory(r"C:\Gebruikers")
if try1 is not None:
    print(try1)
elif try2 is not None:
    print(try2)
else:
    print(None)