# NBioBSP
Python API for Nitgen Hamster 1 with NBioBSP SDK
---

````
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

  def open_device(self, device_id=None):
      """
      Opens device for communication, keep device_id as None to auto-detect the device
      :param device_id: short unsigned int
      :return: True
      """

  def close_device(self, device_id=None):
      """
      Closes opened device, keep device_id as None to auto-detect the device
      :param device_id: short unsigned int
      :return: True
      """

  def check_finger(self):
      """
      Checks if a finger is present on the device to scan
      :return: bool
      """

  def capture(self):
      """
      Captures and returns fingerprint data
      :return: NBioAPI.Type.HFIR
      """

  def verify(self, finger):
      """
      Captures new fingerprint and matches it with stored fingerprint
      :param finger: NBioAPI.Type.HFIR
      :return: bool
      """

  def match(self, finger, ref_finger):
      """
      Checks if finger matches with reference finger
      :param finger: NBioAPI.Type.HFIR
      :param ref_finger: NBioAPI.Type.HFIR
      :return: bool
      """

  def hfir_to_fir_text_encode(self, finger, with_unicode=False, format=None):
      """
      Converts HFIR into text encoding
      :param finger: NBioBSP.Type.HFIR
      :return: NBioBSP.Type.FIR_TEXTENCODE
      """

  def str_to_fir_text_encode(self, text_encoding):
      """
      Converts text encoded fingerprint to HFIR
      :param text_encoding: NBioBSP.Type.FIR_TEXTENCODE
      :return: NBioBSP.Type.HFIR
      """
````
