import cv2

cap = cv2.VideoCapture('1-1.mkv')

# Read the first frame
ret, frame1 = cap.read()
i = 1000
while cap.isOpened():
    i += 1
    ret, frame2 = cap.read()
    # if i % 50 != 0:
    #     continue
    # Read the next frame

    if not ret:
        break

    # Calculate the absolute difference between frames
    # diff = cv2.absdiff(frame1, frame2)
    cv2.imwrite(f'output/{i}.png', frame2)

    # Display the difference
    # cv2.imshow('diff', diff)
    #
    # # Press 'q' to quit
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

    # Now update frame1 to be the new frame2
    frame1 = frame2

cap.release()
cv2.destroyAllWindows()
