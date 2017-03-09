"""
Program test environment
Pyhone version:3.4.1
Firmware version:2.2.12
Dependent files(MacOSX):libGinkgo_Driver.dylib,libusb-0.1.4.dylib,libusb-1.0.0.dylib
Dependent files(Windows):Ginkgo_Driver.dll
Dependent files(Linux):libGinkgo_Driver.so,libusb-1.0.so
More Infomation:www.viewtool.com
"""
from ctypes import *
import platform
import ControlGPIO
import ControlSPI
from time import sleep
# USB - SPI initialization structure
class VSI_INIT_CONFIG(Structure):  
    _fields_ = [("ControlMode", c_ubyte), # 0-Hardware control (full-duplex mode),1-Hardware control (half duplex mode),2-Software control (half duplex mode),3-Single bus model, data input and output for MOSI
                ("TranBits", c_ubyte),    # 8-8bit,16-16bit
                ("MasterMode", c_ubyte),  # 0-Slave,1-Host
                ("CPOL",c_ubyte),         # 0-Hight,1-Low
                ("CPHA",c_ubyte),         # 0-First,1-Second
                ("LSBFirst",c_ubyte),     # 0-MSB First,1-LSB First
                ("SelPolarity",c_ubyte),  # 0-Sel Low,1-Sel Hight
                ("ClockSpeed",c_int),     # Hardware(36000000,18000000,9000000,4500000,2250000,1125000),Software(1000 To 1000000)
                ];


# Error Code
ERR_SUCCESS               = (0)  #
ERR_PARAMETER_NULL        = (-1) #
ERR_INPUT_DATA_TOO_MUCH   = (-2) #
ERR_INPUT_DATA_TOO_LESS   = (-3) #
ERR_INPUT_DATA_ILLEGALITY = (-4) #
ERR_USB_WRITE_DATA        = (-5) #
ERR_USB_READ_DATA         = (-6) #
ERR_READ_NO_DATA          = (-7) #
ERR_OPEN_DEVICE           = (-8) #
ERR_CLOSE_DEVICE          = (-9) #
ERR_EXECUTE_CMD           = (-10)#
ERR_SELECT_DEVICE         = (-11)#
ERR_DEVICE_OPENED         = (-12)#
ERR_DEVICE_NOTOPEN        = (-13)#
ERR_BUFFER_OVERFLOW       = (-14)#
ERR_DEVICE_NOTEXIST       = (-15)#
ERR_LOAD_KERNELDLL        = (-16)#
ERR_CMD_FAILED            = (-17)#
ERR_BUFFER_CREATE         = (-18)#

# Control Pin
LCD_RST_PIN = ControlGPIO.VGI_GPIO_PIN10
LCD_DC_PIN  = ControlGPIO.VGI_GPIO_PIN11
LCD_BL_PIN  = ControlGPIO.VGI_GPIO_PIN9

# FONT
font6x8 = {
    ' ': [0x00, 0x00, 0x00, 0x00, 0x00],
    '!': [0x00, 0x00, 0x5f, 0x00, 0x00],
    '"': [0x00, 0x07, 0x00, 0x07, 0x00],
    '#': [0x14, 0x7f, 0x14, 0x7f, 0x14],
    '$': [0x24, 0x2a, 0x7f, 0x2a, 0x12],
    '%': [0x23, 0x13, 0x08, 0x64, 0x62],
    '&': [0x36, 0x49, 0x55, 0x22, 0x50],
    "'": [0x00, 0x05, 0x03, 0x00, 0x00],
    '(': [0x00, 0x1c, 0x22, 0x41, 0x00],
    ')': [0x00, 0x41, 0x22, 0x1c, 0x00],
    '*': [0x14, 0x08, 0x3e, 0x08, 0x14],
    '+': [0x08, 0x08, 0x3e, 0x08, 0x08],
    ',': [0x00, 0x50, 0x30, 0x00, 0x00],
    '-': [0x08, 0x08, 0x08, 0x08, 0x08],
    '.': [0x00, 0x60, 0x60, 0x00, 0x00],
    '/': [0x20, 0x10, 0x08, 0x04, 0x02],
    '0': [0x3e, 0x51, 0x49, 0x45, 0x3e],
    '1': [0x00, 0x42, 0x7f, 0x40, 0x00],
    '2': [0x42, 0x61, 0x51, 0x49, 0x46],
    '3': [0x21, 0x41, 0x45, 0x4b, 0x31],
    '4': [0x18, 0x14, 0x12, 0x7f, 0x10],
    '5': [0x27, 0x45, 0x45, 0x45, 0x39],
    '6': [0x3c, 0x4a, 0x49, 0x49, 0x30],
    '7': [0x01, 0x71, 0x09, 0x05, 0x03],
    '8': [0x36, 0x49, 0x49, 0x49, 0x36],
    '9': [0x06, 0x49, 0x49, 0x29, 0x1e],
    ':': [0x00, 0x36, 0x36, 0x00, 0x00],
    ';': [0x00, 0x56, 0x36, 0x00, 0x00],
    '<': [0x08, 0x14, 0x22, 0x41, 0x00],
    '=': [0x14, 0x14, 0x14, 0x14, 0x14],
    '>': [0x00, 0x41, 0x22, 0x14, 0x08],
    '?': [0x02, 0x01, 0x51, 0x09, 0x06],
    '@': [0x32, 0x49, 0x79, 0x41, 0x3e],
    'A': [0x7e, 0x11, 0x11, 0x11, 0x7e],
    'B': [0x7f, 0x49, 0x49, 0x49, 0x36],
    'C': [0x3e, 0x41, 0x41, 0x41, 0x22],
    'D': [0x7f, 0x41, 0x41, 0x22, 0x1c],
    'E': [0x7f, 0x49, 0x49, 0x49, 0x41],
    'F': [0x7f, 0x09, 0x09, 0x09, 0x01],
    'G': [0x3e, 0x41, 0x49, 0x49, 0x7a],
    'H': [0x7f, 0x08, 0x08, 0x08, 0x7f],
    'I': [0x00, 0x41, 0x7f, 0x41, 0x00],
    'J': [0x20, 0x40, 0x41, 0x3f, 0x01],
    'K': [0x7f, 0x08, 0x14, 0x22, 0x41],
    'L': [0x7f, 0x40, 0x40, 0x40, 0x40],
    'M': [0x7f, 0x02, 0x0c, 0x02, 0x7f],
    'N': [0x7f, 0x04, 0x08, 0x10, 0x7f],
    'O': [0x3e, 0x41, 0x41, 0x41, 0x3e],
    'P': [0x7f, 0x09, 0x09, 0x09, 0x06],
    'Q': [0x3e, 0x41, 0x51, 0x21, 0x5e],
    'R': [0x7f, 0x09, 0x19, 0x29, 0x46],
    'S': [0x46, 0x49, 0x49, 0x49, 0x31],
    'T': [0x01, 0x01, 0x7f, 0x01, 0x01],
    'U': [0x3f, 0x40, 0x40, 0x40, 0x3f],
    'V': [0x1f, 0x20, 0x40, 0x20, 0x1f],
    'W': [0x3f, 0x40, 0x38, 0x40, 0x3f],
    'X': [0x63, 0x14, 0x08, 0x14, 0x63],
    'Y': [0x07, 0x08, 0x70, 0x08, 0x07],
    'Z': [0x61, 0x51, 0x49, 0x45, 0x43],
    '[': [0x00, 0x7f, 0x41, 0x41, 0x00],
    '\\': [0x02, 0x04, 0x08, 0x10, 0x20],
    ']': [0x00, 0x41, 0x41, 0x7f, 0x00],
    '^': [0x04, 0x02, 0x01, 0x02, 0x04],
    '_': [0x40, 0x40, 0x40, 0x40, 0x40],
    '`': [0x00, 0x01, 0x02, 0x04, 0x00],
    'a': [0x20, 0x54, 0x54, 0x54, 0x78],
    'b': [0x7f, 0x48, 0x44, 0x44, 0x38],
    'c': [0x38, 0x44, 0x44, 0x44, 0x20],
    'd': [0x38, 0x44, 0x44, 0x48, 0x7f],
    'e': [0x38, 0x54, 0x54, 0x54, 0x18],
    'f': [0x08, 0x7e, 0x09, 0x01, 0x02],
    'g': [0x0c, 0x52, 0x52, 0x52, 0x3e],
    'h': [0x7f, 0x08, 0x04, 0x04, 0x78],
    'i': [0x00, 0x44, 0x7d, 0x40, 0x00],
    'j': [0x20, 0x40, 0x44, 0x3d, 0x00],
    'k': [0x7f, 0x10, 0x28, 0x44, 0x00],
    'l': [0x00, 0x41, 0x7f, 0x40, 0x00],
    'm': [0x7c, 0x04, 0x18, 0x04, 0x78],
    'n': [0x7c, 0x08, 0x04, 0x04, 0x78],
    'o': [0x38, 0x44, 0x44, 0x44, 0x38],
    'p': [0x7c, 0x14, 0x14, 0x14, 0x08],
    'q': [0x08, 0x14, 0x14, 0x18, 0x7c],
    'r': [0x7c, 0x08, 0x04, 0x04, 0x08],
    's': [0x48, 0x54, 0x54, 0x54, 0x20],
    't': [0x04, 0x3f, 0x44, 0x40, 0x20],
    'u': [0x3c, 0x40, 0x40, 0x20, 0x7c],
    'v': [0x1c, 0x20, 0x40, 0x20, 0x1c],
    'w': [0x3c, 0x40, 0x30, 0x40, 0x3c],
    'x': [0x44, 0x28, 0x10, 0x28, 0x44],
    'y': [0x0c, 0x50, 0x50, 0x50, 0x3c],
    'z': [0x44, 0x64, 0x54, 0x4c, 0x44],
    '{': [0x00, 0x08, 0x36, 0x41, 0x00],
    '|': [0x00, 0x00, 0x7f, 0x00, 0x00],
    '}': [0x00, 0x41, 0x36, 0x08, 0x00],
    '~': [0x10, 0x08, 0x08, 0x10, 0x08],
}


def ConfigAdapter():
    nRet = ControlSPI.VSI_ScanDevice()
    if(nRet <= 0):
        print("No device connect!")
        exit()
    else:
        print(nRet)
    nRet = ControlSPI.VSI_OpenDevice(ControlSPI.VSI_USBSPI, 0, 0);
    if(nRet != ControlSPI.ERR_SUCCESS):
        print("No device connect!")
        print(nRet)
        exit()
        
    SPI_Init = ControlSPI.VSI_INIT_CONFIG()
    SPI_Init.ClockSpeed = 4500000;
    SPI_Init.ControlMode = 1;
    SPI_Init.CPHA = 0;
    SPI_Init.CPOL = 0;
    SPI_Init.LSBFirst = 0;
    SPI_Init.MasterMode = 1;
    SPI_Init.SelPolarity = 0;
    SPI_Init.TranBits = 8;
    nRet = ControlSPI.VSI_InitSPI(ControlSPI.VSI_USBSPI,0,byref(SPI_Init))
    if(nRet != ControlSPI.ERR_SUCCESS):
        print("Initialization device error!")
        exit()
    else:
        print("Initialization device success!")
    #Config RST,DC,BL pin
    nRet = ControlGPIO.VGI_SetOutput(ControlGPIO.VGI_USBGPIO, 0, LCD_BL_PIN | LCD_DC_PIN | LCD_RST_PIN)
    if(nRet != ControlSPI.ERR_SUCCESS):
        print("Config GPIO error!!")
        exit()
    else:
        print("Config GPIO success!")
    
def LCD_SetBacklightState(state):
    if(state != 0):
        ControlGPIO.VGI_SetPins(ControlGPIO.VGI_USBGPIO,0,LCD_BL_PIN)
    else:
        ControlGPIO.VGI_ResetPins(ControlGPIO.VGI_USBGPIO,0,LCD_BL_PIN)
        
def LCD_Reset():
    ControlGPIO.VGI_ResetPins(ControlGPIO.VGI_USBGPIO, 0, LCD_RST_PIN)
    sleep(0.01);
    ControlGPIO.VGI_SetPins(ControlGPIO.VGI_USBGPIO, 0, LCD_RST_PIN)
    
def LCD_WriteByte(Data, Command):
    if (Command != 0):
        ControlGPIO.VGI_SetPins(ControlGPIO.VGI_USBGPIO, 0, LCD_DC_PIN)
    else:
        ControlGPIO.VGI_ResetPins(ControlGPIO.VGI_USBGPIO, 0, LCD_DC_PIN)
        
    ControlSPI.VSI_WriteBytes(ControlSPI.VSI_USBSPI, 0, 0, byref(c_uint8(Data)),1)
    
def LCD_Init():
    ConfigAdapter()
    LCD_Reset()
    LCD_WriteByte(0x21,0)
    LCD_WriteByte(0xC0,0)
    LCD_WriteByte(0x06,0)
    LCD_WriteByte(0x13,0)
    LCD_WriteByte(0x20,0)
    LCD_WriteByte(0x0C,0)
    
def LCD_SetPosition( x, y):
    y |= 0x40
    x |= 0x80
    LCD_WriteByte( y, 0)
    LCD_WriteByte( x, 0)
    
def LCD_Clear():
    LCD_SetPosition(0,0)
    for t in range(0, 6):
        for k in range(0,84):
            LCD_WriteByte(0x00,1)
    
def LCD_DisplayChar(c):
    #print(c)
    LCD_WriteByte(0x00, 1)        
    for line in range(0, 5):
        LCD_WriteByte(font6x8[c][line], 1)

def LCD_WriteString( x, y, str):
    LCD_SetPosition(x,y)
    for i in range(0, len(str)):
        LCD_DisplayChar(str[i])
        print(str[i], end='')
    print()