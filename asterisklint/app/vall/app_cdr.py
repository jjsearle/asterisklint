# AsteriskLint -- an Asterisk PBX config syntax checker
# Copyright (C) 2016  Walter Doekes, OSSO B.V.
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
from ..base import App, AppBase, AppOptions
from ...version import AsteriskVersion


class NoCDR(AppBase):
    removed_in = 21


class CheckedResetCDR(App):
    # Builtin up to Asterisk 13, in app_cdr since.
    name = 'ResetCDR'
    added_in = 20

    def __init__(self):
        options = 'ev'
        if AsteriskVersion().major >= 21:
            # The e option went together with NoCDR().
            options = 'v'
        super().__init__(args=[AppOptions(options)])


def register(app_loader):
    app_loader.register(NoCDR())
    app_loader.register(CheckedResetCDR())
