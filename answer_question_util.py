import nltk
from nltk.parse.stanford import StanfordParser
from nltk.tree import Tree

WHO = 0
WHAT = 1
HOW = 2
WHERE = 3
WH = "SBARQ"
BI1 = "SQ"
BI2 = "SINV"
DOLIST=["do","does","did"]
BELIST=["is","am","are","was","were"]

def question_classify(question):
    keywords = question[:2]
    if keywords[0] == "what":
        return WHAT
    elif keywords[0] == "who":
        return WHO
    elif keywords[0] == "how":
        return HOW
    elif keywords[0] == "where":
        return WHERE


def predicate_form(question):
    parser = StanfordParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
    tree = list(parser.raw_parse(question))[0]
    tree.draw()
    type = tree[0].label()
    if type == WH:
        if tree[0, 1, 0].leaves()[0] in DOLIST and len(tree[0, 1]) > 1:
            if tree[0, 1, 1].label() == "NP" and tree[0, 1, 2].label() == "VP":
                del tree[0, 1, 0]
                tree[0, 0], tree[0, 1] = tree[0, 1], tree[0, 0]
        elif tree[0, 1, 0].leaves()[0] in BELIST:
            tree[0, 1, 0, 1], tree[0, 0] = tree[0, 0], tree[0, 1, 0, 1]
        tree[0].set_label("S")
        tree[0, 0].set_label("S")
    elif type == BI1 or type == BI2:
        print tree[0,0]
        if tree[0, 0].leaves()[0] in DOLIST:
            del tree[0, 0]
        elif tree[0, 0].leaves()[0] in BELIST:
            if len(tree[0, 0]) != 1:
                tree[0, 0, 0], tree[0, 0, 1] = tree[0, 0, 1], tree[0, 0, 0]
            else:
                print tree[0,0]
                tree[0,0],tree[0,1,0,0]=tree[0,1,0,0],tree[0,0]
        tree[0].set_label("S")
    return type,tree


if __name__ == "__main__":
    type, tree = predicate_form("where did you go last night")
    print type
    # tree.draw()
    print tree.leaves()
