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
from .dolibarr import Dolibarr
import time
import json
import logging

class DolibarrCached(Dolibarr):
    
    _cache = {}
    _cache_accessed = {}
    _max_cached_requests = 100
    _logger = logging.getLogger('bPortal')

    def __init__(self):
        super().__init__()

    def _call(self, method, url, params={}):
        cached_call = self._get_cached_call(method, url, params)
        if cached_call:
            return cached_call
        else:
            response = super(DolibarrCached, self)._call(method, url, params)
            self._add_call_to_cache(method, url, params, response)
            return response
        
    def _call_json(self, method, url, params={}):
        self._logger.debug(f"Attempting to fetch from cache: method={method}, url={url}, params={params}")
        cached_call = self._get_cached_call(method, url, params)
        if cached_call:
            return cached_call
        else:
            response = super(DolibarrCached, self)._call_json(method, url, params)
            self._add_call_to_cache(method, url, params, response)
            return response

    @staticmethod
    def _get_time():
        return time.time()

    def _get_oldest_accessed_cache_key(self):
        try:
            oldest_accessed = None
            for key, timestamp in self._cache_accessed.items():
                if oldest_accessed is None or timestamp < oldest_accessed[1]:
                    oldest_accessed = (key, timestamp)
            return oldest_accessed[0] if oldest_accessed else None
        except Exception as e:
            self._logger.error(f"Error getting oldest accessed cache key: {e}")
            return None

    def _remove_oldest_cached_requests(self):
        if len(self._cache) > self._max_cached_requests:
            oldest_accessed = self._get_oldest_accessed_cache_key()
            if oldest_accessed:
                del self._cache[oldest_accessed]
                del self._cache_accessed[oldest_accessed]

    def _add_call_to_cache(self, method, url, custom_parameters, response):
        try:
            key = (method, json.dumps(custom_parameters, sort_keys=True), url)
            self._cache[key] = response
            self._cache_accessed[key] = self._get_time()
            self._remove_oldest_cached_requests()
            return True
        except Exception as e:
            return False

    def _get_cached_call(self, method, url, custom_parameters):
        try:
            key = (method, json.dumps(custom_parameters, sort_keys=True), url)
            cached_response = self._cache[key]
            self._cache_accessed[key] = self._get_time()
            return cached_response
        except KeyError:
            return None
        except Exception as e:
            self._logger.error(f"Error retrieving from cache: {e}")
            return None

    def clear_cache(self):
        """
        This method clears all the information stored on the internal cache.
        """
        self._cache.clear()
        self._cache_accessed.clear()
        self._logger.info("Cache cleared")

    def get_number_of_cached_calls(self):
        """
        Get the number of cached calls.

        :return: number of cached calls.
        :rtype: int
        """
        return len(self._cache)
