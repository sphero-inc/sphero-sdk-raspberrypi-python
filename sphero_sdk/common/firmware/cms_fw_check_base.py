import os
import aiohttp
import asyncio
import urllib
from urllib import request
from urllib import error
from datetime import datetime
from aiohttp import ClientSession


class CmsFwCheckBase:

    __slots__ = ['__root_path',
                 '_nordic_cms_url',
                 '_st_cms_url',
                 '_rvr_nordic_version',
                 '_rvr_st_version',
                 '__major_key',
                 '__minor_key',
                 '__revision_key',
                 '__versions_key']

    def __init__(self):
        self.__root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
        self._nordic_cms_url = 'https://cms-api-production.platform.sphero.com/api/v1/products/rvr/content_packs/nordic_mainapp_ota/versions/published'
        self._st_cms_url = 'https://cms-api-production.platform.sphero.com/api/v1/products/rvr/content_packs/st_mainapp_ota/versions/published'
        self._rvr_nordic_version = None
        self._rvr_st_version = None
        self.__major_key = 'major'
        self.__minor_key = 'minor'
        self.__revision_key = 'revision'
        self.__versions_key = 'versions'

    def _should_run_fw_check(self):
        try:
            with open('{}/.fw'.format(self.__root_path), mode='r+') as file:
                cached_timestamp = float(file.read())
                cached_datetime = datetime.fromtimestamp(cached_timestamp)
                time_delta = (datetime.now() - cached_datetime)
                return time_delta.days > 7

        except (ValueError, FileNotFoundError) as e:
            return True

    def _network_available(self):
        try:
            urllib.request.urlopen("https://google.com")
        except urllib.error.URLError:
            print("No network available")
            return False
        else:
            print("Network available")
            return True

    def _check_update_available(self, rvr_version, cms_version):

        if rvr_version[self.__major_key] < cms_version[self.__major_key] or \
                rvr_version[self.__minor_key] < cms_version[self.__minor_key] or \
                rvr_version[self.__revision_key] < cms_version[self.__revision_key]:
            self.__log_fw_warning()
            return True

        return False

    async def _get_cms_fw_version(self, url):
        try:
            session = ClientSession(raise_for_status=True)
            response = await session.request(
                method='GET',
                url=str(url),
                timeout=10
            )

        except aiohttp.ClientResponseError:
            print('CMS Response Error')
            return None

        except aiohttp.ClientConnectionError:
            print('CMS Request Connection Error')
            return None

        except asyncio.TimeoutError:
            print('CMS Request Timed Out!')
            return None

        try:
            response_json = await response.json()

        except Exception:
            print('Error getting JSON!')
            return None

        await session.close()

        version_string = response_json[self.__versions_key][-1]
        version_array = version_string.split('.')
        response_dictionary = {
            self.__major_key: int(version_array[0]),
            self.__minor_key: int(version_array[1]),
            self.__revision_key: int(version_array[2])
        }

        return response_dictionary

    def _write_timestamp(self):
        with open('{}/.fw'.format(self.__root_path), 'w') as file:
            now = datetime.now()
            file.write(str(datetime.timestamp(now)))
            file.close()

    def __log_fw_warning(self):
        print('=====================================================')
        print('===== A NEWER VERSION OF FIRMWARE IS AVAILABLE ======')
        print('=====================================================')
        print('If you would like to update your unit, connect RVR to')
        print('the Sphero EDU app to install the latest firmware.')
        print('=====================================================')
        print('\nPress any key to continue...')
        input()


