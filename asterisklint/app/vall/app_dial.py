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
from ..base import App, AppArg, AppBase, AppOptions
from ...version import AsteriskVersion


class Dial(AppBase):
    # Arguments are only checked for versions we have documentation
    # for. See CheckedDial.
    removed_in = 20


class CheckedDial(App):
    name = 'Dial'
    added_in = 20

    def __init__(self):
        options = 'aAbBcCdDeEfFgGhHiIjkKLmMnNoOpPQrRsStTuUwWxXz'
        if AsteriskVersion().major >= 21:
            # M(macro^arg) was removed together with app_macro.
            options = options.replace('M', '')
        super().__init__(
            args=[AppArg('devices'), AppArg('timeout'), AppOptions(options),
                  AppArg('url')],
            min_args=1)


class RetryDial(AppBase):
    pass


def register(app_loader):
    app_loader.register(Dial())
    app_loader.register(CheckedDial())
    app_loader.register(RetryDial())
