

from pyvis.network import Network
from conllu import parse_tree
from random import *
from conllu import parse_tree_incr

def get_title(vert):
    title = "lemma: " + str(vert.token["lemma"]) + "\npos: " + vert.token["upos"]
    return title

def process_vert(tree, vert, index=0, level=0):
    parent = index
    level += 1
    for kid in vert.children:
        #print(type(kid))
        #if kid.token['upos'] == 'PUNCT':
            #continue
        index = tree.num_nodes()
        tree.add_node(index, size=10, level=level, shape="box", label=str(kid.token), title=get_title(kid))
        #tree.nodes[index]['color'] = color_dict[kid.token["upos"]]
        tree.add_edge(parent, index, color='white', label=kid.token["deprel"])
        process_vert(tree, kid, index=index, level=level)

def make_tree(root):
    tree = Network(layout="complete_graph", directed=True, height='650px', width='1400px', bgcolor='#222222', font_color='black', heading=root.metadata['sent_id'])
    tree.toggle_physics(True)
    tree.show_buttons(filter_=['physics'])
    tree.add_node(0, level=0, size=10, shape="box", label=str(root.token), title=get_title(root))
    #tree.nodes[0]['color'] = color_dict[root.token["upos"]]
    process_vert(tree, root)
    file_name = root.metadata['sent_id'] + '.html'
    tree.show(file_name)


def get_label(vert):
    if vert.token['form'] != '_':
        return vert.token['form']
    return vert.token['upos']

def get_title(vert):
    return None

def check_edge(vert):
    if vert.token['form'] == '_':
        return 'red'
    return 'white'


def process_vertex(tree, vert, index=0, level=0):
    parent=index
    level += 1
    for kid in vert.children:
        index = tree.num_nodes()
        tree.add_node(index, size=10, level=level, shape='box', label=get_label(kid), title=get_title(kid), color='white')

        tree.add_edge(parent, index, color=check_edge(kid), label='none')
        process_vertex(tree, kid, index, level)


def process_tree(sentence):
    tree = Network(layout="complete_graph", directed=True, height='100%', width='100%', bgcolor='#222222', font_color='black', heading=sentence.metadata['sent_id'])
    tree.toggle_physics(True)
    tree.show_buttons(filter_=['physics'])
    tree.add_node(0, level=0, size=10, shape="box", label=get_label(sentence), title=get_title(sentence), color='white')
    process_vertex(tree, sentence)
    file_name = sentence.metadata['sent_id'] + '.html'
    tree.show(file_name)

def visualize(file):
    #data_file = open("mydata.conllu.txt", "r", encoding="utf-8")
    data_file = open(file, "r", encoding="utf-8")
    for sentence in parse_tree_incr(data_file):
        print("I AM HERE")
        process_tree(sentence)
