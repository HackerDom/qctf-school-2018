

def load_file(filename):
    with open(filename, mode="rb") as file:
        try:
            return file.read()
        except IOError as e:
            print("Couldn't find image file! ({})".format(e))
            return None
