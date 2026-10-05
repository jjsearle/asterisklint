# AsteriskLint -- an Asterisk PBX config syntax checker
# Copyright (C) 2015-2019  Walter Doekes, OSSO B.V.
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
import os

from .cls import Singleton


class AsteriskVersion(metaclass=Singleton):
    """
    Store the used Asterisk version globally. If you don't initialize
    this before anyone requests anything, you get the default.

    Example::

        from asterisklint.version import AsteriskVersion

        AsteriskVersion('v13')  # set version 13 throughout the run
    """
    DEFAULT = 'v13'
    SUPPORTED = ('v11', 'v13', 'v20', 'v22')

    def __init__(self, version=None):
        self.version = self.normalize(version or self.DEFAULT)

    def reinit(self, version=None):
        if version and self.version != self.normalize(version):
            raise RuntimeError(
                'Attempt to re-set Asterisk version from {} to {}'.format(
                    self.version, version))

    @classmethod
    def normalize(cls, version):
        """
        Turn '20', 'v20' or '20.5.1' into 'v20'. Raises ValueError for
        versions we have no app/func definitions for.
        """
        normalized = 'v{}'.format(str(version).lstrip('v').split('.', 1)[0])
        if normalized not in cls.SUPPORTED:
            raise ValueError(
                'Unsupported Asterisk version {!r}, choose from: {}'.format(
                    version, ', '.join(i[1:] for i in cls.SUPPORTED)))
        return normalized

    @property
    def major(self):
        return int(self.version[1:])

    def provides(self, app_or_func):
        """
        Return whether the app/func exists in this version, judging by
        its optional added_in/removed_in major version attributes.
        """
        added_in = getattr(app_or_func, 'added_in', None)
        removed_in = getattr(app_or_func, 'removed_in', None)
        return ((added_in is None or self.major >= added_in) and
                (removed_in is None or self.major < removed_in))

    def list_app_mods(self):
        """
        Return a list app names in absolute import format. Takes
        internal version into account.
        """
        return self._list_mods('app')

    def list_func_mods(self):
        """
        Return a list function names in absolute import format. Takes
        internal version into account.
        """
        return self._list_mods('func')

    def _get_path(self, submod):
        return os.path.join(os.path.dirname(__file__), submod, self.version)

    def _list_mods(self, submod):
        appsdir = self._get_path(submod)
        appmods = [i[0:-3] for i in os.listdir(appsdir) if i.endswith('.py')]

        modfmt = 'asterisklint.{}.{}.{{}}'.format(submod, self.version)
        return [modfmt.format(appmod) for appmod in appmods]
