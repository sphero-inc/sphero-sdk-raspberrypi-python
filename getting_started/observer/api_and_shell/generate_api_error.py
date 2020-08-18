import os
import sys
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sphero_sdk import SpheroRvrObserver
from sphero_sdk import SpheroRvrTargets
from sphero_sdk import ApiResponseCodesEnum
from sphero_sdk.common.log_level import LogLevel

rvr = SpheroRvrObserver(log_level=LogLevel.Debug_Verbose)


def main():
    """ This sample uses the generate_api_error command to intentionally generate an error response from RVR
        with the specified response code. Under normal circumstances certain commands request a response from RVR.
        If an error response is detected then it can be handled by the SDK's response logic.  However, if a
        command does not have expected output, and therefore doesn't request a response (e.g. drive_with_heading),
        then RVR does not generate an error response if one occurs.  Setting the request_error_responses_only flag
        on RVR will enable it to generate error responses even if no output is expected, and give a program the
        ability to catch any of the following 10 error response codes:

        Response Code 0x00: success
        Response Code 0x01: bad_did
        Response Code 0x02: bad_cid
        Response Code 0x03: not_yet_implemented
        Response Code 0x04: restricted
        Response Code 0x05: bad_data_length
        Response Code 0x06: failed
        Response Code 0x07: bad_data_value
        Response Code 0x08: busy
        Response Code 0x09: bad_tid (bad target id)
        Response Code 0x0A: target_unavailable

        Note a response code of 0x00 indicates a successful command, and is therefore is not considered an error.
    """
    try:
        # Since the generate_api_error command doesn't expect any output, the enable_error_responses_only flag must
        # be set True in order for RVR to generate an error.  This flag will remain true until otherwise specified,
        # or when the program terminates.
        rvr.request_error_responses_only = True

        rvr.generate_api_error(
            error=ApiResponseCodesEnum.bad_cid,  # Specify code 0x01 - 0x0A to receive that specific error response from RVR.
            target=SpheroRvrTargets.secondary.value,
            timeout=3
        )

        # Sleep for one second such that RVR has time to send data back
        time.sleep(1)
    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')
    except Exception:
        print("ERROR ERROR ERROR")
    finally:
        rvr.close()


if __name__ == '__main__':
    main()
