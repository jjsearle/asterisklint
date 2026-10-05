# AsteriskLint -- an Asterisk PBX config syntax checker
# Copyright (C) 2026  Walter Doekes, OSSO B.V.
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


class CALENDAR_BUSY(FuncBase):
    pass


class CALENDAR_EVENT(FuncBase):
    pass


class CALENDAR_QUERY(FuncBase):
    pass


class CALENDAR_QUERY_RESULT(FuncBase):
    pass


class CALENDAR_WRITE(FuncBase):
    pass


def register(func_loader):
    for func in (
            CALENDAR_BUSY,
            CALENDAR_EVENT,
            CALENDAR_QUERY,
            CALENDAR_QUERY_RESULT,
            CALENDAR_WRITE,
            ):
        func_loader.register(func())
