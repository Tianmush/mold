# Physical Tech Codebase

## Object detection

This was our preliminary attempts at object detection and tracking using OpenCV. Our original plans were to track the shapes of objects placed on the table, but eventually we moved to using Aruco markers, making this code obsolete in our final product. 

## Camera Calibration

This code was made to supplement the claibration tools touch designer files we built. This would grab a handful of pictures using checker board grids to determine the distortion of the webcam we were using. We could then take the values that it returned to us and input them into some of the distortion nodes in our networks to account for the lens distortion on our physical camera.
