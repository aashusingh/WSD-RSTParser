from itertools import chain
import itertools
from nltk.corpus import wordnet as wn
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
from nltk import word_tokenize, pos_tag
from collections import defaultdict


porter = PorterStemmer()
wnl = WordNetLemmatizer()

def lemmatize(ambiguous_word):
    lemma = wnl.lemmatize(ambiguous_word)
    return lemma

# def get_pos_of_ambiguous_word(context_sentence, ambiguous_word):
#     return {tok.lower():pos for tok, pos in 
#             pos_tag(word_tokenize(context_sentence))}[ambiguous_word][0].lower()

# def compare_overlaps_greedy(context, synsets_signatures):
#     """
#     Calculate overlaps between the context sentence and the synset_signature
#     and returns the synset with the highest overlap.
#     
#     Note: Greedy algorithm only keeps the best sense, see http://goo.gl/OWSfOZ
#     
#     Only used by original_lesk(). Keeping greedy algorithm for documentary sake, 
#     because original_lesks is greedy.
#     """
#     max_overlaps = 0; lesk_sense = None
#     for ss in synsets_signatures:
#         overlaps = set(synsets_signatures[ss]).intersection(context)
#         if len(overlaps) > max_overlaps:
#             lesk_sense = ss
#             max_overlaps = len(overlaps)    
#     return lesk_sense

def compare_overlaps(context, synsets_signatures, \
                     nbest=False, keepscore=False, normalizescore=False):
    """ 
    Calculates overlaps between the context sentence and the synset_signture
    and returns a ranked list of synsets from highest overlap to lowest.
    """
    overlaplen_synsets = [] # a tuple of (len(overlap), synset).
    for ss in synsets_signatures:
        overlaps = set(synsets_signatures[ss]).intersection(context)
#         print synsets_signatures[ss] + [": " , overlaps]
        overlaplen_synsets.append((len(overlaps), ss))
    
    # Rank synsets from highest to lowest overlap.
    ranked_synsets = sorted(overlaplen_synsets, reverse=True)
    
    # Normalize scores such that it's between 0 to 1. 
    if normalizescore:
        total = float(sum(i[0] for i in ranked_synsets))
        ranked_synsets = [(i/total,j) for i,j in ranked_synsets]
      
    if not keepscore: # Returns a list of ranked synsets without scores
        ranked_synsets = [i[1] for i in sorted(overlaplen_synsets, \
                                               reverse=True)]
      
    if nbest: # Returns a ranked list of synsets.
        return ranked_synsets
    else: # Returns only the best sense.
        if not ranked_synsets: return ""
        else:
            return ranked_synsets[0]
        
def compare_overlaps2(context, wordsign_dict, \
                     nbest=False, keepscore=False, normalizescore=False):
    """ 
    
    """
    final_overlap = []
    overlaplen_synsets = []
     
    temp_list = list(itertools.combinations(wordsign_dict.keys(),2))
    keycombo_list = temp_list
    
    for key,item in wordsign_dict.iteritems():
        for ss in item:
            overlaps = set(item[ss]).intersection(context)
            overlaplen_synsets.append((len(overlaps), ss))
            
    for word1, word2 in keycombo_list:
        fsynsets_signatures = wordsign_dict[word1]
        ssynsets_signatures = wordsign_dict[word2]
        for ss in fsynsets_signatures:
                for pp in ssynsets_signatures:
                    overlaps = (set(fsynsets_signatures[ss]).intersection(set(ssynsets_signatures[pp])))
                    overlaplen_synsets.append((len(overlaps), ss))
        
    
    ranked_synsets = sorted(overlaplen_synsets, reverse=True) 
    if ranked_synsets:  
        return ranked_synsets[0]
    else: return []

def compare_overlaps3( wordsign_dict, \
                     nbest=False, keepscore=False, normalizescore=False):
    """ 
    
    """
    final_overlap = []
    overlaplen_synsets = []
     
    temp_list = list(itertools.combinations(wordsign_dict.keys(),2))
    keycombo_list = temp_list
    
               
    for word1, word2 in keycombo_list:
        fsynsets_signatures = wordsign_dict[word1]
        ssynsets_signatures = wordsign_dict[word2]
        for ss in fsynsets_signatures:
                for pp in ssynsets_signatures:
                    overlaps = (set(fsynsets_signatures[ss]).intersection(set(ssynsets_signatures[pp])))
                    overlaplen_synsets.append((len(overlaps), ss))
        
    
    ranked_synsets = sorted(overlaplen_synsets, reverse=True) 
    if ranked_synsets:  
        return ranked_synsets[0]
    else: return []
    
  
    
def compare_overlaps1(synsets_signatures, synsets_signatures1, \
                     nbest=False, keepscore=False, normalizescore=False):
    """ 
    Calculates overlaps between the context sentence and the synset_signture
    and returns a ranked list of synsets from highest overlap to lowest.
    """
    overlaplen_synsets = [] # a tuple of (len(overlap), synset).
    for ss in synsets_signatures:
        for pp in synsets_signatures1:
            overlaps = set(synsets_signatures[ss]).intersection(set(synsets_signatures1[pp]))
#             print synsets_signatures[ss] + [": " , overlaps]
            overlaplen_synsets.append((len(overlaps), ss, pp))
    
    # Rank synsets from highest to lowest overlap.
    ranked_synsets = sorted(overlaplen_synsets, reverse=True)
    
    # Normalize scores such that it's between 0 to 1. 
    if normalizescore:
        total = float(sum(i[0] for i in ranked_synsets))
        ranked_synsets = [(i/total,j) for i,j in ranked_synsets]
      
    if not keepscore: # Returns a list of ranked synsets without scores
        ranked_synsets = [i[1] for i in sorted(overlaplen_synsets, \
                                               reverse=True)]
      
    if nbest: # Returns a ranked list of synsets.
        return ranked_synsets
    else: # Returns only the best sense.
        if not ranked_synsets: return ""
        else:
            return ranked_synsets[0]

def simple_signature(ambiguous_word, pos=None, stem=True, \
                     hyperhypo=True, stop=True):
    """ 
    Returns a synsets_signatures dictionary that includes signature words of a 
    sense from its:
    (i)   definition
    (ii)  example sentences
    (iii) hypernyms and hyponyms
    """
    synsets_signatures = {}
    for ss in wn.synsets(ambiguous_word):
        # If POS is specified.
        try:
            if pos and str(ss.pos()) != pos:
                continue
        except:
            if pos and str(ss.pos) != pos:
                continue
        
        signature = []
        # Includes definition.
        try: signature+= ss.definition().split()
        except: signature+= ss.definition.split()
        # Includes examples
        try: signature+= list(chain(*[i.split() for i in ss.examples()]))
        except: signature+= list(chain(*[i.split() for i in ss.examples]))
        # Includes lemma_names.
        try: signature+= ss.lemma_names()
        except: signature+= ss.lemma_names
        # Optional: includes lemma_names of hypernyms and hyponyms.
        if hyperhypo == True:
            try: signature+= list(chain(*[i.lemma_names() for i \
                                          in ss.hypernyms()+ss.hyponyms()]))
            except: signature+= list(chain(*[i.lemma_names for i \
                                             in ss.hypernyms()+ss.hyponyms()]))
        # Optional: removes stopwords.
        if stop == True:
            signature = [i for i in signature if i not in stopwords.words('english')]    
        # Matching exact words causes sparsity, so optional matching for stems.
#         if stem == True: 
#             signature = [wnl.lemmatize(i) for i in signature]
            templ = []
            for words in signature:
                if( "(" in words or ")" in words):
                    continue
                templ.append(words)
            temp1 = [x.split('(')[1] for x in signature if '(' in x]
            temp2 = [x.split(')')[0] for x in signature if ')' in x]
            signature = templ + temp1 + temp2
        synsets_signatures[ss] = signature
    
    return synsets_signatures


def adapted_lesk(context_sentence, ambiguous_word, \
                pos=None, stem=True, hyperhypo=True, stop=True, \
                nbest=False, keepscore=False, normalizescore=False):
    """
    This function is the implementation of the Adapted Lesk algorithm, 
    described in Banerjee and Pederson (2002). It makes use of the lexical 
    items from semantically related senses within the wordnet 
    hierarchies and to generate more lexical items for each sense. 
    see www.d.umn.edu/~tpederse/Pubs/cicling2002-b.pdf‎
    """
    # Ensure that ambiguous word is a lemma.
    ambiguous_word = wnl.lemmatize(ambiguous_word)
    # Get the signatures for each synset.
    ss_sign = simple_signature(ambiguous_word, pos, stem, hyperhypo)
    signature = []
    for ss in ss_sign:
        related_senses = list(set(ss.member_holonyms() + ss.member_meronyms() + 
                                 ss.part_meronyms() + ss.part_holonyms() + 
                                 ss.similar_tos() + ss.substance_holonyms() + 
                                 ss.substance_meronyms()))
    
        try:
            signature = signature + list([j for j in chain(*[i.lemma_names() for i in \
                      related_senses]) if j not in stopwords.words('english')])
        except:
            signature = signature + list([j for j in chain(*[i.lemma_names for i in \
                      related_senses]) if j not in stopwords.words('english')])
   
    # Matching exact words causes sparsity, so optional matching for stems.
#     if stem == True:
#         signature = [wnl.lemmatize(i) for i in signature]
        ss_sign[ss]+=signature
  
    # Disambiguate the sense in context.
    
    context_sentence = [wnl.lemmatize(i) for i in context_sentence.decode('utf8','ignore').split()]
    best_sense = compare_overlaps(context_sentence, ss_sign, \
                                    nbest=nbest, keepscore=keepscore, \
                                    normalizescore=normalizescore)
    return best_sense


def adapted_lesk1(context_sentence, ambiguous_word, ambiguous_word1, \
                pos=None, stem=True, hyperhypo=True, stop=True, \
                nbest=False, keepscore=False, normalizescore=False):
    ambiguous_word = wnl.lemmatize(ambiguous_word)
    # Get the signatures for each synset.
    ss_sign = simple_signature(ambiguous_word, pos, stem, hyperhypo)
    signature = []
    for ss in ss_sign:
        related_senses = list(set(ss.member_holonyms() + ss.member_meronyms() + 
                                 ss.part_meronyms() + ss.part_holonyms() + 
                                 ss.similar_tos() + ss.substance_holonyms() + 
                                 ss.substance_meronyms()))
    
        try:
            signature = signature + list([j for j in chain(*[i.lemma_names() for i in \
                      related_senses]) if j not in stopwords.words('english')])
        except:
            signature = signature + list([j for j in chain(*[i.lemma_names for i in \
                      related_senses]) if j not in stopwords.words('english')])
    ss_sign[ss]+=signature
    
    ambiguous_word1 = wnl.lemmatize(ambiguous_word1)
    ss_sign1 = simple_signature(ambiguous_word1, pos, stem, hyperhypo)
    signature = []
    for ss in ss_sign1:
        related_senses = list(set(ss.member_holonyms() + ss.member_meronyms() + 
                                 ss.part_meronyms() + ss.part_holonyms() + 
                                 ss.similar_tos() + ss.substance_holonyms() + 
                                 ss.substance_meronyms()))
    
        try:
            signature = signature + list([j for j in chain(*[i.lemma_names() for i in \
                      related_senses]) if j not in stopwords.words('english')])
        except:
            signature = signature + list([j for j in chain(*[i.lemma_names for i in \
                      related_senses]) if j not in stopwords.words('english')])
    ss_sign1[ss]+=signature
    
    best_sense = compare_overlaps1(ss_sign, ss_sign1, \
                                    nbest=nbest, keepscore=keepscore, \
                                    normalizescore=normalizescore)
    return best_sense
 
    
def adapted_lesk2(context_sentence, ambiguous_list, pos=None, stem=True, hyperhypo=True, stop=True, \
                nbest=False, keepscore=False, normalizescore=False):
    context_sentence = [wnl.lemmatize(i) for i in context_sentence.decode('utf8','ignore').split()]
    wordsign_dict = defaultdict()
    for word in ambiguous_list:
        ambiguous_word = wnl.lemmatize(word)
        ss_sign = simple_signature(ambiguous_word, pos, stem, hyperhypo)
        # Get the signatures for each synset.
        signature = []
        for ss in ss_sign:
            related_senses = list(set(ss.member_holonyms() + ss.member_meronyms() + 
                                 ss.part_meronyms() + ss.part_holonyms() + 
                                 ss.similar_tos() + ss.substance_holonyms() + 
                                 ss.substance_meronyms()))
    
            try:
                signature = signature + list([j for j in chain(*[i.lemma_names() for i in \
                      related_senses]) if j not in stopwords.words('english')])
            except:
                signature = signature + list([j for j in chain(*[i.lemma_names for i in \
                      related_senses]) if j not in stopwords.words('english')])
   
    # Matching exact words causes sparsity, so optional matching for stems.
#     if stem == True:
#         signature = [wnl.lemmatize(i) for i in signature]
            ss_sign[ss]+=signature
  
    # Disambiguate the sense in context.
    
        wordsign_dict[ambiguous_word] = ss_sign
            
    best_sense = compare_overlaps2(context_sentence, wordsign_dict, \
                                    nbest=nbest, keepscore=keepscore, \
                                    normalizescore=normalizescore)
    if(best_sense):
        return str(best_sense[1])
    else:
        return ""
        
        
def adapted_lesk3(context_sentence, pos=None, stem=True, hyperhypo=True, stop=True, \
                nbest=False, keepscore=False, normalizescore=False):
    context_sentence = [wnl.lemmatize(i) for i in context_sentence.decode('utf8','ignore').split()]
    tlist = [ x for x in context_sentence if x.isalpha()]
    wordsign_dict = defaultdict()
    for word in tlist:
        ambiguous_word = (word)
        ss_sign = simple_signature(ambiguous_word, pos, stem, hyperhypo)
        # Get the signatures for each synset.
        signature = []
        for ss in ss_sign:
            related_senses = list(set(ss.member_holonyms() + ss.member_meronyms() + 
                                 ss.part_meronyms() + ss.part_holonyms() + 
                                 ss.similar_tos() + ss.substance_holonyms() + 
                                 ss.substance_meronyms()))
    
            try:
                signature = signature + list([j for j in chain(*[i.lemma_names() for i in \
                      related_senses]) if j not in stopwords.words('english')])
            except:
                signature = signature + list([j for j in chain(*[i.lemma_names for i in \
                      related_senses]) if j not in stopwords.words('english')])
   
    # Matching exact words causes sparsity, so optional matching for stems.
#     if stem == True:
#         signature = [wnl.lemmatize(i) for i in signature]
            ss_sign[ss]+=signature
  
    # Disambiguate the sense in context.
    
        wordsign_dict[ambiguous_word] = ss_sign
            
    best_sense = compare_overlaps2(context_sentence, wordsign_dict, \
                                    nbest=nbest, keepscore=keepscore, \
                                    normalizescore=normalizescore)
    if(best_sense):
        return str(best_sense[1])
    else:
        return ""
               
        

    
    
    
    
    
    


