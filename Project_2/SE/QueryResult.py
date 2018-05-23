import whoosh.index as index
from whoosh.qparser import QueryParser, OrGroup
# from whoosh import scoring
import CustomScoring as scoring


def split_stem(stemmer=None, lemmatizer=None, stem_fn=None, value=None):
    '''
    Split given string query value and then Stem or lemmatize it.
    Union the result set with the original query token set and return modified(unified) query string.
    :param stemmer: Stemmer class in which is used stemming procedure.
    :param lemmatizer: Lemmatizer class in which is used lemmatizing procedure.
    :param stem_fn: Stemmer function which is for stemmer function provided by Whoosh itself
    :param value: String parameter which should be stemmed or lemmatized.
    :return: Stemmed or lemmatized query string
    '''
    stemmed_set = set()
    if type(value) is set:
        value_set = value
    else:
        value_set = set(value.lower().split())

    for entry in value_set:
        if lemmatizer:
            # Make plural nouns to singular ones
            stemmed_set.add(lemmatizer.lemmatize(entry))
        elif stemmer:
            stemmed_set.add(stemmer.stem(entry))
        elif stem_fn:
            stemmed_set.add(stem_fn(entry))
    tot_set = stemmed_set.union(value_set)
    re_query = ' '.join(tot_set)

    return re_query


def getSearchEngineResult(query_dict):
    result_dict = {}
    tot_result_dict = {}
    ix = index.open_dir("index")

    with ix.searcher(weighting=scoring.ScoringFunction()) as searcher:
        # TODO - Define your own query parser
        parser = QueryParser("contents", schema=ix.schema, group=OrGroup)

        #         for k,v in query_dict.items():
        #             v = v.replace(".", "")
        #             nouns = []
        #             weighted_tag = ['NN', 'NNS', 'NNP', 'NNPS']
        # #             weighted_tag = ['IN']
        #             tagged_list = [tag[1] for tag in custom_pos_tag(v)]

        #             nouns = [i for i in range(len(tagged_list)) if tagged_list[i] in weighted_tag]
        #             stemmed_query = [ps2(word) for word in v.lower().split()]
        #             for noun in nouns:
        #                 stemmed_query[noun] += '^1'

        #             tot_set = set(v.lower().split()).union(set(stemmed_query))
        #             result_query = ' '.join(tot_set)
        # #             print(result_query)

        #             query = parser.parse(result_query)
        #             results = searcher.search(query, limit=None)

        #             result_dict[k] = [result.fields()['docID'] for result in results]

        # Use PorterStemmer2 algorithm for stemming. Document index is made with this one.
        from whoosh.lang.porter2 import stem as ps2
        from whoosh.lang.porter import stem as ps1

        # New query_dict applying split_stem() method to every query string
        query_dict = {k: split_stem(stem_fn=ps2, value=v) for k, v in query_dict.items()}
        for qid, q in query_dict.items():
            query = parser.parse(q)
            results = searcher.search(query, limit=None)

            result_dict[qid] = [result.fields()['docID'] for result in results]

            # Expand query by k words
            # For this example, look for 5 top ranked documents and expand query by 2 words
            query_expansion = parse_document(result_dict[qid], 5, 2)
            expand_set = set([ps2(word[0]) for word in query_expansion]).union(set([word[0] for word in query_expansion]))
            q_set = set(q.split())

            # No need to expand words that already exist in 'q'
            unique_set = expand_set - q_set
            q += " " + " ".join(unique_set)

            tot_query = parser.parse(q)
            tot_results = searcher.search(tot_query, limit=None)

            tot_result_dict[qid] = [result.fields()['docID'] for result in tot_results]

    return tot_result_dict


def parse_document(related_doc_list, n, k):
    """
    For a given query, look for first n related_doc_list and count for word occurances.
    return Counter() object which contains k most occured words.
    Note that any stop words must be removed.
    :param n: integer designating the number of docs which will be used for query expansion
    :param k: integer designating the number of 'expanded query words' which the function will return
    :return: Counter object containing k most occurred words in n searched documents
    """
    from whoosh.lang.stopwords import stoplists
    from collections import Counter

    stop_words = stoplists["en"]
    nonstop_words = []
    with open('doc/document.txt', 'r') as f:
        text = f.read()
        docs = text.split('   /\n')[:-1]
        for doc in docs:
            br = doc.find('\n')
            docID = int(doc[:br])
            doc_text = doc[br + 1:]

            if docID in related_doc_list[:n]:
                nonstop_words.extend([word for word in doc_text.split() if word not in stop_words])

        # key: words, value: occurrence
        counter = Counter(nonstop_words)
        return counter.most_common(k)


def getRandom15SearchResult(query_dict):
    """
    Get Random Search results for checking variance, max and min value of BPREF
    Query Number 8,50,59 should be avoided hence those queries are only related to one document.
    :param query_dict: standard query_dict
    :return: result dictionary which contains every info about search result
    """
    result_dict = {}
    tot_result_dict ={}
    ix = index.open_dir("index")

    with ix.searcher(weighting=scoring.ScoringFunction()) as searcher:
        parser = QueryParser("contents", schema=ix.schema, group=OrGroup.factory(0.4))

        from whoosh.lang.porter2 import stem as ps2
        query_dict = {k: split_stem(stem_fn=ps2, value=v) for k, v in query_dict.items()}

        import random
        r = [i for i in range(1, 94) if i not in [8, 50, 59]]
        rand_15 = random.sample(r, 15)

        for qid in rand_15:
            q = query_dict[qid]
            query = parser.parse(q)
            results = searcher.search(query, limit=None)
            result_dict[qid] = [result.fields()['docID'] for result in results]

            query_expansion = parse_document(result_dict[qid], 5, 3)
            expand_set = set([ps2(word[0]) for word in query_expansion]).union(
                set([word[0] for word in query_expansion]))
            q_set = set(q.split())

            unique_set = expand_set - q_set
            q += " " + " ".join(unique_set)

            tot_query = parser.parse(q)
            tot_results = searcher.search(tot_query, limit=None)

            tot_result_dict[qid] = [result.fields()['docID'] for result in tot_results]

        print("Random 15 queries: " + ",".join(str(x) for x in rand_15))
    return tot_result_dict
