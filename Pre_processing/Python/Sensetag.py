import nltk
import os
import itertools
from lesk1.py import adapted_lesk, adapted_lesk2, adapted_lesk3
from numpy.core.defchararray import isalpha

count = 0
# countlist = []
# countlist1 = []
for dirpath, dnames, fnames in os.walk("test_data\\"):
#     print "here"
    for f in fnames:
        count = 0
        if f.endswith('.myedus'):
            with open("test_data\\" + f)as fin:
                s = f.split('.')[:-1]
                f_name = '.'.join((str(e) for e in s))
                with open("test_data\\" + f_name+ ".mypos") as fin1:
                    with open("test_data\\"+ f_name+ ".myindpart3", 'a') as fin2:
                        print f_name
                        for fin1_line in fin1:
                            fin1_list = (fin1_line.split())
                            prev_count = 0
                            fin_line =  fin.readline()
                            fin_list = fin_line.split()
                            zipped = itertools.izip(fin_list, fin1_list)
                            filter = [x[0] for x in zipped if (x[1] == 'NN' or x[1] == 'NNS')]
                            if not filter:
                                answer = adapted_lesk3(fin_line)
                            elif (len(filter) > 1):
                                answer = adapted_lesk2(fin_line, filter)
                            else :
                                answer = adapted_lesk(fin_line,filter[0])
#                             print str(answer)
                            fin2.write(str(answer)+"\n")
#                             else:
#                                 answer = adapted_lesk1(fin_line,'capital', 'market')
#                             fin_count = len(fin_list)
#                             final_count = fin_count+prev_count
#                             temp_list = count[prev_count:(final_count)]
#                             temp_str = " ".join(str(e) for e in temp_list)
#                             fin2.write(temp_str + '\n')
#                             prev_count = final_count
                    
                    