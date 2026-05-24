import cv2

from d435_helper import D435_Helper
from apriltag_helper import AprilTagHelper
from velocity_tracker import VelocityTracker

def main():
    camera = D435_Helper()
    camera.start()

    try:
        fx, fy, cx, cy = camera.camera_parameters()

        tagger = AprilTagHelper(camera_params=(fx, fy, cx, cy), tag_size_m=0.0713, family="tag36h11",)
        tracker = VelocityTracker(alpha=0.25)

        TARGET_ID = 0

        while True:
            frame = camera.get_frames()

            vis = frame.color.copy()

            tags = tagger.detect(frame.color, frame.timestamp_s, target_id=TARGET_ID)

            for tag in tags:
                center = tuple(tag.center.astype(int))
                cv2.circle(vis, center, 6, (0,0,255), -1)
                cv2.putText(vis, f"id={tag.tag_id}", (center[0] + 10, center[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

                for corner in tag.corners.astype(int):
                    cv2.circle(vis, tuple(corner), 4, (0, 255, 0), -1)

                est = tracker.update(tag.position, tag.timestamp_s)
                if est is not None:
                    print(f"pos={tag.position}, v={est.filtered_vel}, speed={est.speed:.3f} m/s")

            cv2.imshow("color", vis)

            if cv2.waitKey(1) & 0xFF in (27, ord("q")):
                break

    finally:
        camera.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()