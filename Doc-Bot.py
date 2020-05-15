import string
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords 
from nltk.stem import WordNetLemmatizer
import re
import string
import sqlite3
import random
from collections import Counter
from string import punctuation
from math import sqrt

#%run Codefile
#%run Training_system
#%run Search 
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "hi there", "hello", "I am glad! You are talking to me"]

import mysql.connector
connection=mysql.connector.connect(user='yash',host="localhost",database="test",password='Password')
cursor=connection.cursor()
cursor.execute("create table IF NOT EXISTS work(question VARCHAR(1000) NOT NULL,answer VARCHAR(1000) NOT NULL,id int auto_increment primary key)")
connection.commit();
connection.close();
stopwords = nltk.corpus.stopwords.words('english')
stopwords.extend(string.punctuation)
stopwords.append('')

def get_wordnet_pos(pos_tag):
    if pos_tag[1].startswith('J'):
        return (pos_tag[0], wordnet.ADJ)
    elif pos_tag[1].startswith('V'):
        return (pos_tag[0], wordnet.VERB)
    elif pos_tag[1].startswith('N'):
        return (pos_tag[0], wordnet.NOUN)
    elif pos_tag[1].startswith('R'):
        return (pos_tag[0], wordnet.ADV)
    else:
        return (pos_tag[0], wordnet.NOUN)

# Create tokenizer and stemmer

lemmatizer =  nltk.stem.WordNetLemmatizer()

def is_ci_lemma_stopword_set_match(a, b, threshold=0.5):
    """Check if a and b are matches."""
    pos_a = map(get_wordnet_pos, nltk.pos_tag(word_tokenize(a)))
    pos_b = map(get_wordnet_pos, nltk.pos_tag(word_tokenize(b)))
    lemmae_a = [lemmatizer.lemmatize(token.lower().strip(string.punctuation), pos) for token, pos in pos_a \
                    if pos == wordnet.NOUN and token.lower().strip(string.punctuation) not in stopwords]
    lemmae_b = [lemmatizer.lemmatize(token.lower().strip(string.punctuation), pos) for token, pos in pos_b \
                    if pos == wordnet.NOUN and token.lower().strip(string.punctuation) not in stopwords]
    
   
    
    # Calculate Jaccard similarity
    if(float(len(set(lemmae_a).union(lemmae_b)))!=0):
        ratio = len(set(lemmae_a).intersection(lemmae_b)) / float(len(set(lemmae_a).union(lemmae_b)))
    else:
        ratio=0.0
    
    return ratio*100

class mdict(dict):
    def __setitem__(self, key, value):
        """add the given value to the list of values for this key"""
        self.setdefault(key, []).append(value)


def start():
    flag=True;
    question=""
    
    answer_of_query=""
    while(flag==True):
        question=input("User Query:")
        question=question.strip()
        question=question.lower()
        if(question!="bye" and greeting(question)==None and question!="exit"):
#            punctuation_removed_question=cs.remove_punctuation(question)
            most_favourable_item_id=int(find_most_favourable_answer(question))
            if(most_favourable_item_id!=0):
                answer_of_query=finding_answer(most_favourable_item_id)
                print("DOCTOR-BOT: "+answer_of_query)
            else:
                print("DOCTOR-BOT: Unable to Find the answer, will get back to you soon")
        else:
            if(greeting(question)!=None):
                print("DOCTOR-BOT: "+greeting(question))
            else:
                print("DOCTOR-BOT: bye, Take care")
                flag=False
def train_system():
    flag=True;
    question=""
    answer=""
    while(flag==True):
        question=input("Admin Question:")
        question=question.strip()
        question=question.lower()
        if(question!="" and question!="bye" and question!="exit"):
            answer=input("Admin Answer:")
            answer=answer.strip()
#            punctuation_removed_question=cs.remove_punctuation(question)
#            cs.get_synonyms(punctuation_removed_question)
#            synonyms=mdict()
#            synonyms=cs.get_synonyms(punctuation_removed_question)
#            cs.generate_sentence_from_question(synonyms)
#            lemmantized_question=cs.sentence_lemmmantizer(punctuation_removed_question)
            save_responses_to_database(question,answer)
            print("Responses saved successfully")
            
        else:
            print("DOCTOR-BOT: Wrong Responses Sir")
            return
class mdict(dict):

    def __setitem__(self, key, value):
        """add the given value to the list of values for this key"""
        self.setdefault(key, []).append(value)
def tokenize_sentence(question):
    return sent_tokenize(question)

def tokenize_words(question):
    return word_tokenize(question)

def remove_punctuation(question):
    
    tokens = [t for t in question.split()] 
    clean_tokens=tokens[:]
    for token in tokens:
        if token in stopwords.words('english'):
             clean_tokens.remove(token)
    string_of_words=""
    for words in clean_tokens:
        string_of_words=string_of_words+' '+words
    return string_of_words

def get_synonyms(question):
    words=tokenize_words(question) 
    synonyms=mdict();
    for word in words:
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonyms[word]=lemma.name()
                  
    return synonyms
#def generate_sentence_from_question(synonyms):
#    list1=list(synonyms.keys())
#    length1=len(list1)
#    list3=[""]
#    str1=""
#    for word  in list1:
#           list2=list(synonyms[word])
#           i=0
#           for word2 in list2:
#               str1=list3[i]+word2+" "
#               list3[i]=str1
#               i=i+1
#    print(list3)
#    sentences=[""]
#    for word in list1:
#        for word1 in synonyms.values(word):
#            print(word1)    

def sentence_lemmmantizer(question):
    lemmer = nltk.stem.WordNetLemmatizer()
    tokens=tokenize_words(question)
    
    str1=""
    wording=""
    for tok in tokens:
        wording=lemmer.lemmatize(tok)
        str1=str1+' '+wording
        
    return(str1)
    
def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

def save_responses_to_database(question,answer):
    
    insert_stmt = ("INSERT INTO work (question,answer) " "VALUES (%s, %s)")
    data=(question,answer)
    connection=mysql.connector.connect(user='yash',host="localhost",database="test",password='Password')
    cursor=connection.cursor()
    
    cursor.execute(insert_stmt,data)
    connection.commit()
    connection.close()
    return
    
def find_most_favourable_answer(question):
    itemming=dict()
    itemming1=dict()
    most_favourable_item_id=0
    insert_stmt = ("select question,id from work")
    connection=mysql.connector.connect(user='yash',host="localhost",database="test",password='Password')
    cursor=connection.cursor()
    cursor.execute(insert_stmt)
    question_list=cursor.fetchall()
    for row in question_list:
        itemming1[row[0]]=row[1]
    
    
    connection.close()
    string=""
    for list1 in question_list:
        string=str(list1[0])
        
        
        ratio=is_ci_lemma_stopword_set_match(question,string)
        itemming[string]=float(ratio)
    list_of_keys=itemming.keys()
    most_favourable_item=0.0
    for name1 in list_of_keys:
        if(most_favourable_item<=float(itemming[name1])):
            most_favourable_item=float(itemming[name1])
            most_favourable_item_name=name1
   
    for list2 in question_list:
        if(most_favourable_item_name==list2[0]):
            if(most_favourable_item>10.0 and most_favourable_item<=100.0):
                most_favourable_item_id=int(list2[1])
            else:
                most_favourable_item_id=0
            
    
    return most_favourable_item_id
    
def finding_answer(most_favourable_item_id):
    connection=mysql.connector.connect(user='yash',host="localhost",database="test",password='Password')
    cursor=connection.cursor()
    insert_stmt = ()
    cursor.execute("select answer from work where id = %s"% (most_favourable_item_id))
    answer=cursor.fetchone()
    for ans in answer:
        correct_ans=str(ans)
    connection.close()
    return correct_ans

print("Hello User I'm DOCTOR-BOT Your chatbot")
class mdict(dict):
    def __setitem__(self, key, value):
        """add the given value to the list of values for this key"""
        self.setdefault(key, []).append(value)



            
            
if __name__=="__main__":
         
   
    valid_response=""
    while True:
    
        print("Do you want to train or search")
        valid_response=input("User:")
        valid_response=valid_response.strip()
        valid_response=valid_response.lower()
        
        if(valid_response=="train"):
            train_system()
        else:
            if(valid_response=="search"):
                start()
            else:
                if(greeting(valid_response)!=None):
                   print("DOCTOR-BOT: "+greeting(valid_response))
                else:
                    print("DOCTOR-BOT: Bye")
                    break
