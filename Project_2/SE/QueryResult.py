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
    value_set = set(value.lower().split())

    for entry in value.lower().split():
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
    return result_dict


def getRandom15SearchResult(query_dict):
    """
    Get Random Search results for checking variance, max and min value of BPREF
    Query Number 8,50,59 should be avoided hence those queries are only related to one document.
    :param query_dict: standard query_dict
    :return: result dictionary which contains every info about search result
    """
    result_dict = {}
    ix = index.open_dir("index")

    with ix.searcher(weighting=scoring.ScoringFunction()) as searcher:
        parser = QueryParser("contents", schema=ix.schema, group=OrGroup.factory(0.4))

        from whoosh.lang.porter2 import stem as ps2
        query_dict = {k: split_stem(stem_fn=ps2, value=v) for k, v in query_dict.items()}

        import random
        r = [i for i in range(1, 94) if i not in [8, 50, 59]]
        rand_15 = random.sample(r, 15)

        for qid in rand_15:
            query = parser.parse(query_dict[qid])
            results = searcher.search(query, limit=None)
            result_dict[qid] = [result.fields()['docID'] for result in results]
        print("Random 15 queries: " + ",".join(str(x) for x in rand_15))
    return result_dict
