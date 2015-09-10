# -*- coding: utf-8 -*-
#
# Copyright 2004-2006 Zuza Software Foundation
#
# This file is part of translate.
#
# translate is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# translate is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

"""A thin wrapper around BytesIO that accepts and auto-convert non bytes input"""

import six
from io import BytesIO


class StringIO(BytesIO):

    def __init__(self, buf=''):
        if not isinstance(buf, six.string_types):
            buf = bytes(buf)
        if isinstance(buf, six.text_type):
            buf = buf.encode('utf-8')
        super(StringIO, self).__init__(buf)


class CatchStringOutput(StringIO):
    """catches the output before it is closed and sends it to an onclose
    method"""

    def __init__(self, onclose):
        """Set up the output stream, and remember a method to call on
        closing"""
        StringIO.__init__(self)
        self.onclose = onclose

    def close(self):
        """wrap the underlying close method, to pass the value to onclose
        before it goes"""
        value = self.getvalue()
        self.onclose(value)
        super(CatchStringOutput, self).close()

    def slam(self):
        """use this method to force the closing of the stream if it isn't
        closed yet"""
        if not self.closed:
            self.close()
