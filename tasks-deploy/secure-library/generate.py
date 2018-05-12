TITLE = "Защищенная библиотека"
STATEMENT_TEMPLATE = '''
В этой библиотеке можно прочитать любую книгу, если захотеть.

`nc secure-library.contest.qctf.ru 20003`

[library](/static/files/<task.id>/library)
'''

def generate(context):
    return TaskStatement(TITLE, STATEMENT_TEMPLATE)
