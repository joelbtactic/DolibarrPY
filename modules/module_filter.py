#######################################################################
# Dolibarr PY is a simple Python client for Dolibarr API.

# Copyright (C) 2023-2024 BTACTIC, SCCL
# Copyright (C) 2023-2024 Joel Ampurdanés Bonjoch

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#######################################################################

from dataclasses import dataclass
from typing import Optional

@dataclass
class ModuleFilter():
    sortfield: Optional[str] = 't.rowid'
    sortorder: Optional[str] = 'ASC'
    limit: Optional[int] = 20
    page: Optional[int] = 0
    thirdparty_ids: Optional[str] = None
    sqlfilters: Optional[str] = None    
    pagination_data: Optional[bool] = True  
    type: Optional[str] = None

    def update_value(self, values):
        for key, value in values.items():
            if key == 'sortfield':
                self.sortfield = str(value)
            elif key == 'sortorder':
                self.sortorder = str(value)
            elif key == 'limit':
                self.limit = int(value)
            elif key == 'page':
                self.page = int(value)
            elif key == 'thirdparty_ids':
                self.thirdparty_ids = str(value)
            elif key == 'sqlfilters':
                self.sqlfilters = str(value)
            elif key == 'pagination_data':
                self.pagination_data = value
            elif key == 'type':
                self.type = value
