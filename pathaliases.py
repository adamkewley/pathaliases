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
import yaml


def resolve_yaml_to_path_strings(yaml_path, alias_key='alias'):
    with open(yaml_path, 'r') as f:
        aliases_dict = yaml.load(f)
        return resolve_path_strings(aliases_dict, alias_key)


def resolve_path_strings(alias_tree, alias_key='alias'):
    path_lists = resolve_path_lists(alias_tree, alias_key)

    return {k: "".join(v) for k, v in path_lists.items()}


def resolve_path_lists(alias_tree, alias_key='alias'):
    h = {}
    _resolve_node(alias_tree, alias_key, [], h)
    return h


def _resolve_node(node, alias_key, previous_keys, resolved_keys):
    if isinstance(node, dict):
        _resolve_dict(node, alias_key, previous_keys, resolved_keys)
    elif isinstance(node, list):
        _resolve_list(node, alias_key, previous_keys, resolved_keys)
    else:
        _resolve_leaf(node, alias_key, previous_keys, resolved_keys)


def _resolve_dict(d, alias_key, previous_keys, resolved_keys):
    for k, v in d.items():
        _resolve_node(v, alias_key, previous_keys + [k], resolved_keys)


def _resolve_list(lst, alias_key, previous_keys, resolved_keys):
    for item in lst:
        _resolve_node(item, alias_key, previous_keys, resolved_keys)


def _resolve_leaf(leaf, alias_key, previous_keys, resolved_keys):
    if len(previous_keys) > 0 and previous_keys[-1] == alias_key:
        leaf_str = str(leaf)
        if leaf_str in resolved_keys:
            raise RuntimeError("%s: already exists" % leaf_str)
        else:
            resolved_keys[leaf_str] = previous_keys[0:-1]
