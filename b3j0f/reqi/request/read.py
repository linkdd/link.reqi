# -*- coding: utf-8 -*-

# --------------------------------------------------------------------
# The MIT License (MIT)
#
# Copyright (c) 2016 Jonathan Labéjof <jonathan.labejof@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# --------------------------------------------------------------------

"""Specification of the class Read.

Equivalent to the SELECT statement in SQL."""

__all__ = ['Read']

from .base import Node

from six import string_types

ASCENDING = 1  #: ascending sort order.
DESCENDING = -1  #: descending sort order.


class Read(Node):
    """In charge of selecting data to retrieve."""

    __slots__ = ['exprs', 'offset', 'limit', 'groupby', 'sort']

    def __init__(
            self, exprs, offset=None, limit=None, groupby=None, sort=None,
            *args, **kwargs
    ):
        """
        :param list exprs: list of expressions to select.
        :param int offset: starting index of data to retrieve.
        :param int limit: maximal number of elements to retrieve.
        :param list groupby: list of expressions to groupy by.
        :param list sort: list of field to sort.
        """

        super(Read, self).__init__(*args, **kwargs)

        self.exprs = exprs
        self.offset = offset
        self.limit = limit
        self.groupby = groupby
        self.sort = sort

    def _run(self, *args, **kwargs):

        result = super(Read, self).run(*args, **kwargs)

        if self.exprs:
            result, oldresult = {}, result

            for expr in self.exprs:
                result[expr] = oldresult.expr

        if self.offset or self.limit:
            offset = self.offset or 0
            limit = self.limit or maxsize

            for key in list(result):
                result[key] = result[offset:limit]

        if self.groupby:
            raise NotImplementedError()

        if self.sort:
            for sortp in self.sort:
                if isinstance(sortp, string_types):
                    sortp = (sortp, ASCENDING)

                for key in list(result):
                    result[key] = sorted(
                        result[key], key=sortp[0], reverse=sortp==DESCENDING
                    )

        return result
