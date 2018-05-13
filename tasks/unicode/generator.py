import random
import string
from pathlib import Path
import codecs

TEAMS_COUNT = 200

def gen_flag(team_id):
	random.seed(b"pGZThTZKraJepQv2m?zx-A#t_DWCfJMe%d" % team_id)
	return "QCTF{4$C11_1$_t00_$m4LL_%s}" % "".join(random.choice(string.ascii_letters + string.digits) for _ in range(7))

def map_char(c):
	return chr(ord(c) - 0x20 + 0xff00)


flags = [gen_flag(team_id) for team_id in range(TEAMS_COUNT)]
tasks = [
	codecs.encode("".join(map_char(c) for c in flag), "unicode-escape").decode()
	for flag in flags
]

def main():
	Path("./task_data").write_text(
		"tasks = %s\nflags = %s" % (repr(tasks), repr(flags)))

if __name__ == '__main__':
    main()
