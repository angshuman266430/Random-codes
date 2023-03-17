import cv2

def edit_video(input_file, output_file, start_time, end_time, output_duration, speed_up_factor=1):
    # Open the input video file
    cap = cv2.VideoCapture(input_file)

    # Get the original video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Calculate start and end frames
    start_frame = int(start_time * fps)
    end_frame = int(end_time * fps)
    total_frames = end_frame - start_frame

    # Calculate the output video frame rate
    output_fps = total_frames / output_duration * speed_up_factor

    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(output_file, fourcc, output_fps, (width, height))

    # Initialize the current frame number
    frame_number = 0

    while cap.isOpened():
        ret, frame = cap.read()

        # Break the loop if the video has ended
        if not ret:
            break

        # Only process and write the frame if it's within the start and end times
        if start_frame <= frame_number <= end_frame:
            frame_step = int((end_frame - start_frame) / (output_duration * fps) * speed_up_factor)
            if frame_number % frame_step == 0:
                out.write(frame)

        # Increment the frame number
        frame_number += 1

        # Stop processing if the end frame is reached
        if frame_number > end_frame:
            break

    # Release the VideoCapture and VideoWriter objects
    cap.release()
    out.release()

# Edit the video
input_file = "screen_record.avi"
output_file = "edited_video.avi"
start_time = 10  # Start time in seconds
end_time = 40  # End time in seconds
output_duration = 20  # Output video duration in seconds
# speed_up_factor = 2  # Uncomment this line to use the speed_up_factor

edit_video(input_file, output_file, start_time, end_time, output_duration) # Add `, speed_up_factor` to the function call if you want to use it
