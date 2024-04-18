import cv2
import numpy as np

# Define a function to handle mouse clicks
points = []
def click_event(event, x, y, flags, param):
    global frame
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) < 4:
            points.append((x, y))
        else:
            # Find the closest point to the mouse click and update it
            distances = [np.sqrt((x - px)**2 + (y - py)**2) for px, py in points]
            min_dist_idx = distances.index(min(distances))
            points[min_dist_idx] = (x, y)
        frame = draw_points(frame, points)

def draw_points(img, points):
    for point in points:
        cv2.circle(img, point, 5, (0, 255, 0), -1)
    return img

# Initialize video capture from camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

# Assume the camera matrix and distortion coefficients are known
camera_matrix = np.array([[1.07904581e+03, 0, 9.44038473e+02],
                          [0, 1.07110786e+03, 4.68711315e+02],
                          [0, 0, 1]])  # fx, fy are focal lengths, cx, cy are the image center
dist_coeffs = np.array([-0.46194896, 0.34433724, 0.00540389, 0.00242163, -0.16613006])  # Distortion coefficients

cv2.namedWindow('Frame')
cv2.setMouseCallback('Frame', click_event)

# Process video stream
while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Correct distortion for each frame
    h, w = frame.shape[:2]
    new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (w,h), 1, (w,h))
    frame = cv2.undistort(frame, camera_matrix, dist_coeffs, None, new_camera_matrix)

    if len(points) == 4:
        src_points = np.array(points, dtype='float32')
        # Define the destination points for the perspective transform
        side = 300  # Size of the square where we will map the points
        dst_points = np.array([[0, 0], [side, 0], [side, side], [0, side]], dtype='float32')
        # Compute the perspective transform matrix
        matrix = cv2.getPerspectiveTransform(src_points, dst_points)
        # Apply the perspective transformation
        result_image = cv2.warpPerspective(frame, matrix, (side, side))
        # Display the result in a separate window
        cv2.imshow('Transformed', result_image)

    # Draw points on the original frame
    frame = draw_points(frame, points)
    cv2.imshow('Frame', frame)

    if cv2.waitKey(1) == ord('q'):  # Exit on 'q' key press
        break

# Clean up
cap.release()
cv2.destroyAllWindows()