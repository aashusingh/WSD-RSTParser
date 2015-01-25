import nltk
import os

count = 0
countlist = []
countlist1 = []
for dirpath, dnames, fnames in os.walk("test_data"):
    print "here"
    for f in fnames:
        count = 0
        if f.endswith('.myedus'):
            with open("test_data\\" + f)as fin:
                s = f.split('.')[:-1]
                f_name = '.'.join((str(e) for e in s))
                with open("test_data\\" + f_name+ ".pos") as fin1:
                    text = fin1.read()
                    ' '.join(text.split())
                    count = text.split('\t')
                    with open("test_data\\"+ f_name+ ".mypos", 'a') as fin2:
                        prev_count = 0
                        for fin_line in fin:
                            fin_list = fin_line.split()
                            fin_count = len(fin_list)
                            final_count = fin_count+prev_count
                            temp_list = count[prev_count:(final_count)]
                            temp_str = " ".join(str(e) for e in temp_list)
                            fin2.write(temp_str + '\n')
                            prev_count = final_count
                    
                    


    
