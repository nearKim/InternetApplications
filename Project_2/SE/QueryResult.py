import whoosh.index as index
from whoosh.qparser import QueryParser, OrGroup
# from whoosh import scoring
import CustomScoring as scoring


def getSearchEngineResult(query_dict):
    result_dict = {}
    ix = index.open_dir("index")

    # with ix.searcher(weighting=scoring.BM25F()) as searcher:
    with ix.searcher(weighting=scoring.ScoringFunction()) as searcher:
        # TODO - Define your own query parser
        parser = QueryParser("contents", schema=ix.schema, group=OrGroup)
        for qid, q in query_dict.items():
            query = parser.parse(q)
            results = searcher.search(query, limit=None)
            # for result in results:
            #     print(result.fields()['docID'], result.score)

            result_dict[qid] = [result.fields()['docID'] for result in results]
    return result_dict