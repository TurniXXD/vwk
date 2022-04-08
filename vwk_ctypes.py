import ctypes
from ctypes import wintypes
import time
user32 = ctypes.WinDLL('user32', use_last_error=True)
INPUT_KEYBOARD = 1
KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP       = 0x0002
KEYEVENTF_UNICODE     = 0x0004
MAPVK_VK_TO_VSC = 0
# msdn.microsoft.com/en-us/library/dd375731
wintypes.ULONG_PTR = wintypes.WPARAM
class MOUSEINPUT(ctypes.Structure):
    _fields_ = (("dx",          wintypes.LONG),
                ("dy",          wintypes.LONG),
                ("mouseData",   wintypes.DWORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))
class KEYBDINPUT(ctypes.Structure):
    _fields_ = (("wVk",         wintypes.WORD),
                ("wScan",       wintypes.WORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))
    def __init__(self, *args, **kwds):
        super(KEYBDINPUT, self).__init__(*args, **kwds)
        if not self.dwFlags & KEYEVENTF_UNICODE:
            self.wScan = user32.MapVirtualKeyExW(self.wVk,
                                                 MAPVK_VK_TO_VSC, 0)
class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (("uMsg",    wintypes.DWORD),
                ("wParamL", wintypes.WORD),
                ("wParamH", wintypes.WORD))
class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = (("ki", KEYBDINPUT),
                    ("mi", MOUSEINPUT),
                    ("hi", HARDWAREINPUT))
    _anonymous_ = ("_input",)
    _fields_ = (("type",   wintypes.DWORD),
                ("_input", _INPUT))
LPINPUT = ctypes.POINTER(INPUT)
def PressKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))
def ReleaseKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode,
                            dwFlags=KEYEVENTF_KEYUP))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

def toKeyCode(c):
    keyCode = keyCodeMap[c[0]]
    return int(keyCode, base=16)

keyCodeMap = {
    ' '                 : "0x20",
    ','                 : "0xBC",
    '.'                 : "0xBE",
    '-'                 : "0xBF",
    ')'                 : "0xE2",
    '0'                 : "0x30",
    '1'                 : "0x31",
    '2'                 : "0x32",
    '3'                 : "0x33",
    '4'                 : "0x34",
    '5'                 : "0x35",
    '6'                 : "0x36",
    '7'                 : "0x37",
    '8'                 : "0x38",
    '9'                 : "0x39",
    'a'                 : "0x41",
    'b'                 : "0x42",
    'c'                 : "0x43",
    'd'                 : "0x44",
    'e'                 : "0x45",
    'f'                 : "0x46",
    'g'                 : "0x47",
    'h'                 : "0x48",
    'i'                 : "0x49",
    'j'                 : "0x4A",
    'k'                 : "0x4B",
    'l'                 : "0x4C",
    'm'                 : "0x4D",
    'n'                 : "0x4E",
    'o'                 : "0x4F",
    'p'                 : "0x50",
    'q'                 : "0x51",
    'r'                 : "0x52",
    's'                 : "0x53",
    't'                 : "0x54",
    'u'                 : "0x55",
    'v'                 : "0x56",
    'w'                 : "0x57",
    'x'                 : "0x58",
    'y'                 : "0x59",
    'z'                 : "0x5A",
    'ě'                 : "0x32",
    'š'                 : "0x33",
    'č'                 : "0x34",
    'ď'                 : "0x44",
    'ť'                 : "0x54",
    'ň'                 : "0x4E",
    'ř'                 : "0x35",
    'ž'                 : "0x36",
    'ý'                 : "0x37",
    'á'                 : "0x38",
    'í'                 : "0x39",
    'é'                 : "0x30",
    'ó'                 : "0x4F",
    'ú'                 : "0xDB",
    'ů'                 : "0xBA"
}

VK_SHIFT = 0x10
VK_CAPS = 0x14
VK_SPECIAL = 0xBF

typeSpeed = 0.1
print("Enter text for vwk: ", end='')
text = str(input())
print("Enter vwk type speed (default "+str(typeSpeed)+"s): ", end='')
i = input()
if i:
    typeSpeed = float(i)

def useKey(key):
    keyCode = toKeyCode(key)
    PressKey(keyCode)
    time.sleep(typeSpeed)
    ReleaseKey(keyCode)
print("Prepare cursor on input field...")

time.sleep(5)

print("Starting vwk...")

for k in range(len(text)):
    if not text[k].isupper():
        if text[k] == "ó":
            PressKey(VK_SPECIAL)
            useKey(text[k])
            ReleaseKey(VK_SPECIAL)
        elif "ď" == text[k] or "ť" == text[k] or "ň" == text[k]:
            PressKey(VK_CAPS)
            ReleaseKey(VK_CAPS)
            PressKey(VK_SHIFT)
            PressKey(VK_SPECIAL)
            useKey(text[k])
            ReleaseKey(VK_SHIFT)
            ReleaseKey(VK_SPECIAL)
            PressKey(VK_CAPS)
            ReleaseKey(VK_CAPS)
        elif "(" == text[k]:
            PressKey(VK_SHIFT)
            useKey(text[k])
            ReleaseKey(VK_SHIFT)
        else:
            useKey(text[k])
    if text[k].isupper():
        if "Ě" == text[k] or "Š" == text[k] or "Č" == text[k] or "Ř" == text[k] or "Ž" == text[k] or "Ý" == text[k] or "Á" == text[k] or "Í" == text[k] or "É" == text[k] or "Ú" == text[k] or "Ů" == text[k]:
            PressKey(VK_CAPS)
            ReleaseKey(VK_CAPS)
            useKey(text[k].lower())
            PressKey(VK_CAPS)
            ReleaseKey(VK_CAPS)
        elif "Ď" == text[k] or "Ť" == text[k] or "Ň" == text[k]:
            PressKey(VK_SHIFT)
            PressKey(VK_SPECIAL)
            useKey(text[k].lower())
            ReleaseKey(VK_SHIFT)
            ReleaseKey(VK_SPECIAL)
        elif text[k] == "Ó":
            PressKey(VK_CAPS)
            ReleaseKey(VK_CAPS)
            PressKey(VK_SPECIAL)
            useKey(text[k].lower())
            ReleaseKey(VK_SPECIAL)
            PressKey(VK_CAPS)
            ReleaseKey(VK_CAPS)
        else:
            PressKey(VK_SHIFT)
            useKey(text[k].lower())
            ReleaseKey(VK_SHIFT)
