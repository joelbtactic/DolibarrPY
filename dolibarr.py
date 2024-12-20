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

from .configd import ConfigD
from .singleton import Singleton
import requests
import logging
import json

class Dolibarr(metaclass=Singleton):
    conf = ConfigD()
    _logger = logging.getLogger('bPortal')

    def __init__(self):
        self._url = self.conf.url
        self._headers = self._get_headers()
        self._timeout = 16

    def _get_headers(self):
        return {
            'DOLAPIKEY': self.conf.api_token,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
    
    def _call(self, method, url, params={}):
        response = requests.request(method, url, params=params, headers=self._headers, timeout=self._timeout)
        try:
            result = json.loads(response.text)
        except:
            self._logger.error(f'Dolibarr API ERROR: {response.text}')
            raise Exception(response.text)
        return result
    
    def _call_json(self, method, url, params={}):
        response = requests.request(method, url, json=params, headers=self._headers, timeout=self._timeout)
        try:
            result = json.loads(response.text)
        except:
            self._logger.error(f'Dolibarr API ERROR: {response.text}')
            raise Exception(response.text)
        return result