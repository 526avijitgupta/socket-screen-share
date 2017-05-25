import nltk
import re
import cgi
import cgitb
from nltk.corpus import brown
from pytrie import SortedStringTrie as Trie
import thread
import modules.create_socket as create_socket
import modules.decode_data as decode_data
import modules.handle_client_handshake as handle_client_handshake
from time import gmtime, strftime

HOST = ''
PORT = 4500
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

def search_by_prefix(arr, first, second):
    for nodeno in range(len(arr)):
        if arr[nodeno].word == first:
            print "first found"
            # print arr[nodeno].next
            for second_nodeno in range(len(arr[nodeno].next)):
                if second == arr[nodeno].next[second_nodeno].word :
                    print "second found"
                    return arr[nodeno].next[second_nodeno].next
    return []

def encode_data(data_to_encode):
    # print chardet.detect(data_to_encode)
    resp = bytearray([0b10000001, len(data_to_encode)])
    for d in bytearray(data_to_encode):
        resp.append(d)
    return resp
    # return data_to_encode

def send_to_client(data, conn):
    try:
        conn.sendall(data)
        return 1
    except:
        print("error sending to a client")
        return 0


def new_client(conn, addr, root):
    print len(root.next)
    handle_client_handshake.handle_client_handshake(conn)
    while 1:
        data_recv = conn.recv(4096)
        if not data_recv:
            print "connection closing"
            clients_set.remove(conn)
            files_mapping.pop(conn, 0)
            print "closing this connection"
            conn.close()
            break
        print strftime("%Y-%m-%d %H:%M:%S", gmtime())
        data_from_client = decode_data.decode_data(data_recv)
        split_data = data_from_client.split('&')
        test_sentence = split_data[0].split(" ")
        if len(test_sentence) > 1:
            first_word = test_sentence[0]
            second_word = test_sentence[1]
            prefix = split_data[1]
            print "First Word: " + first_word + " Second word: " + second_word
            print strftime("%Y-%m-%d %H:%M:%S", gmtime())
            prefixes_candidate = search_by_prefix(root.next, first_word, second_word)
            prediction_array = []
            for obj in prefixes_candidate:
                if obj.word.startswith(prefix):
                    prediction_array.append(obj.word)
                    # prediction_options = prediction_options + "&" + obj.word
                    # print prediction_options
            print strftime("%Y-%m-%d %H:%M:%S", gmtime())
            # print prediction_array
            prediction_options = "&".join(prediction_array)
            prediction_options = prediction_options.encode("ascii","ignore")
            send_to_client(encode_data(prediction_options),conn)
    thread.exit()


if __name__ == "__main__":
    root = Tree()
    root.word = "Root"
    sentences = brown.sents()
    # sample_sentence = "In the example below, you prompt the user to enter some number. Use the int function to enter an number to an integer. Add five to the integer. Then, the str function converts the integer to a string so that Python can concatenate and print out the answer"
    # sentence = sample_sentence.split(" ")
    # print sentences
    print "Mapping starts"
    print strftime("%Y-%m-%d %H:%M:%S", gmtime())
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
    print strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print "Mapped corpus successfully"
    clients_set = set()
    files_mapping = {}
    s = create_socket.start_server(HOST, PORT)

    while 1:
        conn, addr = s.accept()
        thread.start_new_thread(new_client, (conn, addr,root,))
