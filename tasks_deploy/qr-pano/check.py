FLAG = 'QCTF{Ar3nt_sph3r1cal_pan0s_w0nd3rful}'


def check(attempt, context):
    return Checked(attempt.answer == FLAG)
