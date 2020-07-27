import os
import logging
from sphero_sdk import SpheroRvrTargets
from sphero_sdk.common.firmware.cms_fw_check_base import CmsFwCheckBase

logger = logging.getLogger(__name__)


class RvrFwCheckAsync(CmsFwCheckBase):

    def __init__(self):
        CmsFwCheckBase.__init__(self)
        self.__rvr = self

    async def _check_rvr_fw(self):
        """Checks the RVR's firmware on the Nordic and ST chips against the CMS, if an internet connection is available.
        """
        root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../'))

        # Have more than 7 days elapsed since last check?
        if not self._should_run_fw_check():
            return

        if not self._network_available():
            self._write_timestamp()
            return

        print('Checking RVR firmware versions...')

        rvr_nordic_version = await self.__rvr.get_main_application_version(target=SpheroRvrTargets.primary.value, timeout=3)
        rvr_st_version = await self.__rvr.get_main_application_version(target=SpheroRvrTargets.secondary.value, timeout=3)

        if rvr_nordic_version is None or rvr_st_version is None:
            logger.error('Unable to retrieve Nordic and/or ST versions from RVR.')
            return

        print('Checking CMS firmware versions...')
        cms_nordic_version = await self._get_cms_fw_version(self._nordic_cms_url)
        logger.info('CMS Nordic Version:', cms_nordic_version)

        cms_st_version = await self._get_cms_fw_version(self._st_cms_url)
        logger.info('CMS ST Version:', cms_st_version)

        # Proceed only if both versions are acquired from the CMS.
        if cms_nordic_version is not None or cms_st_version is not None:

            # Record timestamp of this check
            self._write_timestamp()

            warning_displayed = self._check_update_available(rvr_nordic_version, cms_nordic_version)

            # Check ST version only if Nordic version check return false
            if not warning_displayed:
                self._check_update_available(rvr_st_version, cms_st_version)

        print('Firmware check complete.')





