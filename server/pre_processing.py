import nltk
from nltk.corpus import brown
from time import gmtime, strftime


class Tree(object):
    def __init__(self):
        self.word = None
        self.next = []


def word_check(arr, word):
    for obj in range(len(arr)):
        if arr[obj].word == word:
            return obj
    return -1



def process(arr = [], first = "", second = "", third = ""):
    # print "first word: " + first + " second word: " + second + " third word: " + third
    first_index = word_check(arr, first)
    # print "first index: " + str(first_index)
    if first_index != -1 :
        second_index = word_check(arr[first_index].next, second)
        # print "second index: " + str(second_index)
        if second_index != -1 :
            third_index = word_check(arr[first_index].next[second_index].next, third)
            # print "third index: " + str(third_index)
            if third_index != -1:
                return arr
            else:
                leaf = Tree()
                leaf.word = third
                arr[first_index].next[second_index].next.append(leaf)
                return arr
        else:
            subroot = Tree()
            subroot.word = second
            leaf = Tree()
            leaf.word = third
            subroot.next.append(leaf)
            arr[first_index].next.append(subroot)
            return arr
    else:
        root = Tree()
        root.word = first
        subroot = Tree()
        subroot.word = second
        leaf = Tree()
        leaf.word = third
        subroot.next.append(leaf)
        root.next.append(subroot)
        arr.append(root)
        return arr

def search_by_prefix(arr, first, second, third = ""):
    for nodeno in range(len(arr)):
        if arr[nodeno].word == first:
            print "first found"
            # print arr[nodeno].next
            for second_nodeno in range(len(arr[nodeno].next)):
                if second == arr[nodeno].next[second_nodeno].word :
                    print "second found"
                    return arr[nodeno].next[second_nodeno].next
    return []



prediction_array = []
root = Tree()
root.word = "Root"
sentences = brown.sents(categories=['news'])
# sample_sentence = "In the example below, you prompt the user to enter some number. Use the int function to enter an number to an integer. Add five to the integer. Then, the str function converts the integer to a string so that Python can concatenate and print out the answer"
# sentence = sample_sentence.split(" ")
# print sentences
for sentence in sentences:
    for iter_arr in range(len(sentence)):
        if iter_arr == 1:
            first = sentence[iter_arr-1]
            second = sentence[iter_arr]
            third = ""
            tree_obj = process(root.next, first, second, third)
            # print tree_obj
            root.next = tree_obj
        else:
            if iter_arr > 1:
                first = sentence[iter_arr-2]
                second = sentence[iter_arr-1]
                third = sentence[iter_arr]
                tree_obj = process(root.next, first, second, third)
                root.next = tree_obj
print len(root.next)
print strftime("%Y-%m-%d %H:%M:%S", gmtime())
prefixes_candidate = search_by_prefix(root.next, "has", "been")
prefix = "a"
print strftime("%Y-%m-%d %H:%M:%S", gmtime())
for obj in prefixes_candidate:
    if obj.word.startswith(prefix):
        prediction_array.append(obj.word)
print prediction_array