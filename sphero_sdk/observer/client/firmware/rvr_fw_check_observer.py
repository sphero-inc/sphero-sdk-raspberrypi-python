import asyncio
import logging
from datetime import datetime
from sphero_sdk import SpheroRvrTargets
from sphero_sdk.common.firmware.cms_fw_check_base import CmsFwCheckBase

logger = logging.getLogger(__name__)


class RvrFwCheckObserver(CmsFwCheckBase):

    def __init__(self):
        CmsFwCheckBase.__init__(self)
        self.__rvr = self

    def _check_rvr_fw(self):
        """Checks the RVR's firmware on the Nordic and ST chips against the CMS, if an internet connection is available.
        """

        # Have more than 7 days elapsed since last check?
        if not self._should_run_fw_check():
            return

        print('Checking RVR firmware versions...')

        self.__rvr.get_main_application_version(handler=self.nordic_version_handler, target=SpheroRvrTargets.primary.value)
        self.__rvr.get_main_application_version(handler=self.st_version_handler, target=SpheroRvrTargets.secondary.value)

        # Block here while rvr versions are retrieved, timeout at 5 seconds.
        rvr_version_successful = self.wait_for_rvr_versions()

        if not rvr_version_successful:
            logger.error('Unable to retrieve Nordic and/or ST versions from RVR.')
            return

        print('Checking CMS firmware versions...')
        task = asyncio.ensure_future(self._get_cms_fw_version(self._nordic_cms_url))
        asyncio.get_event_loop().run_until_complete(task)
        cms_nordic_version = task.result()
        logger.info('CMS Nordic Version:', cms_nordic_version)

        task = asyncio.ensure_future(self._get_cms_fw_version(self._st_cms_url))
        asyncio.get_event_loop().run_until_complete(task)
        cms_st_version = task.result()
        logger.info('CMS ST Version:', cms_st_version)

        asyncio.get_event_loop().close()

        # Proceed only if both versions are acquired from the CMS.
        if cms_nordic_version is not None or cms_st_version is not None:

            # Record timestamp of this check
            self._write_timestamp()

            warning_displayed = self._check_update_available(self._rvr_nordic_version, cms_nordic_version)

            # Check ST version only if Nordic version check return false
            if not warning_displayed:
                self._check_update_available(self._rvr_st_version, cms_st_version)

        print('Firmware check done.')

    def wait_for_rvr_versions(self):
        initial_time = datetime.now()
        while self._rvr_nordic_version is None or self._rvr_st_version is None:
            time_delta = (datetime.now() - initial_time)

            # Loop is broken by timeout, Nordic and ST version acquisition from RVR was unsuccessful.
            if time_delta.seconds > 5:
                return False

        # Loop was broken by successful Nordic and ST version acquisition from RVR.
        return True

    def nordic_version_handler(self, response):
        logger.info('RVR Nordic Version:', response)
        self._rvr_nordic_version = response

    def st_version_handler(self, response):
        logger.info('RVR ST Version:', response)
        self._rvr_st_version = response




