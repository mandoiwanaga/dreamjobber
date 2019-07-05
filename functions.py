import pandas as pd
import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import numpy as np
import nltk

from gensim.models.coherencemodel import CoherenceModel
from gensim.models.ldamodel import LdaModel
from gensim.corpora.dictionary import Dictionary



with open(‘.secrets/mongodb_credentials.txt’, ‘r’) as f:
    conn_string = f.read().strip()

mc = pymongo.MongoClient(conn_string)
jobrec_db = mc[‘job_recommendation_db’]
user_coll = jobrec_db[‘user_collection’]





def lemmatize_stemming(text):
    """Return lemmetized and stemmed text"""
    stemmer = SnowballStemmer('english')
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))


def preprocess(text):
    result = []
    stopwords = ['a',
         'about',
         'above',
         'across',
         'accredited',
         'affirmative',
         'after',
         'afterwards',
         'again',
         'against',
         'age',
         'agency',
         'all',
         'almost',
         'alone',
         'along',
         'already',
         'also',
         'although',
         'always',
         'am',
         'among',
         'amongst',
         'amoungst',
         'amount',
         'an',
         'and',
         'another',
         'any',
         'anyhow',
         'anyone',
         'anything',
         'anyway',
         'anywhere',
         'apply',
         'application',
         'applications',
         'applicant',
         'applicants',
         'are',
         'around',
         'as',
         'at',
         'bachelor',
         'bachelors',
         "bachelor's",
         'be',
         'became',
         'because',
         'become',
         'becomes',
         'becoming',
         'been',
         'before',
         'beforehand',
         'behind',
         'being',
         'below',
         'benefit',
         'benefits',
         'beside',
         'besides',
         'between',
         'beyond',
         'bill',
         'both',
         'bonus',
         'bottom',
         'but',
         'by',
         'call',
         'can',
         'candid',
         'candidates',
         'candidate',
         'cannot',
         'cant',
         'card',
         'career',
         'certificate',
         'certification',
         'ciber',
         'ciber',
         'cisco',
         'citizen',
         'citizenship',
         'click',
         'client',
         'co',
         'college',
         'color',
         'com',
         'company',
         'compensation',
         'computer',
         'con',
         'consultnet',
         'contract',
         'could',
         'couldnt',
         'country',
         'cry',
         'cybercoder',
         'cybercoders',
         'de',
         'degree',
         'dental',
         'describe',
         'description',
         'detail',
         'did',
         'didn',
         'diploma',
         'direct',
         'disability',
         'do',
         'does',
         'doesn',
         'doing',
         'don',
         'done',
         'down',
         'due',
         'duration',
         'during',
         'each',
         'east',
         'education',
         'eg',
         'eight',
         'either',
         'eleven',
         'eliassen',
         'eligible',
         'eligibility',
         'else',
         'elsewhere',
         'email',
         'employ',
         'employees',
         'employee',
         'employer',
         'employment',
         'empty',
         'enough',
         'equal',
         'etc',
         'even',
         'ever',
         'every',
         'everyone',
         'everything',
         'everywhere',
         'except',
         'experience',
         'experiences',
         'experienced',
         'experienced',
         'experience',
         'fahrenheit',
         'federal',
         'few',
         'fico',
         'fifteen',
         'fifty',
         'fill',
         'find',
         'fire',
         'first',
         'five',
         'for',
         'former',
         'formerly',
         'forty',
         'found',
         'four',
         'from',
         'full',
         'fulltime',
         'further',
         'gender',
         'get',
         'give',
         'global',
         'go',
         'govern',
         'government',
         'green',
         'greencard',
         'had',
         'half',
         'has',
         'hasnt',
         'have',
         'he',
         'hence',
         'her',
         'here',
         'hereafter',
         'hereby',
         'herein',
         'hereupon',
         'hers',
         'herself',
         'him',
         'himself',
         'hire',
         'hired',
         'his',
         'how',
         'however',
         'hour',
         'hours',
         'hundred',
         'i',
         'identity',
         'ie',
         'if',
         'immediate',
         'immediately',
         'in',
         'inc',
         'include',
         'indeed',
         'insurance',
         'interest',
         'into',
         'is',
         'it',
         'its',
         'itself',
         'jobs',
         'job',
         'just',
         'keep',
         'kg',
         'km',
         'last',
         'latter',
         'latterly',
         'law',
         'least',
         'less',
         'life',
         'linkedin',
         'ltd',
         'local',
         'location',
         'made',
         'make',
         'many',
         'master',
         'masters',
         "master's",
         'may',
         'me',
         'meanwhile',
         'medical',
         'might',
         'mill',
         'mine',
         'minimum',
         'nminimum',
         'month',
         'months',
         'monthly',
         'more',
         'moreover',
         'most',
         'mostly',
         'move',
         'much',
         'must',
         'my',
         'myself',
         'name',
         'namely',
         'nation',
         'national',
         'needs',
         'need',
         'neither',
         'never',
         'nevertheless',
         'next',
         'nine',
         'nkforce',
         'no',
         'nobody',
         'none',
         'noone',
         'nor',
         'north',
         'not',
         'nothing',
         'now',
         'nowhere',
         'of',
         'off',
         'offer',
         'often',
         'on',
         'once',
         'one',
         'only',
         'onto',
         'opportunity',
         'or',
         'oracle',
         'other',
         'others',
         'otherwise',
         'our',
         'ours',
         'ourselves',
         'out',
         'over',
         'own',
         'part',
         'pay',
         'payroll',
         'per',
         'perhaps',
         'permanent',
         'phd',
         'please',
         'position',
         'pregnancy',
         'pregnant',
         'preferred',
         'protect',
         'put',
         'qualification',
         'qualifications',
         'qualify',
         'quite',
         'race',
         'rather',
         're',
         'really',
         'refer',
         'referral',
         'regarding',
         'reimbursement',
         'reimburse',
         'religion',
         'require',
         'requires',
         'required',
         'nrequired',
         'requirement',
         'recruiter',
         'recruit',
         'resume',
         'rights',
         'right',
         'robert',
         'salesforce',
         'same',
         'sap',
         'say',
         'school',
         'see',
         'seem',
         'seemed',
         'seeming',
         'seems',
         'senior',
         'serious',
         'several',
         'sex',
         'sexual',
         'she',
         'should',
         'show',
         'side',
         'since',
         'sincere',
         'six',
         'sixty',
         'skill',
         'skills',
         'so',
         'some',
         'somehow',
         'someone',
         'something',
         'sometime',
         'sometimes',
         'somewhere',
         'south',
         'staff',
         'state',
         'states',
         'still',
         'such',
         'summary',
         'system',
         'take',
         'tek',
         'teksystems',
         'teksystem',
         'teksystems',
         'teksystem',
         'teksystems:',
         'ten',
         'than',
         'that',
         'the',
         'their',
         'them',
         'themselves',
         'then',
         'thence',
         'there',
         'thereafter',
         'thereby',
         'therefore',
         'therein',
         'thereupon',
         'these',
         'they',
         'thick',
         'thin',
         'third',
         'this',
         'those',
         'though',
         'three',
         'through',
         'throughout',
         'thru',
         'thus',
         'to',
         'together',
         'too',
         'top',
         'toward',
         'towards',
         'transfer',
         'twelve',
         'twenty',
         'two',
         'un',
         'under',
         'unless',
         'until',
         'up',
         'upon',
         'us',
         'used',
         'using',
         'various',
         'very',
         'veteran',
         'via',
         'vision',
         'was',
         'we',
         'well',
         'were',
         'west',
         'what',
         'whatever',
         'when',
         'whence',
         'whenever',
         'where',
         'whereafter',
         'whereas',
         'whereby',
         'wherein',
         'whereupon',
         'wherever',
         'whether',
         'which',
         'while',
         'whither',
         'who',
         'whoever',
         'whole',
         'whom',
         'whose',
         'why',
         'will',
         'with',
         'within',
         'without',
         'world',
         'would',
         'www',
         'year',
         'years',
         'yet',
         'you',
         'your',
         'yours',
         'yourself',
         'yourselves',
         'new',
         'york',
         'los',
         'angeles',
         'chicago',
         'houston',
         'philadelphia',
         'phoenix',
         'san',
         'antonio',
         'san',
         'diego',
         'dallas',
         'san',
         'jose',
         'austin',
         'jacksonville',
         'san',
         'francisco',
         'indianapolis',
         'columbus',
         'fort',
         'worth',
         'charlotte',
         'seattle',
         'denver',
         'el',
         'paso',
         'detroit',
         'washington',
         'boston',
         'memphis',
         'nashville',
         'portland',
         'oklahoma',
         'city',
         'las',
         'vegas',
         'baltimore',
         'louisville',
         'milwaukee',
         'albuquerque',
         'tucson',
         'fresno',
         'sacramento',
         'kansas',
         'city',
         'long',
         'beach',
         'mesa',
         'atlanta',
         'colorado',
         'springs',
         'virginia',
         'beach',
         'raleigh',
         'omaha',
         'miami',
         'oakland',
         'minneapolis',
         'tulsa',
         'wichita',
         'new',
         'orleans',
         'arlington',
         'alabama',
         'alaska',
         'arizona',
         'arkansas',
         'california',
         'colorado',
         'connecticut',
         'delaware',
         'florida',
         'georgia',
         'hawaii',
         'idaho',
         'illinois',
         'indiana',
         'iowa',
         'kansas',
         'kentucky',
         'louisiana',
         'maine',
         'maryland',
         'massachusetts',
         'miami',
         'michigan',
         'minnesota',
         'mississippi',
         'missouri',
         'montana',
         'nebraska',
         'nevada',
         'new',
         'hampshire',
         'new',
         'jersey',
         'new',
         'mexico',
         'new',
         'york',
         'north',
         'carolina',
         'north',
         'dakota',
         'ohio',
         'oklahoma',
         'oregon',
         'pennsylvania',
         'rhode',
         'island',
         'south',
         'carolina',
         'south',
         'dakota',
         'tennessee',
         'texas',
         'utah',
         'vermont',
         'virginia',
         'washington',
         'west',
         'virginia',
         'wisconsin',
         'wyoming',
         'america',
         'u.s.',
         'asia']
    for token in gensim.utils.simple_preprocess(text):
        if token not in stopwords and len(token) > 2:
            result.append(lemmatize_stemming(token))
    return result




def remove_brackets(list1):
    """Remove [] from text"""
    return str(list1).replace('[','').replace(']','')

def get_first_title(title):
    """Return first title in job_title"""
    title = re.sub(r"[Cc]o[\-\ ]","", title)
    split_titles = re.split(r"\,|\:|\(|and", title)
    return split_titles[0].strip()









#Find the optimal number of topics
def compute_coherence_values(dictionary, corpus, texts, limit, start=2, step=3):
    """
    Compute c_v coherence for various number of topics

    Parameters:
    ----------
    dictionary : Gensim dictionary
    corpus : Gensim corpus
    texts : List of input texts
    limit : Max num of topics

    Returns:
    -------
    model_list : List of LDA topic models
    coherence_values : Coherence values corresponding to the LDA model with respective number of topics
    """
    coherence_values = []
    model_list = []
    for num_topics in range(start, limit, step):
        model=gensim.models.LdaMulticore(corpus=corpus, id2word=dictionary, 
                                         num_topics=num_topics, chunksize=100,
                                        passes=20, workers=4)
        model_list.append(model)
        coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())

    return model_list, coherence_values



def show_topics_sentences(ldamodel, corpus, texts):
    """Returns df with topics and descriptions"""
    sent_topics_df = pd.DataFrame()

    # Get main topic in each document
    for i, row in enumerate(ldamodel[corpus]):
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        # Get the Dominant topic, Perc Contribution and Keywords for each document
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # => dominant topic
                wp = ldamodel.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num), round(prop_topic,4), topic_keywords]), ignore_index=True)
            else:
                break
    sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']

    # Add original text to the end of the output
    contents = pd.Series(texts)
    sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)
    return(sent_topics_df)









def make_recommendation(nn_model, df, user=None):
    """Return top 10 recommended jobs based off user input"""
    if user is None:
        user = np.array([0,0,0,0,0,0,0,0,0]).reshape(1,-1)
    
    distances, indices = nn_model.kneighbors(user)
    
    job_recs = []
    for index in indices[0]:
        job_recs.append(df.iloc[index])
        
        
    similarity = []
    for distance in distances[0]:
        similarity.append(round(distance, 8))
        
    rec = []    
    for index, value in enumerate(job_recs[:10], 1):
        rec.append("{}. {}".format(index, value))
   
    
    return list(zip(rec, similarity[:10]))
    


def input_user_scores():
    """Collect user score"""
    
   
    print('''Scale of 0-10.
    0 is Do NOT agree and 10 is agree''')

    #col_names=['Computer Network', 'Web Dev', 'Security', 'Analyst', 
     #      'Leadership', 'Database Admin', 'Cloud Computing', 'Computer Support', 'Software/App Dev']
        
        
    topics=['Computer Network', 'Web Dev', 'Security', 'Analyst', 
           'Leadership', 'Database Admin', 'Cloud Computing', 'Computer Support', 'Software/App Dev']
        
            
    user_scores = [float(input(f"Agree or Disagree: I am/I like {topic}: ")) / 10
                   for topic in topics]
    print('\n')
    user = np.array(user_scores).reshape(1, -1)
    return user
    
    
    
    
def collect_score_and_recommend(nn_model, df):
    """Collect user score then output top 10 recommendations"""
    user = input_user_scores()
    return make_recommendation(nn_model, df, user)






