import usb.core
import usb.util
import time

class LCD2USB:
    def __init__(self):
        self.LCD2USB_VID = 0x0403
        self.LCD2USB_PID = 0xc630
        self.LCD_CTRL_0 = (1 << 3)
        self.LCD_CTRL_1 = (1 << 4)
        self.LCD_BOTH = (self.LCD_CTRL_0 | self.LCD_CTRL_1)
        self.LCD_ECHO = (0 << 5)
        self.LCD_CMD = (1 << 5)
        self.LCD_DATA = (2 << 5)
        self.LCD_SET = (3 << 5)
        self.LCD_GET = (4 << 5)
        self.LCD_SET_CONTRAST = (self.LCD_SET | (0 << 3))
        self.LCD_SET_BRIGHTNESS = (self.LCD_SET | (1 << 3))
        self.LCD_GET_FWVER = (self.LCD_GET | (0 << 3))
        self.LCD_GET_KEYS = (self.LCD_GET | (1 << 3))
        self.LCD_GET_CTRL = (self.LCD_GET | (2 << 3))

        self.device = usb.core.find(idVendor=self.LCD2USB_VID, idProduct=self.LCD2USB_PID)

        if self.device is None:
            raise ValueError("Device not found")

    def lcd_get(self, request):
        try:
            buffer = self.device.ctrl_transfer(
                0xC0,  # bmRequestType (direction: in, type: vendor, recipient: device)
                request,
                0,  # wValue
                0,  # wIndex
                2   # Length of the data buffer
            )

            return buffer[0] + 256 * buffer[1]

        except usb.core.USBError:
            print("USB GET request failed!")
            return -1

    def lcd_send(self, request, value, index):
        try:
            self.device.ctrl_transfer(0x40, request, value, index, 0)
        except usb.core.USBError:
            print("USB request failed!")

    def lcd_command(self, ctrl, cmd):
        request = self.LCD_CMD | ctrl
        self.lcd_send(request, cmd, 0)

    def lcd_clear(self):
        self.lcd_command(self.LCD_BOTH, 0x01)
        self.lcd_command(self.LCD_BOTH, 0x03)

    def lcd_write(self, data):
        ctrl = self.LCD_CTRL_0
        for ch in data:
            request = self.LCD_DATA | ctrl  # 2 << 5 is LCD_DATA
            self.lcd_send(request, ord(ch), 0)

    def lcd_set_brightness(self, value):
        request = self.LCD_SET_BRIGHTNESS  # 3 << 5 is LCD_SET, 1 << 3 is brightness
        self.lcd_send(request, value, 0)

    def lcd_read_buttons(self):
        keymask = self.lcd_get(self.LCD_GET_KEYS) # CHATGPT I AM MISSING THIS FUNCTION
        if keymask != -1:
            return {"key_0": bool(keymask & 1), "key_1": bool(keymask & 2), }

    def lcd_read_buttons(self):
        keymask = self.lcd_get(self.LCD_GET_KEYS) # CHATGPT I AM MISSING THIS FUNCTION
        print(keymask)
        if keymask != -1:
            return {"key_0": bool(keymask & 1), "key_1": bool(keymask & 2), }

    def check_buttons(self):
        while True:
            buttons = self.lcd_read_buttons()
            print(buttons)
            if buttons.get("key_0"):
                self.check_button1_function()
            elif buttons.get("key_1"):
                self.check_button2_function()
            # ...and so on for other buttons
            time.sleep(0.2)

    def check_button1_nunction(self):
        print("Button 1 pressed!")
        self.lcd_write("Button 1")
        self.lcd.clear()

    def check_button2_function(self):
        print("Button 2 pressed!")
        self.lcd_write("Button 2")
        self.lcd_clear()



if __name__ == "__main__":
    lcd = LCD2USB()
    lcd.lcd_clear()
    lcd.lcd_write("Hello, Python")
    lcd.lcd_set_brightness(255)
    time.sleep(3)
    lcd.lcd_clear()
    lcd.lcd_write("Checking Buttons in 3 secs!")
    time.sleep(3)
    lcd.lcd_clear()
    lcd.check_buttons()
