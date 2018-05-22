# Copyright 2008 Matt Chaput. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    1. Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#
#    2. Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY MATT CHAPUT ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
# EVENT SHALL MATT CHAPUT OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# The views and conclusions contained in the software and documentation are
# those of the authors and should not be interpreted as representing official
# policies, either expressed or implied, of Matt Chaput.

"""
This module contains classes for scoring (and sorting) search results.
"""

from __future__ import division
from math import log, pi

from whoosh.compat import iteritems


# Base classes

class WeightingModel(object):
    """Abstract base class for scoring models. A WeightingModel object provides
    a method, ``scorer``, which returns an instance of
    :class:`whoosh.scoring.Scorer`.

    Basically, WeightingModel objects store the configuration information for
    the model (for example, the values of B and K1 in the BM25F model), and
    then creates a scorer instance based on additional run-time information
    (the searcher, the fieldname, and term text) to do the actual scoring.
    """

    use_final = False

    def idf(self, searcher, fieldname, text):
        """Returns the inverse document frequency of the given term.
        """

        parent = searcher.get_parent()
        n = parent.doc_frequency(fieldname, text)
        dc = parent.doc_count_all()
        return log(dc / (n + 1)) + 1

    def scorer(self, searcher, fieldname, text, qf=1):
        """Returns an instance of :class:`whoosh.scoring.Scorer` configured
        for the given searcher, fieldname, and term text.
        """

        raise NotImplementedError(self.__class__.__name__)

    def final(self, searcher, docnum, score):
        """Returns a final score for each document. You can use this method
        in subclasses to apply document-level adjustments to the score, for
        example using the value of stored field to influence the score
        (although that would be slow).

        WeightingModel sub-classes that use ``final()`` should have the
        attribute ``use_final`` set to ``True``.

        :param searcher: :class:`whoosh.searching.Searcher` for the index.
        :param docnum: the doc number of the document being scored.
        :param score: the document's accumulated term score.

        :rtype: float
        """

        return score


class BaseScorer(object):
    """Base class for "scorer" implementations. A scorer provides a method for
    scoring a document, and sometimes methods for rating the "quality" of a
    document and a matcher's current "block", to implement quality-based
    optimizations.

    Scorer objects are created by WeightingModel objects. Basically,
    WeightingModel objects store the configuration information for the model
    (for example, the values of B and K1 in the BM25F model), and then creates
    a scorer instance.
    """

    def supports_block_quality(self):
        """Returns True if this class supports quality optimizations.
        """

        return False

    def score(self, matcher):
        """Returns a score for the current document of the matcher.
        """

        raise NotImplementedError(self.__class__.__name__)

    def max_quality(self):
        """Returns the *maximum limit* on the possible score the matcher can
        give. This can be an estimate and not necessarily the actual maximum
        score possible, but it must never be less than the actual maximum
        score.
        """

        raise NotImplementedError(self.__class__.__name__)

    def block_quality(self, matcher):
        """Returns the *maximum limit* on the possible score the matcher can
        give **in its current "block"** (whatever concept of "block" the
        backend might use). This can be an estimate and not necessarily the
        actual maximum score possible, but it must never be less than the
        actual maximum score.

        If this score is less than the minimum score
        required to make the "top N" results, then we can tell the matcher to
        skip ahead to another block with better "quality".
        """

        raise NotImplementedError(self.__class__.__name__)


# Scorer that just returns term weight

class WeightScorer(BaseScorer):
    """A scorer that simply returns the weight as the score. This is useful
    for more complex weighting models to return when they are asked for a
    scorer for fields that aren't scorable (don't store field lengths).
    """

    def __init__(self, maxweight):
        self._maxweight = maxweight

    def supports_block_quality(self):
        return True

    def score(self, matcher):
        return matcher.weight()

    def max_quality(self):
        return self._maxweight

    def block_quality(self, matcher):
        return matcher.block_max_weight()

    @classmethod
    def for_(cls, searcher, fieldname, text):
        ti = searcher.term_info(fieldname, text)
        return cls(ti.max_weight())


# Base scorer for models that only use weight and field length

class WeightLengthScorer(BaseScorer):
    """Base class for scorers where the only per-document variables are term
    weight and field length.

    Subclasses should override the ``_score(weight, length)`` method to return
    the score for a document with the given weight and length, and call the
    ``setup()`` method at the end of the initializer to set up common
    attributes.
    """

    def setup(self, searcher, fieldname, text):
        """Initializes the scorer and then does the busy work of
        adding the ``dfl()`` function and maximum quality attribute.

        This method assumes the initializers of WeightLengthScorer subclasses
        always take ``searcher, offset, fieldname, text`` as the first three
        arguments. Any additional arguments given to this method are passed
        through to the initializer.

        Note: this method calls ``self._score()``, so you should only call it
        in the initializer after setting up whatever attributes ``_score()``
        depends on::

            class MyScorer(WeightLengthScorer):
                def __init__(self, searcher, fieldname, text, parm=1.0):
                    self.parm = parm
                    self.setup(searcher, fieldname, text)

                def _score(self, weight, length):
                    return (weight / (length + 1)) * self.parm
        """

        ti = searcher.term_info(fieldname, text)
        if not searcher.schema[fieldname].scorable:
            return WeightScorer(ti.max_weight())

        self.dfl = lambda docid: searcher.doc_field_length(docid, fieldname, 1)
        self._maxquality = self._score(ti.max_weight(), ti.min_length())

    def supports_block_quality(self):
        return True

    def score(self, matcher):
        return self._score(matcher.weight(), self.dfl(matcher.id()))

    def max_quality(self):
        return self._maxquality

    def block_quality(self, matcher):
        return self._score(matcher.block_max_weight(),
                           matcher.block_min_length())

    def _score(self, weight, length):
        # Override this method with the actual scoring function
        raise NotImplementedError(self.__wclass__.__name__)


def intappscorer(tf, idf, cf, qf, dc, fl, avgfl, param):
    # tf - term frequency in the current document
    # idf - inverse document frequency
    # cf - term frequency in the collection
    # qf - term frequency in the query
    # dc - doc count
    # fl - field length in the current document
    # avgfl - average field length across documents in collection
    # param - free parameter
    # TODO - Define your own scoring function

    # K1 = 0.5
    # B = 0.5
    #
    # bm25_score = idf * ((tf * (K1 + 1)) / (tf + K1 * ((1 - B) + B * fl / avgfl)))

    # prior = tf / fl
    # post = (tf + 1.0) / (fl + 1.0)
    # invpriorcol = avgfl / cf
    # norm = tf * log(post / prior)
    # dfree_score = qf * norm * (tf * (log(prior * invpriorcol))
    #                            + (tf + 1.0) * (log(post * invpriorcol))
    #                            + 0.5 * log(post / prior))

    c = 3.2
    rec_log2_of_e = 1.0 / log(2)
    TF = tf * log(1.0 + (c * avgfl) / fl)
    norm = 1.0 / (TF + 1.0)
    f = cf / dc
    pl2_score = norm * qf * (TF * log(1.0 / f)
                             + f * rec_log2_of_e
                             + 0.5 * log(2 * pi * TF)
                             + TF * (log(TF) - rec_log2_of_e))

    # total_score = 0.0 * bm25_score + 0.04 * dfree_score + 2.0 * pl2_score
    # total_score = 1 * bm25_score + 4 * pl2_score

    return pl2_score


class ScoringFunction(WeightingModel):
    def __init__(self, param=1.0):
        self.param = param

    def scorer(self, searcher, fieldname, text, qf=1):
        if not searcher.schema[fieldname].scorable:
            return WeightScorer.for_(searcher, fieldname, text)

        return CustomScoring(searcher, fieldname, text, self.param, qf=qf)


class CustomScoring(WeightLengthScorer):
    def __init__(self, searcher, fieldname, text, param, qf=1):
        parent = searcher.get_parent()  # Returns self if no parent
        self.idf = parent.idf(fieldname, text)
        self.cf = parent.frequency(fieldname, text)
        self.dc = parent.doc_count_all()
        # self.fl = parent.field_length(fieldname)
        self.avgfl = parent.avg_field_length(fieldname) or 1

        self.param = param
        self.qf = qf
        self.setup(searcher, fieldname, text)

    def _score(self, weight, length):
        return intappscorer(weight, self.idf, self.cf, self.qf, self.dc, length, self.avgfl, self.param)


# Implementation of BM25F model for example

def bm25(idf, tf, fl, avgfl, B, K1):
    # idf - inverse document frequency
    # tf - term frequency in the current document
    # fl - field length in the current document
    # avgfl - average field length across documents in collection
    # B, K1 - free paramters

    return idf * ((tf * (K1 + 1)) / (tf + K1 * ((1 - B) + B * fl / avgfl)))


class BM25F(WeightingModel):
    def __init__(self, B=0.75, K1=1.2, **kwargs):
        self.B = B
        self.K1 = K1

        self._field_B = {}
        for k, v in iteritems(kwargs):
            if k.endswith("_B"):
                fieldname = k[:-2]
                self._field_B[fieldname] = v

    def supports_block_quality(self):
        return True

    def scorer(self, searcher, fieldname, text, qf=1):
        if not searcher.schema[fieldname].scorable:
            return WeightScorer.for_(searcher, fieldname, text)

        if fieldname in self._field_B:
            B = self._field_B[fieldname]
        else:
            B = self.B

        return BM25FScorer(searcher, fieldname, text, B, self.K1, qf=qf)


class BM25FScorer(WeightLengthScorer):
    def __init__(self, searcher, fieldname, text, B, K1, qf=1):
        # IDF and average field length are global statistics, so get them from
        # the top-level searcher
        parent = searcher.get_parent()  # Returns self if no parent
        self.idf = parent.idf(fieldname, text)
        self.avgfl = parent.avg_field_length(fieldname) or 1

        self.B = B
        self.K1 = K1
        self.qf = qf
        self.setup(searcher, fieldname, text)

    def _score(self, weight, length):
        s = bm25(self.idf, weight, length, self.avgfl, self.B, self.K1)
        return s
