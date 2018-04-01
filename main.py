#Enter the names of the rooms here
rooms = {1: "Abdullah's Room", 2: "Office", 3: "Another Room", 4: "Extra Room"} 

#Enter your Hue Bridge's IP address here
ip = '192.168.X.X'

# Import Python Philips Hue Library & Keyboard key listener library
from phue import Bridge
from pynput.keyboard import Key, Listener


#Execute series of commands based on what's in the array
	# 0: Room/Light (r: rooms, l: lights)
	# 1: Room/light ID (Refer to rooms array for values)
	# 2: Modifier (enter: toggle power, h: hue, s: saturation)
	# 3: Modifier Value (0-255 for satuation/brightness. 0-65535 for hue)
cmd = []

# Connection Settings to connect to the Philips Hue Bridge
def init(ip_address):
	global b
	b = Bridge(ip_address)
	b.connect
	#print(b.get_group()) #Uncomment this if you need to know your room names

#Execute this function when a key is pressed
def on_press(key):
	send(key)
	print(cmd)

#Execute this function when a key is released, press F12 to exit this app
def on_release(key):
    if key == Key.f12:
        # Stop listener
        return False

def send(key):
	print(key)
	global cmd

	try:
		i = key.char
	except AttributeError:
		i = key

	# If Escape is pressed, reset the selected room/light
	if(key == Key.esc or key == Key.backspace):
		cmd = []
	
	# Otherwise get the room/light ID
	elif(len(cmd) <= 2):

		# By default, pressing a number will select the room by ID
		if(len(cmd) == 0):
			try:
				# Set selected group/room to the right index from rooms[]  
				if(i.isdigit()):
					cmd.append('r')
					cmd.append(int(i))
					cmd.append('bri')
					cmd.append(b.get_group(rooms[cmd[1]], 'bri'))


				# Unless you press the 'L' key first, then you can select a light manually
				elif(i == 'l'):
					cmd.append('l')
				else:
					pass
			except:
				pass

		# Select the light to edit
		elif(len(cmd) == 1 and cmd[0] == 'l'):
			try:
				if(i.isdigit()):
					cmd.append(int(i))
					cmd.append('bri')
					cmd.append(b.get_light(cmd[1], 'bri'))
				else:
					pass
			except:
				pass
		else:
			pass
	
	# Change the modifier/ modifier value
	elif(len(cmd) == 4):
		value = 255

		# If input is enter/space, toggle power
		if(key == Key.enter or key == Key.space):
			if(cmd[0] == 'r'):
				b.set_group(rooms[cmd[1]], 'on', not b.get_group(rooms[cmd[1]], 'on'))
			else:
				b.set_light(cmd[1], 'on', not b.get_light(cmd[1], 'on'))
		else:
			#Change the modifier "S" to change satuation, "B" to change brightness (default), "H"/"C" for color/hue, "W" to set the lights to white
			if(i == 's'):
				cmd[2] = 'sat'
			elif(i == 'b'):
				cmd[2] = 'bri'
			elif(i == 'c' or i == 'h'):
				cmd[2] = 'hue'
				if(cmd[0] == 'r'):
					b.set_group(rooms[cmd[1]], 'sat', 255)
				else:
					b.set_light(cmd[1], 'sat', 255)

			elif(i == 'w'):
				# Make the lights white

				#This is the default 'white' color
				white_hue = 8418
				white_sat = 140

				if(cmd[0] == 'r'):
					b.set_group(rooms[cmd[1]], 'on', True)
					b.set_group(rooms[cmd[1]], 'bri', 255)
					b.set_group(rooms[cmd[1]], 'hue', white_hue)
					b.set_group(rooms[cmd[1]], 'sat', white_sat)
				else:
					b.set_light(cmd[1], 'on', True)
					b.set_light(cmd[1], 'bri', 255)
					b.set_light(cmd[1], 'hue', white_hue)
					b.set_light(cmd[1], 'sat', white_sat)
			else:
				# Change the values by taking inputs 0-9 (10%-100%) if input is a number
				try:
					if(i.isdigit()):

						# Change the modifier value to a multiple of 10%
						if(cmd[2] == 'sat' or cmd[2] == 'bri'):
							# Make i an integer, if it's zero assign it to the highest value
							if(int(i) == 9):
								i = 10
							else:
								i = int(i)

							value = int( 255 * (i / 10) )
						elif(cmd[2] == 'hue'):
							value = int( 65535 * (int(i) / 10) )
							print(value)
						else:
							pass
						
						#Change the value locally
						cmd[3] = value

				except AttributeError:
					pass
				except UnboundLocalError:
					pass

				# Fine tune values using up/down keys, or very fine tune with left/right
				if(key == Key.up):
					if(cmd[2] == 'sat' or cmd[2] == 'bri'):
						cmd[3] = cmd[3] + 10
					elif(cmd[2] == 'hue' and cmd[3]):
						cmd[3] = cmd[3] + 500
					
					if((cmd[2] == 'sat' or cmd[2] == 'bri') and cmd[3] >= 255):
						cmd[3]  = 255
					elif(cmd[2] == 'hue' and cmd[3] > 65535):
						cmd[3] = 65535

				elif(key == Key.down):
					if(cmd[2] == 'sat' or cmd[2] == 'bri'):
						cmd[3] = cmd[3] - 10
					elif(cmd[2] == 'hue' and cmd[3]):
						cmd[3] = cmd[3] - 500

					if((cmd[2] == 'sat' or cmd[2] == 'bri') and cmd[3] <= 0):
						cmd[3] = 0
					elif(cmd[2] == 'hue' and cmd[3] < 0):
						cmd[3] = 0

				elif(key == Key.right):
					if(cmd[2] == 'sat' or cmd[2] == 'bri'):
						cmd[3] = cmd[3] + 2
					elif(cmd[2] == 'hue' and cmd[3]):
						cmd[3] = cmd[3] + 100
					
					if((cmd[2] == 'sat' or cmd[2] == 'bri') and cmd[3] >= 255):
						cmd[3]  = 255
					elif(cmd[2] == 'hue' and cmd[3] > 65535):
						cmd[3] = 65535

				elif(key == Key.left):
					if(cmd[2] == 'sat' or cmd[2] == 'bri'):
						cmd[3] = cmd[3] - 2
					elif(cmd[2] == 'hue' and cmd[3]):
						cmd[3] = cmd[3] - 100

					if((cmd[2] == 'sat' or cmd[2] == 'bri') and cmd[3] <= 0):
						cmd[3] = 0
					elif(cmd[2] == 'hue' and cmd[3] < 0):
						cmd[3] = 0
				else:
					pass

				# Apply the modifier changes to the lights
				if(cmd[0] == 'r'):
					b.set_group(rooms[cmd[1]], cmd[2], cmd[3])
				else:
					b.set_light(cmd[1], cmd[2], cmd[3])

			
			# Get the currently assigned modifier value
			if(cmd[0] == 'r'):
				cmd[3] = b.get_group(rooms[cmd[1]], cmd[2])
			else:
				cmd[3] = b.get_light(cmd[1], cmd[2])

	else:
		pass
	

# Connect to the Bridge
init(ip)

# Listen to key events until stopped
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()