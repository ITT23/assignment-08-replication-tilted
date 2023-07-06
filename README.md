[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/Ki47e6IN)

## TODO:

### Gesture Recognition
Recognize gestures based on DIPPID-data

- tilt left
- tilt right
- throw

Approach (in paper): Thresholds
Alternative approach (maybe better?): (SVM), LSTM

### Desktop Image Viewer
- GUI sth like this: ![image](https://github.com/ITT23/assignment-08-replication-tilted/assets/53038141/5d7a7aa6-e0e2-4e05-bf4c-f05ad32e7f3e)
- handle event: tilt left -> last img
- handle event: tilt right -> next img
- handle event: throw -> show received img at current position

### Mobile App
- connect with desktop (WiFi)
- chose image (folder)
- send image(s) to desktop (TCP)
- (take picture)

---

Tilt Paper weil wegen:
- no additional hardware
- not too easy
- decided to implement the image viewer part because it can be extended for example for PowerPoint, image viewer makes sense with data transfer, possibility to implement in pyglet
- TODO: links other potential paper we had a look at
  
