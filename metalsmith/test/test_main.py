# Copyright 2015-2017 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

import mock

from metalsmith import main


@mock.patch.object(main.deploy, 'deploy', autospec=True)
@mock.patch.object(main.generic, 'Password', autospec=True)
class TestMain(unittest.TestCase):
    def test_args_ok(self, mock_auth, mock_deploy):
        args = ['--network', 'mynet', '--image', 'myimg', 'compute']
        main.main(args)
        mock_deploy.assert_called_once_with(mock.ANY,
                                            profile='compute',
                                            image_id='myimg',
                                            network_id='mynet')

    def test_args_debug(self, mock_auth, mock_deploy):
        args = ['--network', 'mynet', '--image', 'myimg', '--debug', 'compute']
        main.main(args)
        mock_deploy.assert_called_once_with(mock.ANY,
                                            profile='compute',
                                            image_id='myimg',
                                            network_id='mynet')

    @mock.patch.object(main.LOG, 'critical', autospec=True)
    def test_deploy_failure(self, mock_log, mock_auth, mock_deploy):
        args = ['--network', 'mynet', '--image', 'myimg', 'compute']
        mock_deploy.side_effect = RuntimeError('boom')
        self.assertRaises(SystemExit, main.main, args)
        mock_log.assert_called_once_with('%s', mock_deploy.side_effect,
                                         exc_info=False)
