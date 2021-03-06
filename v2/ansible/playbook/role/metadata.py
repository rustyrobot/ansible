# (c) 2014 Michael DeHaan, <michael@ansible.com>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from six import iteritems, string_types

from ansible.errors import AnsibleParserError
from ansible.playbook.attribute import Attribute, FieldAttribute
from ansible.playbook.base import Base
from ansible.playbook.role.include import RoleInclude


__all__ = ['RoleMetadata']


class RoleMetadata(Base):
    '''
    This class wraps the parsing and validation of the optional metadata
    within each Role (meta/main.yml).
    '''

    _allow_duplicates = FieldAttribute(isa='bool', default=False)
    _dependencies     = FieldAttribute(isa='list', default=[])
    _galaxy_info      = FieldAttribute(isa='GalaxyInfo')

    def __init__(self):
        self._owner = None
        super(RoleMetadata, self).__init__()

    @staticmethod
    def load(data, owner, loader=None):
        '''
        Returns a new RoleMetadata object based on the datastructure passed in.
        '''

        if not isinstance(data, dict):
            raise AnsibleParserError("the 'meta/main.yml' for role %s is not a dictionary" % owner.get_name())

        m = RoleMetadata().load_data(data, loader=loader)
        return m

    def _load_dependencies(self, attr, ds):
        '''
        This is a helper loading function for the dependencis list,
        which returns a list of RoleInclude objects
        '''

        assert isinstance(ds, list)

        deps = []
        for role_def in ds:
            i = RoleInclude.load(role_def, loader=self._loader)
            deps.append(i)

        return deps

    def _load_galaxy_info(self, attr, ds):
        '''
        This is a helper loading function for the galaxy info entry
        in the metadata, which returns a GalaxyInfo object rather than
        a simple dictionary.
        '''

        return ds
