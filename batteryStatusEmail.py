import ctypes
import os
import smtplib
from ctypes import wintypes


# Retrieving all components related to power status
class SYSTEM_POWER_STATUS(ctypes.Structure):
    _fields_ = [
        ('ACLineStatus', wintypes.BYTE),
        ('BatteryFlag', wintypes.BYTE),
        ('BatteryLifePercent', wintypes.BYTE),
        ('Reserved1', wintypes.BYTE),
        ('BatteryLifeTime', wintypes.DWORD),
        ('BatteryFullLifeTime', wintypes.DWORD),
    ]

SYSTEM_POWER_STATUS_P = ctypes.POINTER(SYSTEM_POWER_STATUS)
GetSystemPowerStatus = ctypes.windll.kernel32.GetSystemPowerStatus
GetSystemPowerStatus.argtypes = [SYSTEM_POWER_STATUS_P]
GetSystemPowerStatus.restype = wintypes.BOOL

status = SYSTEM_POWER_STATUS()

if not GetSystemPowerStatus(ctypes.pointer(status)):
    raise ctypes.WinError()

batteryPercentage = status.BatteryLifePercent

if batteryPercentage < 50:

    # Retrieving user login details
    username = os.environ.get('PYTHON_EMAIL_ADDRESS')
    password = os.environ.get('PYTHON_EMAIL_PASSWORD')

    receiverEmail = os.environ.get('PYTHON_RECEIVER_EMAIL_ADDRESS')

    server = smtplib.SMTP('imap.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username, password)

    if batteryPercentage < 30:
        server.sendmail(username, receiverEmail, "CRITICAL !!!!!! Battery Percentage " + str(batteryPercentage))
    else:
        server.sendmail(username, receiverEmail, "Battery Percentage " + str(batteryPercentage))

    server.close()

