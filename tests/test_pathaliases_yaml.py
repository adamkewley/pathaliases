# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import unittest

import pathaliases


def _fixure_path(p):
    return os.path.join(os.path.dirname(__file__), "fixtures", p)


class TestPathaliasesYAML(unittest.TestCase):

    def test_readme_demo_example_works(self):
        readme_demo_path = _fixure_path("readme_demo.yml")
        aliases = pathaliases.resolve_yaml_to_path_strings(readme_demo_path)

        self.assertIsNotNone(aliases)
        self.assertIsInstance(aliases, dict)
        self.assertEqual(aliases['SUBDIR'], 'dir/subdir/')
        self.assertEqual(aliases['SUBDIR_2'], 'dir/subdir/some/other/dir/')
