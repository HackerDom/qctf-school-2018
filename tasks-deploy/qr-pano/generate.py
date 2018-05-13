TITLE = 'Pano'
STATEMENT = '''
Солнце над Зоной - редкое явление. Но в те дни, когда оно пробивается из-за туч,
можно заметить интересную особенность: его свет не похож на то, к чему привыкли люди
до катастрофы. Более того, порой оно высвечивает то, что сложно увидеть в обычном сумраке
затянутого облаками неба. В один такой день, восхищённый внезапно открывшейся панорамой,
я сделал [фотоснимок](/static/files/7bjf8qvcne/photo.jpg).
'''

def generate(context):
    return TaskStatement(TITLE, STATEMENT)
