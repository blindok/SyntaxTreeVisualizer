from io import open
from conllu import parse_tree
from conllu import parse_incr
from conllu.models import TokenList, Token
from visualizer import visualize

#добавляем новую группу
def add_token(sentence, form, id, head=None, deprel=None):
    token = Token(id=id, form=None, lemma=None, upos=form, xpos=None, feats=None, head=head, deprel=deprel, deps=[(deprel, head)])
    sentence.insert(id-1, token)

    for i in range(1, len(sentence)):
        if i >= id:
            sentence[i]['id'] += 1
        if sentence[i]['head'] >= id or id==1:
            sentence[i]['head'] += 1
            sentence[i]['deps'] = [(sentence[i]['deprel'], sentence[i]['head'])]

    return token


#ищем токен, который указывает на нужного нам родителя
def search_by_parent(sentence, parent_id, id):
    for token in sentence:
        if token['head'] == parent_id:
            if token['upos'] != 'PUNCT' and token['upos'] != 'SCONJ':
                return token
    return None

def get_id(token):
    return token['id']

#в передаваемом массиве - токены, в результате - строка с раставленными по порядку словами
def form_chunk(array):
    array.sort(key=get_id)
    chunk = ''
    for token in array:
        chunk += token['form'] + ' '
    return chunk

#составить чанк по заданному слову (то есть собрать в кучу все зависимые слова от заданного слова)
def get_chunk(sentence, token):
    array = []
    start_token = token
    array.append(token)
    while True:
        new_token = search_by_parent(sentence, token['id'], 0)
        if new_token is None:
            break
        array.append(new_token)
        token = new_token

    chunk = form_chunk(array)
    add_token(sentence, chunk, array[0]['id'], head=start_token['head'], deprel=start_token['deprel'])
    start_token['head'] = array[0]['id'] - 1
    return chunk


def check_child(sentence, parent_id, token):
    for word in sentence:
        if word['head'] == token['id']:
            word['head'] = parent_id

#основная функция
def form_groups(sentence):
    add_token(sentence, sentence.metadata['text'], 1, 0, 'root')
    i = 1
    while i < len(sentence):
        if sentence[i]['deprel'] == 'case':
            token = sentence[i]
            id = i + 1
            head_token = sentence.filter(id=token['head'])[0]

            new_form = token['form'] + ' ' + head_token['form']
            new_token = add_token(sentence, new_form, id, head=head_token['head'], deprel= head_token['deprel'])
            head_token['head'] = id
            head_token['deps'] = [(head_token['deprel'], head_token['head'])]

            check_child(sentence, head_token['head'], head_token)
            parent_id = new_token['head']
            i += 1
        i += 1


data_file = open("mydata.conllu.txt", "r", encoding="utf-8")

for sentence in parse_incr(data_file):
    print("\n**********INPUT DATA**********\n")
    print(sentence.serialize())
    form_groups(sentence)
    print("\n************RESULT************\n")
    print(sentence.serialize())

    result_file = open('result.conllu.txt', 'w', encoding="utf-8")
    result_file.writelines(sentence.serialize())
    result_file.close()

    visualize('result.conllu.txt')



data_file.close()

