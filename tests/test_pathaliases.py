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
import unittest

import pathaliases


class TestPathaliases(unittest.TestCase):
    def test_resolve_path_strings_returns_empty_dict_when_given_empty_dict(self):
        self.assertEqual(pathaliases.resolve_path_strings({}), {})

    def test_resolve_path_strings_returns_expected_dict_for_trivial_input(self):
        trivial_input = {
            "k1": {
                "k2": {
                    "alias": "v1",
                }
            }
        }

        output = pathaliases.resolve_path_strings(trivial_input)
        expected_output = {"v1": "k1k2"}
        self.assertEqual(output, expected_output)

    def test_resolve_path_lists_returns_expected_dict_for_trivial_input(self):
        trivial_input = {
            "k1": {
                "k2": {
                    "alias": "v1",
                }
            }
        }

        output = pathaliases.resolve_path_lists(trivial_input)
        expected_output = {"v1": ["k1", "k2"]}
        self.assertEqual(output, expected_output)

    def test_resolve_path_strings_returns_expected_dict_for_trivial_input_and_custom_alias_key(self):
        alternate_key = "aliaskey"
        trivial_input = {
            "k1": {
                "k2": {
                    alternate_key: "v1",
                }
            }
        }

        output = pathaliases.resolve_path_strings(trivial_input, alias_key=alternate_key)
        expected_output = {"v1": "k1k2"}
        self.assertEqual(output, expected_output)

    def test_resolve_path_lists_returns_expected_dict_for_trivial_input_and_custom_alias_key(self):
        alternate_key = "aliaskey"
        trivial_input = {
            "k1": {
                "k2": {
                    alternate_key: "v1",
                }
            }
        }

        output = pathaliases.resolve_path_lists(trivial_input, alias_key=alternate_key)
        expected_output = {"v1": ["k1", "k2"]}
        self.assertEqual(output, expected_output)

    def test_resolve_path_strings_returns_empty_dict_if_no_keys_are_alias(self):
        input_containing_no_aliases = {
            "k1": {
                "k2": "v1",
                "k3": "v2",
                "k4": {
                    "k5": "v3",
                }
            }
        }

        output = pathaliases.resolve_path_strings(input_containing_no_aliases)
        self.assertEqual(output, {})

    def test_resolve_path_lists_returns_empty_dict_if_no_keys_are_alias(self):
        input_containing_no_aliases = {
            "k1": {
                "k2": "v1",
                "k3": "v2",
                "k4": {
                    "k5": "v3",
                }
            }
        }

        output = pathaliases.resolve_path_lists(input_containing_no_aliases)
        self.assertEqual(output, {})

    def test_resolve_path_lists_returns_aliases_even_if_dict_contains_other_data(self):
        input_with_extra_data = {
            "k1": {
                "k2": "v1",
                "k3": {
                    "k4": "v2",
                    "k5": {
                        "alias": "v3",
                    }
                }
            }
        }

        output = pathaliases.resolve_path_lists(input_with_extra_data)
        expected_output = {"v3": ["k1", "k3", "k5"]}
        self.assertEqual(output, expected_output)

    def test_resolve_path_strings_returns_aliases_on_the_root(self):
        input_root = {
            "alias": "v1",
        }

        output = pathaliases.resolve_path_strings(input_root)
        expected_output = {"v1": ""}
        self.assertEqual(output, expected_output)

    def test_resolve_path_lists_returns_empty_array_for_root_alias(self):
        input_root = {
            "alias": "v1",
        }

        output = pathaliases.resolve_path_lists(input_root)
        expected_output = {"v1": []}
        self.assertEqual(output, expected_output)

    def test_resolve_path_lists_returns_aliases_from_alias_array(self):
        input_with_array = {
            "k1": {
                "alias": [
                    "v1",
                    "v2",
                ]
            }
        }

        output = pathaliases.resolve_path_lists(input_with_array)
        expected_output = {"v1": ["k1"], "v2": ["k1"]}
        self.assertEqual(output, expected_output)

    def test_resolve_path_lists_returns_aliases_from_nested_alias_arrays(self):
        input_with_nesting = {
            "k1": {
                "k2": "v1",
                "k3": [
                    {"k4": {"alias": "v2"}},
                    [
                        {"k5": {"alias": "v3"}},
                    ],
                    "v4"
                ],
                "k6": {
                    "k7": [
                        {"alias": "v5"},
                    ]
                }
            }
        }

        output = pathaliases.resolve_path_lists(input_with_nesting)
        expected_output = {
            "v2": ["k1", "k3", "k4"],
            "v3": ["k1", "k3", "k5"],
            "v5": ["k1", "k6", "k7"],
        }
        self.assertEqual(output, expected_output)

    def test_resolve_path_strings_returns_empty_hash_if_provided_array(self):
        output = pathaliases.resolve_path_strings([])
        self.assertEqual(output, {})

    def test_resolve_path_lists_root_array_works_as_expected(self):
        input_array = [
            {"alias": "v1"},
            "v2",
            {"k1": {
                "k2": {"alias": "v3"},
                "k3": [
                    {"alias": "v4"},
                    "v5",
                    {"k4": {"alias": "v6"}},
                ]
            }}
        ]

        output = pathaliases.resolve_path_lists(input_array)

        expected_output = {
            "v1": [],
            "v3": ["k1", "k2"],
            "v4": ["k1", "k3"],
            "v6": ["k1", "k3", "k4"],
        }

        self.assertEqual(output, expected_output)

    def test_resolve_throws_if_dict_contains_duplicate_aliases(self):
        input_with_duplicate_aliases = {
            "k1": {"alias": "v1"},
            "k2": {"alias": "v1"},
        }

        with self.assertRaises(RuntimeError):
            pathaliases.resolve_path_strings(input_with_duplicate_aliases)

    def test_resolve_throws_if_dict_contains_deeply_nested_duplicate_aliases(self):
        input_with_duplicate_aliases = {
            "k1": {"alias": "v1"},
            "k2": {
                "k3": {
                    "k4": [
                        {"alias": "v1"},
                    ]
                }
            }
        }

        with self.assertRaises(RuntimeError):
            pathaliases.resolve_path_strings(input_with_duplicate_aliases)

    def test_resolve_path_strings_resolves_variables_in_root_keys_if_provided_an_environment(self):
        input_containing_unresolved_variables = {
            "${var1}": {
                "alias": "v1",
            }
        }

        env = {
            "var1": "k1",
        }

        result = pathaliases.resolve_path_strings(input_containing_unresolved_variables, env=env)

        expected_result = {
            "v1": "k1",
        }

        self.assertEqual(result, expected_result)

    def test_resolve_path_lists_resolves_variables_in_root_keys_if_provided_environment(self):
        input_containing_unresolved_variables = {
            "${var1}": {
                "alias": "v1",
            }
        }

        env = {
            "var1": "k1",
        }

        result = pathaliases.resolve_path_lists(input_containing_unresolved_variables, env=env)

        expected_result = {
            "v1": ["k1"],
        }

        self.assertEqual(result, expected_result)

    def test_resolve_path_strings_resolves_varibles_in_root_values_if_provided_an_environment(self):
        input_containing_unresolved_variables = {
            "k1": {
                "alias": "${var1}",
            }
        }

        env = {
            "var1": "v1",
        }

        result = pathaliases.resolve_path_strings(input_containing_unresolved_variables, env=env)

        expected_result = {
            "v1": "k1",
        }

        self.assertEqual(result, expected_result)

    def test_resolve_path_lists_resolves_variables_in_root_values_if_provided_an_environment(self):
        input_containing_unresolved_variables = {
            "k1": {
                "alias": "${var1}",
            }
        }

        env = {
            "var1": "v1",
        }

        result = pathaliases.resolve_path_lists(input_containing_unresolved_variables, env=env)

        expected_result = {
            "v1": ["k1"],
        }

        self.assertEqual(result, expected_result)

    def test_resolve_path_stings_resolves_nested_dictionary_variables(self):
        input_containing_nested_variables = {
            "k1": {
                "k2": {
                    "${var1}": {
                        "alias": "${var2}",
                    }
                }
            }
        }

        env = {
            "var1": "k3",
            "var2": "v1",
        }

        result = pathaliases.resolve_path_strings(input_containing_nested_variables, env=env)

        expected_result = {
            "v1": "k1k2k3",
        }

        self.assertEqual(result, expected_result)

    def test_resolve_path_lists_resolves_nested_dictionary_variables(self):
        input_containing_nested_variables = {
            "k1": {
                "k2": {
                    "${var1}": {
                        "alias": "${var2}",
                    }
                }
            }
        }

        env = {
            "var1": "k3",
            "var2": "v1",
        }

        result = pathaliases.resolve_path_lists(input_containing_nested_variables, env=env)

        expected_result = {
            "v1": ["k1", "k2", "k3"],
        }

        self.assertEqual(result, expected_result)

    def test_resolve_path_lists_resolves_nested_array_variables(self):
        input_containing_nested_variables_in_array = {
            "k1": {
                "k2": {
                    "alias": [
                        "${var1}"
                    ]
                }
            }
        }

        env = {
            "var1": "v1",
        }

        result = pathaliases.resolve_path_lists(input_containing_nested_variables_in_array, env=env)

        expected_result = {
            "v1": ["k1", "k2"],
        }

        self.assertEqual(result, expected_result)

    def test_resolve_works_with_numeric_values_in_env(self):
        input_containing_unresolved_variables = {
            "k1": {
                "alias": "${var1}",
            }
        }

        env = {
            "var1": 1,
        }

        result = pathaliases.resolve_path_lists(input_containing_unresolved_variables, env=env)

        expected_result = {
            "1": ["k1"],
        }

        self.assertEqual(result, expected_result)
