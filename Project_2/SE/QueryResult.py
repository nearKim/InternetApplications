import whoosh.index as index
from whoosh.qparser import QueryParser, OrGroup
# from whoosh import scoring
import CustomScoring as scoring


def split_stem(stemmer=None, lemmatizer=None, value=None):
    stemmed_set = set()
    value_set = set(value.lower().split())

    for entry in value.lower().split():
        if lemmatizer:
            # Make plural nouns to singular ones
            # print(entry.strip() +"=====>" + lemmatizer.lemmatize(entry))
            stemmed_set.add(lemmatizer.lemmatize(entry))
        else:
            stemmed_set.add(stemmer.stem(entry))
    tot_set = stemmed_set.union(value_set)
    re_query = ' '.join(tot_set)

    # print(re_query)
    return re_query


def getSearchEngineResult(query_dict):
    result_dict = {}
    ix = index.open_dir("index")

    # with ix.searcher(weighting=scoring.BM25F()) as searcher:
    with ix.searcher(weighting=scoring.ScoringFunction()) as searcher:
        # TODO - Define your own query parser
        parser = QueryParser("contents", schema=ix.schema, group=OrGroup.factory(0.4))

        from nltk.stem import (PorterStemmer,
                               SnowballStemmer,
                               WordNetLemmatizer)

        lm = WordNetLemmatizer()
        query_dict = {k: split_stem(lemmatizer=lm, value=v) for k, v in query_dict.items()}

        # ss = SnowballStemmer('english', ignore_stopwords=True)
        # query_dict = {k: split_stem(stemmer=ss, value=v) for k, v in query_dict.items()}
        # ps = PorterStemmer()
        # query_dict = {k: split_stem(stemmer=ps, value=v) for k, v in query_dict.items()}

        for qid, q in query_dict.items():
            query = parser.parse(q)
            results = searcher.search(query, limit=None)

            result_dict[qid] = [result.fields()['docID'] for result in results]
    return result_dict
