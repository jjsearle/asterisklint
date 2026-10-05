# AsteriskLint -- an Asterisk PBX config syntax checker
# Copyright (C) 2015-2016  Walter Doekes, OSSO B.V.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from ..base import FuncBase


class ODBC_FETCH(FuncBase):
    pass


class SQL_ESC(FuncBase):
    pass


class SQL_ESC_BACKSLASHES(FuncBase):
    added_in = 20


def register(func_loader):
    for func in (
            ODBC_FETCH,
            SQL_ESC,
            SQL_ESC_BACKSLASHES,
            ):
        func_loader.register(func())
