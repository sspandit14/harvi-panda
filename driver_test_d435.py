import cv2
import numpy as np

from d435_helper import D435_Helper

def main():
    camera = D435_Helper()
    camera.start()

    try:
        fx, fy, cx, cy = camera.camera_parameters()
        print("Intrinsics: ", fx, fy, cx, cy)

        while True:
            frame = camera.get_frames()

            print(
                f"t={frame.timestamp_s:.3f}s"
                f"color={frame.color.shape}"
                f"depth={frame.depth.shape}"
                f"depth_dtype={frame.depth.dtype}"
            )

            depth_vis = cv2.convertScaleAbs(frame.depth, alpha=0.03)
            depth_vis = cv2.applyColorMap(depth_vis, cv2.COLORMAP_JET)

            stacked = np.hstack((frame.color, depth_vis))
            cv2.imshow("Color | Depth", stacked)

            key = cv2.waitKey(1) & 0xFF
            if key == 27 or key == ord("q"):
                break

    finally:
        camera.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()