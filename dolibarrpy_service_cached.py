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

from dataclasses import asdict
from .modules.module_filter import ModuleFilter
from .dolibarr_bean import DolibarrBean
from .dolibarrpy_cached import DolibarrCached
import re
from django.utils import translation
class DolibarrApiServiceCached(DolibarrCached):

    def __init__(self):
        super(DolibarrApiServiceCached, self).__init__()

    def get_all_records(self, module_name = '', filters = None):
        """
        @endpoint get all /<module_name>
        @param module_name: Name of the module
        @param filters: Dictionary with the filters to apply
        @return: list of a records
        """
        if filters is None:
            search_filter = ModuleFilter()
        else:
            search_filter = ModuleFilter()
            search_filter.update_value(filters)
        current_page, last_page = search_filter.page, search_filter.page
        limit = search_filter.limit
        data = None
        params = asdict(search_filter)
        url = self._url + module_name
        response = self._call('get', url, params)
        if 'pagination' in response:
            current_page = response['pagination']['page']
            last_page = response['pagination']['page_count'] - 1
            limit = response['pagination']['limit']
            data = self._get_response_data(response['data'])
        else:
            data = self._get_response_data(response)

        list_of_bean = []
        for record in data:
            list_of_bean.append(DolibarrBean(module_name, record))
        return {
            "entry_list": list_of_bean,
            "result_count": len(list_of_bean),
            "previous_offset": current_page - 1 if current_page != 0 else None,
            "current_offset": current_page,
            "next_offset": current_page + 1 if last_page != current_page else None,
            "current_limit": limit,
            "last_page": last_page
        }   
    
    def _get_response_data(self, data):
        for record in data:
            if 'array_options' in record and record['array_options'] != []:
                for extrafield, value in record['array_options'].items():
                    extrafield = extrafield.replace("options_", "")
                    record[extrafield] = value
        return data
     
    def get_record_by_id(self, module_name, id, action = None):
        """
        @endpoint get record id /<module_name>/<id>
        @param module_name: Name of the module
        @param id: Id of the record
        @return: record
        """
        response_lst = []

        url = self._url + module_name + '/' + str(id)
        response = self._call('get' , url)
        response_lst.append(response)
        response = self._get_response_data(response_lst)[0]
        relationship_list = None 
        if action:
            relationship_list = self.get_relationship_action(module_name, id, action)
        bean = DolibarrBean(module_name.capitalize(), response, relationship_list, relationship_name=action)
        return bean
    
    def get_module_fields(self, module_name, extrafield = False, extrafield_module = ''):
        """
        @endpoint get module fields /get<module>fields/
        @param module_name: Name of the module
        @return list of fields
        """
        url = self._url + module_name + '/get' + module_name + 'fields'
        current_language = translation.get_language()
        params = {
            'lang': current_language
        }
        response = self._call('get' , url, params)
        if extrafield:
            self._get_extrafields(extrafield_module, response)
        
        for field_name, field_def in response.items():
            if 'name' not in field_def:
                field_def['name'] = field_name
        
        return response
    
    def _get_extrafields(self, extrafield_module, data):
        url = self._url + 'setup/extrafields'
        search_filter = ModuleFilter()
        search_filter.update_value({'type': extrafield_module})
        params = asdict(search_filter)
        response = self._call('get', url, params)[extrafield_module]
        for key, value in response.items():
            value['extrafield'] = True
            data[key] = value
    
    def get_relationship_action(self, module_name, id, action):
        url = self._url + module_name + '/' + str(id) + "/" + action
        response = self._call('get' , url)
        return response
    
    def get_document_pdf(self, module_area, doc_file):
        url = self._url + 'documents' + '/' + 'download'
        doc_path = self._get_doc_path_format(doc_file)

        param = {
            'modulepart': module_area,
            'original_file': doc_path
        }
        response = self._call('get', url, param)
        return response

    def _get_doc_path_format(self, doc_file):
        # Define the regular expression pattern
        pattern = r'/([^/]+/[^/]+\.pdf)$'

        # Search for the pattern in the input string
        match = re.search(pattern, doc_file)

        # Check if a match was found
        if match:
            # Extract the matched part
            result = match.group(1)
            return result
        else:
            return ''
        
    def save_record(self, module_name, id, params, action = None):
        response_lst = []
        url = self._url + module_name + '/' + str(id)
        if action:
            url += '/' + action
        response = self._call_json('put' , url, params)
        response_lst.append(response)
        response = self._get_response_data(response_lst)[0]
        relationship_list = None 
        if action:
            relationship_list = self.get_relationship_action(module_name, id, action)
        bean = DolibarrBean(module_name.capitalize(), response, relationship_list, relationship_name=action)
        return bean
    
    def create_record(self, module_name, params):
        url = self._url + module_name 
        response = self._call_json('post' , url, params)

        bean = DolibarrBean(module_name.capitalize(), params)
        bean['id'] = response
        return bean
