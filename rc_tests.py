#!/usr/bin/env python3
# Copyright 2018 Evgeny Golyshev <eugulixes@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from optparse import OptionParser

from base import RocketChatTestCase


class GeneralTestCase(RocketChatTestCase):
    def __init__(self, addr, username, password, rc_version, **kwargs):
        RocketChatTestCase.__init__(self, addr, username, password, **kwargs)

        self._rc_version = rc_version

    def test_check_rc_version(self):
        options_btn = self.browser.find_by_css(
            '.sidebar__toolbar-button.rc-tooltip.rc-tooltip--down.js-button'
        )
        assert len(options_btn)
        options_btn.last.click()

        administration_btn = self.browser.find_by_css('.rc-popover__item-text')
        assert administration_btn
        administration_btn.click()

        info_btn = self.browser.driver.find_elements_by_css_selector(
            'a.sidebar-item__link[aria-label="Info"]')

        assert len(info_btn)

        self.browser.driver.execute_script("arguments[0].click();",
                                           info_btn[0])

        info_table = self.browser.find_by_css(".admin-table-row")
        assert len(info_table)

        version = '.'.join(info_table.first.text.split()[1].split('.')[0:2])
        assert version == self._rc_version


def main():
    parser = OptionParser(usage='usage: %prog [options] arguments')
    parser.add_option('-a', '--host', dest='host',
                      help='allows specifying admin username')
    parser.add_option('-u', '--username', dest='username',
                      help='allows specifying admin username')
    parser.add_option('-p', '--password', dest='password',
                      help='allows specifying admin password')
    parser.add_option('-v', '--rc_version', dest='rc_version',
                      help='allows specifying version of Rocket.Chat')
    options, args = parser.parse_args()

    if not options.host:
        parser.error('Host is not specified')

    if not options.username:
        parser.error('Username is not specified')

    if not options.password:
        parser.error('Password is not specified')

    if not options.rc_version:
        parser.error('Rocket.Chat version is not specified')

    test_cases = GeneralTestCase(options.host, options.username,
                                 options.password, options.rc_version)
    test_cases.run()


if __name__ == '__main__':
    main()
