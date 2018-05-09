import uuid
import random
import string


random.seed("SCHOOL_QCTF_2018_STASH")
FLAG = "QCTF{{h3re_is_y0ur_R4ng3d_st4Sh_{}}}"
ALPHABET = string.ascii_letters + string.digits


def get_rand_uuid():
    return uuid.UUID(bytes=bytes(bytearray(random.getrandbits(8) for _ in range(16))))


def get_rand_text():
    return "".join(random.choice(ALPHABET) for _ in range(8))


if __name__ == '__main__':
    flags = {get_rand_uuid(): FLAG.format(get_rand_text()) for _ in range(500)}
    with open("flags.py", mode="w") as flags_file:
        flags_file.writelines([
            "FLAGS = {\n",
            *["    \"{}\": \"{}\",\n".format(key, flags[key]) for key in sorted(flags)],
            "}"
        ])
