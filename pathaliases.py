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
import re

import yaml


def resolve_yaml_to_path_strings(yaml_path, alias_key='alias', env={}):
    with open(yaml_path, 'r') as f:
        aliases_dict = yaml.load(f)
        return resolve_path_strings(aliases_dict, alias_key, env)


def resolve_path_strings(alias_tree, alias_key='alias', env={}):
    path_lists = resolve_path_lists(alias_tree, alias_key, env)

    return {k: "".join(v) for k, v in path_lists.items()}


def resolve_path_lists(alias_tree, alias_key='alias', env={}):
    h = {}
    _resolve_node(alias_tree, alias_key, [], h, env)
    return h


def _resolve_node(node, alias_key, previous_keys, resolved_keys, env):
    if isinstance(node, dict):
        _resolve_dict(node, alias_key, previous_keys, resolved_keys, env)
    elif isinstance(node, list):
        _resolve_list(node, alias_key, previous_keys, resolved_keys, env)
    else:
        _resolve_leaf(node, alias_key, previous_keys, resolved_keys, env)


def _resolve_dict(d, alias_key, previous_keys, resolved_keys, env):
    for k, v in d.items():
        new_tail = [_substitute_variables_in(k, env)]
        _resolve_node(v, alias_key, previous_keys + new_tail, resolved_keys, env)


def _substitute_variables_in(s, env):
    ret = s
    for var_name, var_val in env.items():
        var_regex = re.compile("\${\s*%s\s*}" % var_name)
        ret = var_regex.sub(str(var_val), ret)
    return ret


def _resolve_list(lst, alias_key, previous_keys, resolved_keys, env):
    for item in lst:
        _resolve_node(item, alias_key, previous_keys, resolved_keys, env)


def _resolve_leaf(leaf, alias_key, previous_keys, resolved_keys, env):
    if len(previous_keys) > 0 and previous_keys[-1] == alias_key:
        _resolve_alias(str(leaf), previous_keys, resolved_keys, env)


def _resolve_alias(alias, previous_keys, resolved_keys, env):
    substituted_alias = _substitute_variables_in(alias, env)

    if substituted_alias in resolved_keys:
        raise RuntimeError("%s: already exists" % substituted_alias)
    else:
        resolved_keys[substituted_alias] = previous_keys[0:-1]
