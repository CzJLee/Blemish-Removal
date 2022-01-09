# Blemish Removal Tool in OpenCV

- [Blemish Removal Tool in OpenCV](#blemish-removal-tool-in-opencv)
	- [How To Use](#how-to-use)
	- [Requirements](#requirements)
	- [Examples](#examples)
	- [Image Credits](#image-credits)

A Blemish Removal tool in OpenCV that replicates the Heal Brush tool from Photoshop. The Heal Brush is used to remove blemishes, spots, and unwanted objects from an image.

The Heal Brush is used by first selecting the unwanted object. A target region is then selected to clone from and replace the unwanted object. The patch is then blended to create a seamless image with the object removed. 

The Blemish Removal tool is great at removing pimples, unwanted objects or animals, or sensor dust. 

## How To Use

```
python3 blemish.py -i <input_path> -o <output_path>
```

`<input_path>`: Pathname of image to touchup. If no input path is given, a sample image will be used.

`<output_path>` (optional): The file name to save the final image. 

Keyboard Shortcuts:
* Press `ESC` to exit the program. 

* Press `'z'` to undo. 

* Press `'s'` to save the image. 

* Press `'['` or `']'` to change the brush size, or move the brush size slider.

## Requirements
```
pip3 install opencv-python
```

## Examples

![Before After Blemish](before-after-blemish.jpg?raw=true "Before After Blemish")

![Before After Birds](before-after-birds.jpg?raw=true "Before After Birds")


## Image Credits
[Silhouette of Person Standing on Field](https://www.pexels.com/photo/silhouette-of-person-standing-on-field-556669/) by luisclaz

[Acne Pores Skin Pimple Female](https://pixabay.com/photos/acne-pores-skin-pimple-female-1606765/) by Kjerstin_Michaela

