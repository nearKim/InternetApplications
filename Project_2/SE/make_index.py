import os.path
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, NUMERIC
from whoosh.analysis import StemmingAnalyzer
from whoosh.lang.snowball import english
from whoosh.lang.porter2 import stem
# from whoosh.lang.paicehusk import PaiceHuskStemmer

# Use PorterStemmer2 Algorithm in indexing
stem_ana = StemmingAnalyzer(stemfn=stem)

schema = Schema(docID=NUMERIC(stored=True), contents=TEXT(analyzer=stem_ana))
index_dir = "index"

if not os.path.exists(index_dir):
    os.makedirs(index_dir)

ix = create_in(index_dir, schema)

writer = ix.writer()

with open('doc/document.txt', 'r') as f:
    text = f.read()
    docs = text.split('   /\n')[:-1]
    for doc in docs:
        br = doc.find('\n')
        docID = int(doc[:br])
        doc_text = doc[br + 1:]
        writer.add_document(docID=docID, contents=doc_text)

writer.commit()