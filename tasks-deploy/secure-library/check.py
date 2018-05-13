FLAG = 'QCTF{n0b0dy_5h0uld_533_7h15_53cur3_73x7}'

def check(attempt, context):
    return Checked(attempt.answer == FLAG)
