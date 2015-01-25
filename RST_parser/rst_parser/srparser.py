
from sqlalchemy.util._collections import OrderedSet
import lesk
from lesk import adapted_lesk, adapted_lesk1, adapted_lesk2, adapted_lesk3
from nltk.corpus import wordnet as wn
from nltk import word_tokenize

""" Shift-reduce parser, including following functions
1, Initialize parsing status given a sequence of texts
2, Change the status according to a specific parsing action
3, Get the status of stack/queue
4, Check whether should stop parsing
- YJ
"""

from datastructure import *
from util import *
import itertools

class SRParser:
    """ It shouldn't be a sub-class of 'object',
        otherwise, it won't work.
        To be clear, being a sub-class of 'object',
        it will make copy of stack and queue, but I
        don't want it works in that way with a purpose.
        - YJ
    """
    def __init__(self, stack, queue):
        """ Initialization
        """
        self.Stack = stack
        self.Queue = queue


    def init(self, texts):
        """ Using text to initialize Queue

        :type texts: list of string
        :param texts: a sequence of EDUs for parsing
        """
        for (idx, text) in enumerate(texts):
            n = idx + 1
            node = SpanNode(prop=None)
            node.text = text
            node.eduspan, node.nucspan = (n, n), (n, n)
            node.nucedu = n
            self.Queue.append(node)


    def operate(self, action_tuple):
        """ According to parsing label to modify the status of
            the Stack/Queue

        Need a special exception for parsing error -YJ

        :type action_tuple: tuple (,,)
        :param action_tuple: one specific parsing action,
                             for example: reduce-NS-elaboration
        """
        action, form, relation = action_tuple
        if action == 'Shift':
            if len(self.Queue) == 0:
                raise ActionError("Shift action with an empty queue")
            node = self.Queue.pop(0)
            self.Stack.append(node)
        elif action == 'Reduce':
            if len(self.Stack) < 2:
                raise ActionError("Reduce action with stack which has less than 2 spans")
            rnode = self.Stack.pop()
            lnode = self.Stack.pop()
            # Create a new node
            # Assign a value to prop, only when it is someone's
            #   children node
            node = SpanNode(prop=None)
            # Children node
            node.lnode, node.rnode = lnode, rnode
            # Parent node of children nodes
            node.lnode.pnode, node.rnode.pnode = node, node
            # Node text
            node.text = lnode.text + " " + rnode.text
            # POS Tag
            node.pos_Text = lnode.pos_Text + " " + rnode.pos_Text
            node.firstPOS = lnode.firstPOS
            node.lastPOS = rnode.lastPOS
            node.slastPOS = rnode.slastPOS
            node.sfirstPOS = lnode.sfirstPOS
            #Head word
            if lnode.ishead == 'True':
                node.ishead = 'True'
                node.headlist = lnode.headlist
                node.headtuple = tuple(set(node.headlist))
            elif rnode.ishead == 'True':
                node.ishead = 'True'
                node.headlist = rnode.headlist
                node.headtuple = tuple(set(node.headlist))
            else:
                node.headlist = lnode.headlist + rnode.headlist
                node.headtuple = tuple(set(node.headlist))
            #Independent part 1- single sense
#             node.senseSingle_list = lnode.senseSingle_list + rnode.senseSingle_list
#             node.senseSingle_tuple =  tuple(set(node.senseSingle_list))
            #Ind- part 2
            zipped = itertools.izip(node.text.split(), node.pos_Text.split())
            filtered = [x[0] for x in zipped if (x[1].lower() == 'nn' or x[1].lower()== 'nns' )]
            if not filtered:
#                 answer = ""
                node.senseSingle_list = []
                node.senseSingle_tuple =  tuple((node.senseSingle_list))
            elif (len(filtered) > 1):
                answer = adapted_lesk2(node.text, filtered)
                node.senseSingle_list = [str(answer).lower()]
                node.senseSingle_tuple =  tuple((node.senseSingle_list))
            else :
                answer = adapted_lesk(node.text,filtered[0])
                node.senseSingle_list = [str(answer).lower()]
                node.senseSingle_tuple =  tuple((node.senseSingle_list))
            #Path Similarity:
            if (lnode.senseSingle_tuple is not None and rnode.senseSingle_tuple is not None):
                try:   
                    if (lnode.senseSingle_tuple[0] and rnode.senseSingle_tuple[0]):
                        left = wn.synset(word_tokenize(lnode.senseSingle_tuple[0])[2].split('\'')[1])
                        right = wn.synset(word_tokenize(rnode.senseSingle_tuple[0])[2].split('\'')[1])
                        temp_int = left.path_similarity(right)
                        lnode.sim_measure = temp_int
                        rnode.sim_measure = temp_int
                        node.sim_measure = temp_int
                except: pass
            # EDU span
            node.eduspan = (lnode.eduspan[0],rnode.eduspan[1])
            # Nuc span / Nuc EDU
            if form == 'NN':
                node.nucspan = (lnode.eduspan[0],rnode.eduspan[1])
                node.nucedu = lnode.nucedu
                node.lnode.prop = "Nucleus"
                node.lnode.relation = relation
                node.rnode.prop = "Nucleus"
                node.rnode.relation = relation
            elif form == 'NS':
                node.nucspan = lnode.eduspan
                node.nucedu = lnode.nucedu
                node.lnode.prop = "Nucleus"
                node.lnode.relation = "span"
                node.rnode.prop = "Satellite"
                node.rnode.relation = relation
            elif form == 'SN':
                node.nucspan = rnode.eduspan
                node.nucedu = rnode.nucedu
                node.lnode.prop = "Satellite"
                node.lnode.relation = relation
                node.rnode.prop = "Nucleus"
                node.rnode.relation = "span"
            else:
                raise ValueError("Unrecognized form: {}".format(form))
            self.Stack.append(node)
            # How about prop? How to update it?
        else:
            raise ValueError("Unrecoginized parsing action: {}".format(action))


    def getstatus(self):
        """ Return the status of the Queue/Stack
        """
        return (self.Stack, self.Queue)


    def endparsing(self):
        """ Whether we should end parsing
        """
        if (len(self.Stack) == 1) and (len(self.Queue) == 0):
            return True
        elif (len(self.Stack) == 0) and (len(self.Queue) == 0):
            raise ParseError("Illegal stack/queue status")
        else:
            return False

    def getparsetree(self):
        """ Get the entire parsing tree
        """
        if (len(self.Stack) == 1) and (len(self.Queue) == 0):
            return self.Stack[0]
        else:
            return None

            
