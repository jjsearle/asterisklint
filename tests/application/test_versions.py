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
from asterisklint.alinttest import ALintTestCase, asteriskVersion
from asterisklint.app.base import AppOptions
from asterisklint.application import App
from asterisklint.varfun import FuncLoader
from asterisklint.version import AsteriskVersion
from asterisklint.where import DUMMY_WHERE


def app(data):
    App(data, where=DUMMY_WHERE)


def func(data):
    FuncLoader().process_read_function(data, where=DUMMY_WHERE)


class AsteriskVersionTest(ALintTestCase):
    def test_normalize(self):
        for value in ('20', 'v20', '20.5.1', 20):
            self.assertEqual(AsteriskVersion.normalize(value), 'v20')

    def test_unsupported(self):
        for value in ('12', '24', 'v1.8', 'foo'):
            self.assertRaises(ValueError, AsteriskVersion.normalize, value)

    def test_default_is_unchanged(self):
        self.assertEqual(AsteriskVersion().version, 'v13')


class SplitOptionsTest(ALintTestCase):
    def test_skips_option_arguments(self):
        self.assertEqual(
            AppOptions.split_options('tg(5)U(sub^arg1^arg2)M(x(y))'),
            ['t', 'g', 'U', 'M'])


class AppAvailabilityTest(ALintTestCase):
    def test_new_apps_in_v20_and_v22(self):
        for version in ('v20', 'v22'):
            with asteriskVersion(version):
                app('MSet(a=1,b=2)')
                app('If($[${a}=1])')
                app('EndIf()')
                app('AMD()')
                app('PJSIPHangup(486)')
                app('SLAStation(station1)')
                self.assertLinted({})

    def test_new_apps_not_in_v13(self):
        app('If($[${a}=1])')
        app('AMD()')
        self.assertLinted({'E_APP_MISSING': 2})

    def test_removed_in_v21(self):
        apps = ('Macro(foo)', 'NoCDR()', 'SIPAddHeader(X-Foo: bar)',
                'ImportVar(a=chan,b)', 'SetAMAFlags(billing)',
                'Monitor(wav)', 'OSPAuth(provider)')
        with asteriskVersion('v20'):
            for data in apps:
                app(data)
            self.assertLinted({})
        with asteriskVersion('v22'):
            for data in apps:
                app(data)
            self.assertLinted({'E_APP_MISSING': len(apps)})

    def test_gone_by_v20(self):
        with asteriskVersion('v20'):
            app('SetCallerID(123)')
            app('MYSQL(Connect conn host user pass db)')
            app('MailboxExists(100@default)')
            self.assertLinted({'E_APP_MISSING': 3})

    def test_mset_checks_assignments(self):
        with asteriskVersion('v20'):
            app('MSet(a=1,b)')
            self.assertLinted({'E_ASSIGN_NO_EQUALS': 1})


class AppOptionsTest(ALintTestCase):
    def test_dial_macro_option(self):
        with asteriskVersion('v20'):
            app('Dial(PJSIP/100,30,tM(foo^bar))')
            self.assertLinted({})
        with asteriskVersion('v22'):
            app('Dial(PJSIP/100,30,tM(foo^bar))')
            self.assertLinted({'E_APP_ARG_BADOPT': 1})

    def test_dial_option_arguments(self):
        with asteriskVersion('v22'):
            app('Dial(PJSIP/100&PJSIP/101,,tTg(5)U(sub^a^b)b(pre^s^1))')
            self.assertLinted({})

    def test_dial_too_many_args(self):
        with asteriskVersion('v22'):
            app('Dial(PJSIP/100,30,t,url,extra)')
            self.assertLinted({'E_APP_ARG_MANY': 1})

    def test_queue_monitor_options_and_macro_arg(self):
        with asteriskVersion('v20'):
            app('Queue(support,tw,,,30,,macro,gosub,rule,1)')
            self.assertLinted({})
        with asteriskVersion('v22'):
            app('Queue(support,tw,,,30,,gosub,rule,1)')
            self.assertLinted({'E_APP_ARG_BADOPT': 1})
            app('Queue(support,t,,,30,,macro,gosub,rule,1)')
            self.assertLinted({'E_APP_ARG_MANY': 1})

    def test_resetcdr_e_option(self):
        with asteriskVersion('v20'):
            app('ResetCDR(ev)')
            self.assertLinted({})
        with asteriskVersion('v22'):
            app('ResetCDR(ev)')
            self.assertLinted({'E_APP_ARG_BADOPT': 1})

    def test_voicemail_new_options(self):
        with asteriskVersion('v22'):
            app('VoiceMail(100@default,g(5)eSt(beep))')
            self.assertLinted({})

    def test_originate_options(self):
        with asteriskVersion('v22'):
            app('Originate(PJSIP/100,exten,ctx,s,1,30,av(a=b))')
            self.assertLinted({})
            app('Originate(PJSIP/100,exten,ctx,s,1,30,z)')
            self.assertLinted({'E_APP_ARG_BADOPT': 1})

    def test_milliwatt_m_option(self):
        app('Milliwatt(m)')
        self.assertLinted({})


class FuncAvailabilityTest(ALintTestCase):
    def test_new_functions(self):
        for version in ('v20', 'v22'):
            with asteriskVersion(version):
                func('MAX(1,2)')
                func('TRIM( a )')
                func('PJSIP_HEADERS(X-)')
                func('HANGUPCAUSE(chan,tech)')
                self.assertLinted({})

    def test_new_functions_not_in_v13(self):
        func('MAX(1,2)')
        self.assertLinted({'E_FUNC_MISSING': 1})

    def test_chan_sip_functions_removed_in_v21(self):
        with asteriskVersion('v20'):
            func('SIPPEER(foo,ip)')
            func('SIP_HEADERS(X-)')
            self.assertLinted({})
        with asteriskVersion('v22'):
            func('SIPPEER(foo,ip)')
            func('SIP_HEADERS(X-)')
            self.assertLinted({'E_FUNC_MISSING': 2})

    def test_featuremap_automon(self):
        with asteriskVersion('v20'):
            func('FEATUREMAP(automon)')
            self.assertLinted({})
        with asteriskVersion('v22'):
            func('FEATUREMAP(automon)')
            func('FEATUREMAP(automixmon)')
            self.assertLinted({'E_FUNC_BAD_ARGS': 1})
