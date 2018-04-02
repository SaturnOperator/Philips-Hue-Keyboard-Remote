# Philips Hue Keyboard Remote

Use any keyboard to control Philips Hue lights!

This Python script listens to key presses and has the power to control any lights or rooms connected to your Philips Hue Bridge! The controls are very simple and no screen is required. 

I have this script running on a Raspberry Pi that's paired to my Logitech K380 bluetooth keyboard, it's really convenient as I can easily switch to the profile to control the lights and works from anywhere in the house!

----------
**Installation:**

The script is written for Python 3+. I'm using the [phue](https://github.com/studioimaginaire/phue) python library to easily control Philips Hue lights and [pynput](https://pypi.python.org/pypi/pynput) to detect keyboard key presses. You can install them using:

```
pip install phue
```
```
pip install pynput
```
----------

**Setup:**

The first time you run the script you will need to authorize the script with your Philips Hue Bridge. You can do this by pressing the blue lit button on your bridge within 30 seconds of running the script. 

On *Line 2* fill the array with the rooms/light groups associated with your Philips Hue Bride. Make sure the spelling is exactly how it's spelled on the Philips Hue Bridge .

    rooms = {1: "Abdullah's Room", 2: "Office", 3: "Another Room", 4: "Extra Room"}

On *Line 5* in the script change the IP address to the IP address of your Philips Hue Bridge.

    ip = '192.168.X.X'

Note to get all the room names you can uncomment *Line 24* to get all the room names on your Philips Hue Bridge.

    print(b.get_group())

----------
**Instructions:**

When you run the script it will start listening for key presses. 

 1. Pressing numbers **1-9** will select which light group (room) you want
    to control. Alternatively pressing '**L**' followed by numbers **1-9**
    will select the light with that ID. For example pressing 1 will select "Abdullah's Room" as that is set for index value 1 in the rooms array. 
 
 2. Pressing **ESC** / **Backspace** will reset the current selected light/room. Then follow step 1 to select a new light / room.

3. Once you have selected a light/room you have the following options to control your selected light/room:
	- **Enter** / **Space**: Turns the selected light on or off
	- **W**: Sets the selected lights to the color white
	- **#0-9**: Changes the selected modifier's value (default modifier is brightness so pressing #0-9 after selecting a new room will change the brightness) 
	- **UP** / **DOWN**: Fine tune the modifier values to get the exact setting you want.
	- **LEFT** / **RIGHT**: Very fine tuning to the modifier values to get that even more precise setting you want.
	
	Modifiers:
	- **B**: Changes the modifier to Brightness, pressing B followed by a number from 0-9 will set the brightness to that amount on a scale from one to ten. For example pressing 5 will set brightness to 50%. (Note pressing 9 sets brightness to the max). You can also use the arrow keys to set a more precise value, such as changing 50% to 55% brightness.
	- **S**: Changes the modifier to Saturation, works the same way as adjusting the brightness however here you're tuning how much color the light has (Saturation) using numbers 0-9.
	- **C** / **H**: Changes the modifier to hue/color. Pressing numbers 0-9 will represent  a different spot on the RGB colorwheel. (Essentially each number is a different color). You can also use the arrow keys to get a more precise color shade that you want.

4. **F12**: Exit the script and stops listening to keyboard input.



