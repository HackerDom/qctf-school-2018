from hashlib import md5

TEAMS_COUNT = 200


def gen_task_id(team_id):
    return md5(b"8n?KLzP=4aymhn9gKNVVUVa$DF84fs%d" % team_id).hexdigest()


def gen_flag(team_id):
    return "QCTF{%s}" % md5(
        b"MM4P6JC9=NxXab=QxcU&aMhqF#vQtH%d" % team_id).hexdigest()


task_ids = [gen_task_id(team_id) for team_id in range(TEAMS_COUNT)]
flags = [gen_flag(team_id) for team_id in range(TEAMS_COUNT)]


def main():
    print("task_ids = %s" % repr(task_ids))
    print("flags = %s" % repr(flags))


if __name__ == '__main__':
    main()
