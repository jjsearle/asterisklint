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


class Queue(AppBase):
    # Arguments are only checked for versions we have documentation
    # for. See CheckedQueue.
    removed_in = 20


class CheckedQueue(App):
    name = 'Queue'
    added_in = 20

    def __init__(self):
        options = 'bBcCdFhHiIkKmnrRtTwWxX'
        macro = [AppArg('macro')]
        if AsteriskVersion().major >= 21:
            # The w/W (Monitor) options went with res_monitor and the
            # macro argument went with app_macro.
            options = options.replace('w', '').replace('W', '')
            macro = []
        super().__init__(
            args=([AppArg('queuename'), AppOptions(options), AppArg('url'),
                   AppArg('announceoverride'), AppArg('timeout'),
                   AppArg('agi')] + macro +
                  [AppArg('gosub'), AppArg('rule'), AppArg('position')]),
            min_args=1)


class AddQueueMember(AppBase):
    pass


class RemoveQueueMember(AppBase):
    pass


class PauseQueueMember(AppBase):
    pass


class UnpauseQueueMember(AppBase):
    pass


class QueueLog(AppBase):
    pass


class QueueUpdate(AppBase):
    added_in = 20


def register(app_loader):
    for app in (
            Queue,
            CheckedQueue,
            AddQueueMember,
            RemoveQueueMember,
            PauseQueueMember,
            UnpauseQueueMember,
            QueueLog,
            QueueUpdate,
            ):
        app_loader.register(app())
