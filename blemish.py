import cv2
import numpy as np
import sys, getopt
import pathlib

def fix_blemish(image, source_pos, target_pos, brush_size):
	# Trying to construct a good method to identify a "good" region seems really difficult. 
	# There are multiple factors to consider, such as how big of a search region to include, how to determine proper textured regions vs incorrect near by regions, how to optimize a search, whether to just search until you find one, or try to optimize, etc. 
	# So instead, I will build a tool similar to the Photoshop healing brush tool, where the user manually selects a better region. 
	# Personally, having used photoshop, I actually prefer this method, as it gives the user more control. Plus, since I am more familiar with it, it'll be easier for me to implement.

	image_original = image.copy()
	# Get ROI
	clone_source_roi = image_original[source_pos[1]-brush_size:source_pos[1]+brush_size, source_pos[0]-brush_size:source_pos[0]+brush_size]
	
	# Get mask
	clone_source_mask = np.ones(clone_source_roi.shape, clone_source_roi.dtype) * 255
	# Feather mask
	clone_source_mask = cv2.GaussianBlur(clone_source_mask, (5,5), 0, 0)

	# Apply clone
	fix = cv2.seamlessClone(clone_source_roi, image_original, clone_source_mask, target_pos, cv2.NORMAL_CLONE)
	return fix

# Function to update low threshold value
# Define brush size callback function
brush_size = 20
max_brush_size = 50
def update_brush_size( *args ):
	global brush_size, max_brush_size
	brush_size = args[0]

# Add mouse callback
target_selected = False
target_pos = None
def on_mouse(event, x, y, flags, userdata):
	global image, brush_size, image_history, target_selected, target_pos
	# image_view will be what is shown to the user, but is not necessarily the final image
	image_view = image_history[-1].copy()
	# Get mouse position
	mouse_pos = (x, y)

	# Have different handlers based on if the target is selected. 
	if target_selected == True:
		# User will click again to select the source region that they want to clone from
		if event == cv2.EVENT_LBUTTONDOWN:
			# On click
			image_view = fix_blemish(image_view, mouse_pos, target_pos, brush_size)
			image_history.append(image_view)
			target_selected = False

		if flags == cv2.EVENT_MOUSEMOVE:
			# Show ROI
			# Show target
			image_view = fix_blemish(image_view, mouse_pos, target_pos, brush_size)
			cv2.circle(image_view, center = target_pos, radius = brush_size, color = (0, 0, 255), thickness=1)
			# Make line Blue
			cv2.circle(image_view, center = mouse_pos, radius = brush_size, color = (255, 0, 0), thickness=1)
			# Draw line
			# Whole bunch of vector code to draw the proper connecting line
			t = np.array(target_pos)
			m = np.array(mouse_pos)
			if np.linalg.norm(t-m) > brush_size * 2:
				# Brushes are far enough to draw lines without error
				# Get vector between points
				v = t - m
				# Normalize vector
				line_vector = v / np.linalg.norm(v)
				# Subtract off the parts that we don't want 
				t = t - line_vector * brush_size
				t = tuple(t.astype(np.int64))
				m = m + line_vector * brush_size
				m = tuple(m.astype(np.int64))
				cv2.line(image_view, t, m, (255, 0, 0), 1)
	else:
		# If target_selected is False
		# User will click to select the target region that will be replaced. 
		if event == cv2.EVENT_LBUTTONDOWN:
			# On click
			# Define the target position
			target_pos = mouse_pos
			# Set toggle
			target_selected = True
			cv2.circle(image_view, center = mouse_pos, radius = brush_size, color = (0, 0, 255), thickness=1)

		if flags == cv2.EVENT_MOUSEMOVE:
			# Show ROI
			# Make mouse red
			cv2.circle(image_view, center = mouse_pos, radius = brush_size, color = (0, 0, 255), thickness=1)
	
	cv2.imshow(window_name, image_view)

def get_cli_io(argv):
	input_path = None
	output_path = None
	try:
		opts, args = getopt.getopt(argv[1:],"hi:o:")
	except getopt.GetoptError as err:
		print("Usage: blemish.py -i <input_path> -o <output_path>")
		print(err)
		sys.exit()
	for opt, arg in opts:
		if opt == '-h':
			print("Usage: blemish.py -i <input_path> -o <output_path>")
			sys.exit()
		elif opt == "-i":
			input_path = pathlib.Path(arg)
		elif opt == "-o":
			output_path = pathlib.Path(arg)
	if input_path is None:
		input_path = pathlib.Path("blemish.png")
		output_path = pathlib.Path("blemish_fix.png")
	elif output_path is None:
		output_path = input_path.with_stem(input_path.stem + "_fix")

	return input_path.as_posix(), output_path.as_posix()

if __name__ == "__main__":
	input_path, save_file_path = get_cli_io(sys.argv)
	# Read image
	image = cv2.imread(input_path, cv2.IMREAD_COLOR)
	if image is not None:
		print(f"\nSuccessfully read image '{input_path}'")
	else:
		print(f"\nFailed to read image '{input_path}'")
		quit()
	
	print("\nInstructions: Click on the blemish you want to remove. Then click on the target area to clone from.")
	print("Press ESC to exit the program. \nPress 'z' to undo. \nPress 's' to save the image. \nPress '[' or ']' to change the brush size, or move the brush size slider.")
	# Make a copy
	image_original = image.copy()
	# Create an image history to allow for undo
	image_history = [image_original]

	# Create a display window
	window_name = "Blemish Tool"
	cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
	cv2.imshow(window_name, image_history[-1])

	# Create a trackbar to control brush size
	# Why can createTrackbar not take keyword arguments?
	cv2.createTrackbar("Brush Size", window_name, brush_size, max_brush_size, update_brush_size)

	cv2.setMouseCallback(window_name, on_mouse)
	# Key press
	key_press = None
	while key_press != 27:
		# While key_press is not esc key

		# If "z" key
		if key_press == ord("z") and len(image_history) > 1:
			# Undo
			image_history.pop()
			cv2.imshow(window_name, image_history[-1])

		# If "s" key
		if key_press == ord("s"):
			# Save the image
			try:
				retval = cv2.imwrite(save_file_path, image_history[-1])
				if retval == True:
					print(f"Saved image as '{save_file_path}'")
			except cv2.error:
				print(f"Could not save image to '{save_file_path}'")

		# Add key toggles to change brush size
		if key_press == ord("]") and brush_size < max_brush_size:
			update_brush_size(brush_size + 1)
			cv2.setTrackbarPos("Brush Size", window_name, brush_size)
		if key_press == ord("[") and brush_size > 0:
			update_brush_size(brush_size - 1)
			cv2.setTrackbarPos("Brush Size", window_name, brush_size)

		# Need to have waitKey or else window will not display properly.
		key_press = cv2.waitKey(20) & 0xFF
		# Info on why "& 0xFF" is included: 
		# https://stackoverflow.com/questions/35372700/whats-0xff-for-in-cv2-waitkey1

	cv2.destroyAllWindows()