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
from .. import E_FUNC_BAD_ARGS
from ..base import FuncBase
from ...version import AsteriskVersion


class _Builtin(object):
    @property
    def module(self):
        return '<builtin>'


class BuiltinFuncBase(_Builtin, FuncBase):
    pass


class AMI_CLIENT(BuiltinFuncBase):
    pass


class EXCEPTION(BuiltinFuncBase):
    pass


class FEATURE(BuiltinFuncBase):
    pass


class FEATUREMAP(BuiltinFuncBase):
    def __call__(self, data, where):
        # Only checked for versions we have documentation for.
        if AsteriskVersion().major >= 20 and isinstance(data, str):
            features = ['atxfer', 'blindxfer', 'automon', 'disconnect',
                        'parkcall', 'automixmon']
            if AsteriskVersion().major >= 21:
                # automon went together with res_monitor.
                features.remove('automon')
            if data not in features:
                E_FUNC_BAD_ARGS(where, func=self.name, data=data)
        super().__call__(data, where)


class MESSAGE(BuiltinFuncBase):
    pass


class MESSAGE_DATA(BuiltinFuncBase):
    pass


class TESTTIME(BuiltinFuncBase):
    pass


class LOG_GROUP(BuiltinFuncBase):
    added_in = 20


def register(func_loader):
    for func in (
            AMI_CLIENT, EXCEPTION, FEATURE, FEATUREMAP,
            MESSAGE, MESSAGE_DATA, TESTTIME,
            LOG_GROUP):
        func_loader.register(func())
