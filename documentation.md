# Documentation

## Decision Process
We discussed a few potential paper for example "The bubble cursor: enhancing target acquisition by dynamic resizing of the cursor's activation area", "Mobile Phones as Pointing Devices" or the papers of our journal club. But the input techniques presented in those were either too easy(for 3 people) or too hard to replicate. After looking over them we discussed the paper... , which we found was a reasonable interaction technique, that can be used in many applications. In the paper they described a few application purposes and presented a gallery view, which we chose to implement ourselfs. We have chosen the image viewer from the paper ... for the following reasons:

- for the application you only need a smartphone and no additional hardware
- nothing too easy or shallow, since we are a group of three
- in the image viewer you can switch images with tilt gestures and add new images by a throwing gesture, which can be extended to work in more than this application (e.g. powerpoint)

## Implementation

### Gesture Recognition
We trained an LSTM model on three gestures: TILT, THROW, NEUTRAL. In order to distinguish between right- and left-tilt, we categorize the accelerometer data, after our model predicted a tilt gesture. 

### Desktop Image Viewer
The desktop application consists of a pyglet window, in which selected images of the user are displayed. The pyglet app handles different events, that are received from the smartphone. When the model predicts a left tilt, the image viewer shows the previous displayed image. When a right tilt is detected, the next picture is shown (in focus). When a throw gesture is detected, an images taken with the corresponding mobile app is added to the image viewer.

### mobile app
The mobile app consists of two sections. one section for selecting a image nfolder and another section for making a new phoo and adding it to the current image gallery.


### usage

- download the apk and enter the ip of your pc/laptop
- choose a folder you want to have displayed on your other device
- if images are shown on other device, you can tilt your phone left or right, to scroll through your images
- if you want to add a new image to your gallery, you can take a picture with the app and send it to your device
- the new picture is displayed at the position of the current image
(Video)