# AsteriskLint -- an Asterisk PBX config syntax checker
# Copyright (C) 2015-2017  Walter Doekes, OSSO B.V.
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
from ..base import App, AppArg, AppOptions, AppBase
from ...version import AsteriskVersion


class VoiceMail(App):
    def __init__(self):
        if AsteriskVersion().major >= 20:
            options = 'bdegPsStuU'
        else:
            options = 'bdgsuUP'
        super().__init__(
            args=[AppArg('mailboxes'), AppOptions(options)], min_args=1)


class VoiceMailMain(AppBase):
    pass


class VoiceMailPlayMsg(AppBase):
    pass


class MailboxExists(AppBase):
    # Superseded by the VM_INFO() function; absent from the Asterisk 20
    # documentation.
    removed_in = 20


class VMAuthenticate(AppBase):
    pass


class VMSayName(AppBase):
    pass


def register(app_loader):
    for app in (
            VoiceMail,
            VoiceMailMain,
            VoiceMailPlayMsg,
            MailboxExists,
            VMAuthenticate,
            VMSayName,
            ):
        app_loader.register(app())
