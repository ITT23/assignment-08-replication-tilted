# Documentation

## Decision Process

We discussed a few potential paper for example "The bubble cursor: enhancing target acquisition by dynamic resizing of the cursor's activation area", "Mobile Phones as Pointing Devices" or the papers of our journal club. But the input techniques presented in those were either too easy(for 3 people) or too hard to replicate. After looking over them we discussed the paper ["Natural throw and tilt interaction between mobile phones and distant displays"](https://dl.acm.org/doi/abs/10.1145/1520340.1520467?casa_token=tPt_nNSHzxoAAAAA%3AvBnONUcn68lt9nj3HLlBOtkJKcMi-a-HIHsYxd4WW2xYXDjClwjj9KEan7ISVKCcHQQqxwkJwEN6) , which we found was a reasonable interaction technique, that can be used in many applications. In the paper they described a few application purposes and presented a gallery view, which we chose to implement ourselfs. We have chosen the image viewer from the paper for the following reasons:

- for the application you only need a smartphone and no additional hardware
- nothing too easy or shallow, since we are a group of three
- in the image viewer you can switch images with tilt gestures and add new images by a throwing gesture, which can be extended to work in more than this application (e.g. powerpoint)

## Components and Implementation

### Gesture Recognition

we trained an LSTM model on four gestures: TILT_LEFT, TILT_RIGHT, THROW, NEUTRAL.

1. first, we generated a lot of accelerometer data with `gather-data.py` with M5Stacks and android smartphones using the DIPPID class. this app makes it easy to generate data: pressing button_1 starts a record, pressing button_1 again stops the record and dumps it in a csv file. this can be repeated for a specific gesture as long as needed. the CLI parameters are documented in the according script file. According to the paper, accelerometer data is sufficient to recognise the correct gestures.

2. mid-project, we realised that the x-axis of M5Stacks and some Android Smartphones are inverted. so we decided to check all the git commits that included data from M5Stacks and multiplied all accelermeter x values by -1. (see `invert.py` in archive)

3. we trained a lstm model that showed good results after 500 records. in total, we recorded 2608 gestures with M5Stacks and android smartphones. we also included a plot showing the loss and accuracy for each epoch along with a confusion matrix.

4. we saved the trained model to the folder lstm_model so that we can compile it when needed in `recogniser.py` that is referenced in `gallery_app.py`. we also saved the encoder settings so that we can savely translate the encoding back to the enum names.

5. `test_recogniser.py` (in archive) can be used to test the trained recogniser model with a M5Stack or an android smartphone.

### Tilted Desktop App - Image Viewer

#### Getting Started

0. make sure there is a folder called `lstm_model` in the same directory as `pyglet-gallery.py`. Otherwiese run `gesture_recognition/model.ipynb` first.
1. run `python pyglet-gallery.py [smartphone IP] [path to image folder]`
   Command line parameters are optional and have default values. But for remote control, make sure the smartphone IP is corrent.

#### Description

The desktop application consists of a pyglet window, which displays images of a given folder. You can use the arrow keys on the keyboard to scroll to this image gallery.

**TODO: GIF einfügen**

In combination with **DIPPID** and **Tilted** (described below), you can also use a mobile device as remote control here. The pyglet app handles different events then:

- TILT LEFT: the image viewer shows the previous displayed image.
- TILT RIGHT: the next picture is shown.
- THROW: an image chosen by **Tilted** mobile app is added and focused.

#### Implementation

For classifying performed gestures with the mobile device, the desktop app uses a pre-trained LSTM (described above). The prediction is based on accelerometer sonsor data which are sent via **DIPPID** from mobile device to PC. Incoming accelerometer data is stored in a deque. As soon as we have enough values, the program initiates a prediction. Based on the prediction, the pyglet app replaces the images or sends a GET-request to receive an image from **Tilted** mobile app.

### Tilted Mobile App - Image Selection

If you just want to use your smartphone as a remote control to browse through your image gallery, it is sufficient to install only the **DIPPID** app. But if you also want to transfer an image from your smartphone to a larger screen, you will additionally need the **Tilted** app.

#### Getting Started

1. download [Tilted]() and [DIPPID]() and install them on your mobile device
2. start **DIPPID**, enter your PC's IP and toggle send data so that it is active
3. start **Tilted**, make sure **DIPPID** is still running in the background
4. start pyglet-gallery.py and pass the IP displayed in your **Tilted** app as command line parameter
5. use **Tilted** as described in the following

#### Description

The mobile app consists of two sections which can be switched by a tab menu. One section for selecting an image and another section for taking a new photo to add it to the current image gallery at the larger screen.

|                explorer view                |               take-a-photo view               |              ready-to-throw view              |
| :-----------------------------------------: | :-------------------------------------------: | :-------------------------------------------: |
| ![Explorer View Image](mobile_explorer.png) | ![Take A Photo View Image](mobile_camera.png) | ![Ready 2 Throw View Image](mobile_throw.png) |

In the **explorer view**, you can chose an image out of your files. If you click its filename, it will be displayed in the **ready-to-throw view**. By performing a _throw_ gesture, the file will be transferred to and displayed at your other device.

When clicking the button in the **take-a-photo view**, the camera opens up and you can take a picture in landscape mode. Once you have done this, the newly captured image shows up in the **ready-to-throw view**. Now, you can transfer the photo with a _throwing_ gesture.

#### Implementation

We implemented the mobile app in Java. It offers a GUI to chose an image file out of a file explorer as well as the option to take a new photo.

Since we have **DIPPID**, we used the existing workflow for sending sensor data to the PC. For this reason, and because of the simpler use `python`, we recognize performed gestures on the PC, not on the mobile device. Therefore, the PC has to notify the mobile device when the user performs a _throwing_ gesture.

To this end, we implemented a HTTP server on the mobile device using [NanoHTTPD](https://github.com/NanoHttpd/nanohttpd) which receives GET-requests as soon as a _throw_ gesture is recognized. The smartphone responds with the currently displayed image within **Tilted** encoded as `base64`.

To establish a connection between mobile device and PC, the smartphone's IP is served as command line parameter to the image gallery. No worries, there is no need for the user to discover their smartphone's IP by themselves: It is displayed in **Tilted**.
