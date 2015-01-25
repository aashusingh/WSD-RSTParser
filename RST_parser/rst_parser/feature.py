
from nltk.tokenize import word_tokenize
import nltk
from nltk.tag.stanford import POSTagger
import os
from numpy.core.defchararray import isalpha

def myround(x, base=10):
        return int(base * round(float(x)/base))

class FeatureGenerator(object):
    def __init__(self, stack, queue, doclen=None):
        """ Initialization of feature generator

        :type stack: list
        :param stack: list of SpanNode instance

        :type queue: list
        :param queue: list of SpanNode instance

        :type doclen: int
        :param doclen: document length wrt EDUs
        """
        # Stack
        if len(stack) >= 2:
            self.stackspan1 = stack[-1] # Top-1st on stack
            self.stackspan2 = stack[-2] # Top-2rd on stack
        elif len(stack) == 1:
            self.stackspan1 = stack[-1]
            self.stackspan2 = None
        else:
            self.stackspan1, self.stackspan2 = None, None
        # Queue
        if len(queue) > 0:
            self.queuespan1 = queue[0] # First in queue
        else:
            self.queuespan1 = None
        # Document length
        self.doclen = doclen


    def features(self):
        """ Main function to generate features

        1, if you add any argument to this function, remember
           to give it a default value
        2, if you add any sub-function for feature generation,
           remember to call the sub-function here
        """
        features = []
        # Status features
        for feat in self.status_features():
            features.append(feat)
        # Structural features
        for feat in self.structural_features():
            features.append(feat)
            # Lexical features
        for feat in self.lexical_features():
            features.append(feat)
        return features
    

    def structural_features(self):
        """ Structural features
        """
        features = []
        if self.stackspan1 is not None:
            # Span Length wrt EDUs
            features.append(('StackSpan1','Length-EDU',self.stackspan1.eduspan[1]-self.stackspan1.eduspan[0]+1))
            # Distance to the beginning of the document wrt EDUs
            features.append(('StackSpan1','Distance-To-Begin',self.stackspan1.eduspan[0]))
            # Distance to the end of the document wrt EDUs
            if self.doclen is not None:
                features.append(('StackSpan1','Distance-To-End',self.doclen-self.stackspan1.eduspan[1]))
        if self.stackspan2 is not None:
            features.append(('StackSpan2','Length-EDU',self.stackspan2.eduspan[1]-self.stackspan2.eduspan[0]+1))
            features.append(('StackSpan2','Distance-To-Begin',self.stackspan2.eduspan[0]))
            if self.doclen is not None:
                features.append(('StackSpan2','Distance-To-End',self.doclen-self.stackspan2.eduspan[1]))
        if self.queuespan1 is not None:
            features.append(('QueueSpan1','Distance-To-Begin',self.queuespan1.eduspan[0]))
        # Should include some features about the nucleus EDU
        for feat in features:
            yield feat
        

    def status_features(self):
        """ Features related to stack/queue status
        """
        features = []
        if (self.stackspan1 is None) and (self.stackspan2 is None):
            features.append(('Empty-Stack'))
        elif (self.stackspan1 is not None) and (self.stackspan2 is None):
            features.append(('One-Elem-Stack'))
        elif (self.stackspan1 is not None) and (self.stackspan2 is not None):
            features.append(('More-Elem-Stack'))
        else:
            raise ValueError("Unrecognized status in stack")
        if self.queuespan1 is None:
            features.append(('Empty-Queue'))
        else:
            features.append(('NonEmpty-Queue'))
        for feat in features:
            yield feat
    
    

    def lexical_features(self):
        """ Lexical features
        """
        java_path = "C:/Program Files/Java/jdk1.8.0_20/bin/java.exe"
        os.environ['JAVAHOME'] = java_path
        features = []
        if (self.stackspan1 is not None):
            words = word_tokenize(self.stackspan1.text.lower())
            features.append(('FirstWordStack1', words[0]))
            features.append(('EndWordStack1', words[-1]))
            if (len(words) >= 2 ):
                if( not words[0].isalpha()):
                    features.append(('AFirstWordStack1', words[1]))
                if( not words[-1].isalpha()):
                    features.append(('ZEndWordStack1', words[-2])) 
                    
            if (self.queuespan1 is not None):
                queue_words = word_tokenize(self.queuespan1.text.lower())
                features.append(('FirstWord-Stack1-Queue1', words[0], queue_words[0]))
                features.append(('FirstLastWord-Stack1-Queue1', words[0], queue_words[-1]))
                features.append(('LastFirstWord-Stack1-Queue1', words[-1], queue_words[0]))
                features.append(('EndWord-Stack1-Queue1', words[-1], queue_words[-1]))
                if( not queue_words[-1].isalpha() and len(queue_words) >= 2):
                    features.append(('ZFirstLastWord-Stack1-Queue1', words[0], queue_words[-2]))
                    if(not words[-1].isalpha() and len(words) >= 2):
                        features.append(('ZLastFirstWord-Stack1-Queue1', words[-2], queue_words[0]))
                        features.append(('ZEndWord-Stack1-Queue1', words[-2], queue_words[-2]))
           
            if (self.stackspan2 is not None):
                words2 = word_tokenize(self.stackspan2.text.lower())
                features.append(('FirstWord-Stack2-Stack1', words[0], words2[0]))
                features.append(('FirstLastWord-Stack2-Stack1', words[0], words2[-1]))
                features.append(('LastFirstWord-Stack2-Stack1', words[-1], words2[0]))
                features.append(('EndWord-Stack2-Stack1', words[-1], words2[-1]))
                if(not words2[-1].isalpha() and len(words2) >= 2):
                    features.append(('ZFirstLastWord-Stack2-Stack1', words[0], words2[-2]))
                    if(not words[-1].isalpha() and len(words) >= 2):
                        features.append(('ZLastFirstWord-Stack2-Stack1', words[-2], words2[0]))
                        features.append(('ZEndWord-Stack2-Stack1', words[-2], words2[-2]))
       
        if (self.queuespan1 is not None):
            queue_words = word_tokenize(self.queuespan1.text.lower())
            features.append(('FirstWordQueue1', queue_words[0]))
            features.append(('EndWordQueue1', queue_words[-1]))  
            if(len(queue_words) >= 2 ):
                if( not queue_words[0].isalpha()):
                    features.append(('AFirstWordQueue1', queue_words[1]))
                if( not queue_words[-1].isalpha()):
                    features.append(('ZEndWordQueue1', queue_words[-2])) 
                    
        if (self.stackspan2 is not None):
            words2 = word_tokenize(self.stackspan2.text.lower())
            features.append(('FirstWordStack2', words2[0]))
            features.append(('EndWordStack2', words2[-1]))
            if (len(words2) >= 2 ):
                if( not words2[0].isalpha()):
                    features.append(('AFirstWordStack2', words2[1]))
                if( not words2[-1].isalpha()):
                    features.append(('ZEndWordStack2', words2[-2])) 
                    
                
        if (self.stackspan1 is not None):
            features.append(('EndPOSStack1', self.stackspan1.lastPOS))
            features.append(('FirstPOSStack1', self.stackspan1.firstPOS))
            if ( not self.stackspan1.lastPOS.isalpha()):
                features.append(('EndPOSStack1', self.stackspan1.slastPOS))
            if( not self.stackspan1.firstPOS.isalpha()):
                features.append(('AFirstPOSStack1', self.stackspan1.sfirstPOS))

        if (self.queuespan1 is not None):
            features.append(('EndPOSQueue1', self.queuespan1.lastPOS))
            features.append(('FirstPOSQueue1', self.queuespan1.firstPOS))
            if( not self.queuespan1.lastPOS.isalpha()):
                features.append(('ZEndPOSQueue1', self.queuespan1.slastPOS))
#             else:
            if( not self.queuespan1.firstPOS.isalpha()):
                features.append(('AFirstPOSQueue1', self.queuespan1.sfirstPOS))
#             else:
                
            
        if (self.stackspan2 is not None ):
            features.append(('EndPOSStack2', self.stackspan2.lastPOS))
            features.append(('FirstPOSStack2', self.stackspan2.firstPOS))
            if( not self.stackspan2.firstPOS.isalpha()):
                features.append(('AFirstPOSStack2', self.stackspan2.sfirstPOS))
#             else:
            if (not self.stackspan2.lastPOS.isalpha() ):
                features.append(('ZEndPOSStack2', self.stackspan2.slastPOS)) 
#             else:   
             
        if(self.stackspan1 is not None and ( self.stackspan1.senseSingle_tuple)):
            features.append(('SenseSetStack1', self.stackspan1.senseSingle_tuple))
        if(self.stackspan2 is not None and ( self.stackspan2.senseSingle_tuple)):
            features.append(('SenseSetStack2', self.stackspan2.senseSingle_tuple))
        if(self.queuespan1 is not None and ( self.queuespan1.senseSingle_tuple)):
            features.append(('SenseSetQueue1', self.queuespan1.senseSingle_tuple))
            
                                    
        if(self.stackspan1 is not None and ( self.stackspan1.headtuple)):
            if self.stackspan1.ishead == 'True':
                features.append(('HeadSetStack1', self.stackspan1.headtuple))
            else:
                features.append(('NHeadSetStack1', self.stackspan1.headtuple))

        if(self.stackspan2 is not None and (self.stackspan2.headtuple)):
            if self.stackspan2.ishead == 'True':
                features.append(('HeadSetStack2', self.stackspan2.headtuple))
            else:
                features.append(('NHeadSetStack2', self.stackspan2.headtuple))
        if(self.queuespan1 is not None and (self.queuespan1.headtuple)):
            if self.queuespan1.ishead == 'True':
                features.append(('HeadSetQueue1', self.queuespan1.headtuple))
            else:
                features.append(('NHeadSetQueue1', self.queuespan1.headtuple))
                   
        #Path Similarity
        if(self.stackspan1 is not None and self.stackspan1.sim_measure is not None and self.stackspan1.sim_measure<= 1):
            temp_no = myround(self.stackspan1.sim_measure*100, 10)
            features.append((str(temp_no), self.stackspan1.senseSingle_tuple))
               
        if(self.stackspan2 is not None and self.stackspan2.sim_measure is not None and self.stackspan2.sim_measure <= 1):
            temp_no1 = myround(self.stackspan2.sim_measure*100, 10)
            features.append((str(temp_no1), self.stackspan2.senseSingle_tuple))
               
        if(self.queuespan1 is not None and self.queuespan1.sim_measure  is not None and self.queuespan1.sim_measure <= 1):
            temp_no2 = myround(self.queuespan1.sim_measure*100, 10)
            features.append((str(temp_no2), self.queuespan1.senseSingle_tuple))
   
                  
        for feat in features:
            yield feat


        
            
        
