TITLE = "Защищенная библиотека"
STATEMENT_TEMPLATE = '''В этой библиотеке можно прочитать любую книгу, если захотеть.

[library](/static/files/<task.id>/library)'''

def generate(context):
    return TaskStatement(TITLE, STATEMENT)
