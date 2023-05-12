import os
import clr


class NBioBSP:
    """
    Python API for NITGEN HAMSTER 1
    using NITGEN.SDK.NBioBSP.dll written in .NET 3.5 64bit
    and NBioBSP.dll (main library)
    """

    def __init__(self):
        """
        Initializes .NET runtime and loads SDK DLL as Python library
        Required files:
            NITGEN.SDK.NBioBSP.dll
            NBioBSP.dll
        """
        sdk = os.path.join(os.path.dirname(__file__), "NITGEN.SDK.NBioBSP.dll")
        n_bio_api = os.path.join(os.path.dirname(__file__), "NBioBSP.dll")

        def error_text(file):
            return f"Required DLL file {file} not found"

        if not os.path.exists(sdk):
            raise FileNotFoundError(error_text(sdk))

        if not os.path.exists(n_bio_api):
            raise FileNotFoundError(error_text(n_bio_api))

        clr.AddReference(sdk)
        from NITGEN.SDK.NBioBSP import NBioAPI

        self.api = NBioAPI()

    def _handle_return(self, return_code):
        if return_code == 0:
            return True
        raise Exception(self.api.Error.GetErrorDescription(return_code))

    def _handle_device(self, do_open: bool = True, device_id: int = None):
        if not device_id:
            device_id = self.api.Type.DEVICE_ID.AUTO
        return self._handle_return(self.api.OpenDevice(device_id) if do_open else self.api.CloseDevice(device_id))

    def _verify_core(self, finger_1, finger_2=None):
        ret, is_same = self.api.VerifyMatch(finger_1, finger_2, bool(), self.api.Type.FIR_PAYLOAD()) if finger_2 else \
            self.api.Verify(finger_1, bool(), self.api.Type.FIR_PAYLOAD())
        if self._handle_return(ret):
            return is_same

    def open_device(self, device_id=None):
        """
        Opens device for communication, keep device_id as None to auto-detect the device
        :param device_id: short unsigned int
        :return: True
        """
        return self._handle_device(True, device_id)

    def close_device(self, device_id=None):
        """
        Closes opened device, keep device_id as None to auto-detect the device
        :param device_id: short unsigned int
        :return: True
        """
        return self._handle_device(False, device_id)

    def check_finger(self):
        """
        Checks if a finger is present on the device to scan
        :return: bool
        """
        ret, is_present = self.api.CheckFinger()
        if self._handle_return(ret):
            return is_present

    def capture(self):
        """
        Captures and returns fingerprint data
        :return: NBioAPI.Type.HFIR
        """
        ret, HFIR = self.api.Capture()
        if self._handle_return(ret):
            return HFIR

    def verify(self, finger):
        """
        Captures new fingerprint and matches it with stored fingerprint
        :param finger: NBioAPI.Type.HFIR
        :return: bool
        """
        return self._verify_core(finger)

    def match(self, finger, ref_finger):
        """
        Checks if finger matches with reference finger
        :param finger: NBioAPI.Type.HFIR
        :param ref_finger: NBioAPI.Type.HFIR
        :return: bool
        """
        return self._verify_core(finger, ref_finger)

    def hfir_to_fir_text_encode(self, finger, with_unicode=False, format=None):
        """
        Converts HFIR into text encoding
        :param finger: NBioBSP.Type.HFIR
        :return: NBioBSP.Type.FIR_TEXTENCODE
        """
        ret, fir_text_encode = self.api.GetTextFIRFromHandle(finger, self.api.Type.FIR_TEXTENCODE(), with_unicode,
                                      (format or self.api.Type.FIR_FORMAT.STANDARD))
        if self._handle_return(ret):
            return fir_text_encode

    def str_to_fir_text_encode(self, text_encoding):
        """
        Converts text encoded fingerprint to HFIR
        :param text_encoding: NBioBSP.Type.FIR_TEXTENCODE
        :return: NBioBSP.Type.HFIR
        """
        temp = self.api.Type.FIR_TEXTENCODE()
        temp.TextFIR = text_encoding
        return temp


if __name__ == "__main__":

    # Initialize API
    api = NBioBSP()

    # Open Device
    api.open_device()

    # Checks if finger is placed on the scanner
    # print(api.check_finger())

    # Captures fingerprint
    # f = api.capture()
    # rf = api.capture()
    # texen = api.hfir_to_fir_text_encode(rf)
    # print(texen.TextFIR)
    #
    #
    # Converts fingerprint to text encoding
    tfir = (api.str_to_fir_text_encode('AQAAABQAAAA0AQAAAQASAAEAZAAAAAAAMAEAAK9ZM3/XQL*193UJZg2o0Ub6F18jUnjt9afBvOZ1zRD0SfmrAeVW3MB2cvx3*HAtBPOhesdJxZtiJBzcdOSdNQsjeCsS2FcyUTwtWx0/r*IfvVReiTI5YG5cy3sfngHJj0pG*2T7ijine6kVeESYTq*DluY1id1kDo6sHMlrWdDOmJIHYL3lhSwlR/TJRpSqUwGykwZxk77hLEbc72ZhI96E4eCM*x*ynzgC/wmAT*xMtF4FBSFNp*iLhsOamzDj5YKBQ/4XEw/KUUSQyL6tE9cptTZK/AonblbVHOys*BpN31f5cBM5437FTVReZuccd5Y2H5s*mpkBH2W7gAGLYZqEIii64LR95LA8ietdNkKpcqhzeQQ3zk88nWEu*xIgyGv7Yl76owxpAYVN0i2cSuQ'))
    print(tfir)
    # Matches two fingerprints
    # ff = api.capture()
    # print(api.api.GetQualityInfo(None, None, None)[1].Quality)
    print(api.verify(tfir))

    # Closes the device
    api.close_device()
