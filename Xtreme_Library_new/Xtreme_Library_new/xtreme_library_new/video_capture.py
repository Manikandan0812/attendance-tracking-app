import logging
import os
import threading
import time
from os.path import exists

import cv2
import numpy as np
from pyautogui import screenshot, size


class VideoRec:
    def __init__(self, file_path: str) -> None:
        self.four_cc = cv2.VideoWriter_fourcc(*"VP80")
        self.vw = None
        self.file_path = file_path
        self.recording = False
        self.thread = None
        self.lock = threading.Lock()  # Threading lock to ensure thread safety
        self.fps = 1
        self.resolution = size()  # Dynamically get screen resolution

    def start_recording(self, fps=1) -> None:
        """Initialize the recording."""
        self.fps = fps
        logging.info(f"Starting video recording: {self.file_path} with resolution: {self.resolution}")

        try:
            self.vw = cv2.VideoWriter(
                self.file_path,
                self.four_cc,
                self.fps,
                self.resolution
            )
            if not self.vw.isOpened():
                raise ValueError(f"Failed to open VideoWriter for {self.file_path}")
            self.recording = True
        except Exception as e:
            print(f"Error initializing recording: {e}")
            self.cleanup_resources()
            raise

    def record_video(self) -> None:
        """Capture the screen and save to video."""
        try:
            while self.recording:
                if not self.vw:
                    raise RuntimeError("VideoWriter is not initialized.")

                img = screenshot()
                img_np = np.array(img)
                img_final = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
                self.vw.write(img_final)
                time.sleep(1 / self.fps)
        except Exception as e:
            print(f"Error during video recording: {e}")
        finally:
            print("Recording stopped. Cleaning up resources.")
            self.stop_recording()

    def stop_recording(self) -> None:
        """Stop the recording and release resources."""
        with self.lock:
            if self.recording:
                self.recording = False
                self.cleanup_resources()

    def cleanup_resources(self) -> None:
        """Release the video writer and other resources."""
        if self.vw:
            print(f"Releasing video writer for: {self.file_path}")
            self.vw.release()
            self.vw = None

    def run_in_thread(self) -> None:
        """Start recording in a separate thread."""
        with self.lock:
            if self.thread and self.thread.is_alive():
                print("Recording thread is already running.")
                return
            self.thread = threading.Thread(target=self.record_video, daemon=True)
            self.thread.start()

    def wait_for_thread(self) -> None:
        """Wait for the thread to finish."""
        if self.thread:
            self.thread.join()



if __name__ == "__main__":
    v = VideoRec("steps.webm")
    v.start_recording()
    v.run_in_thread()
    time.sleep(10)
    v.stop_recording()
    v.wait_for_thread()