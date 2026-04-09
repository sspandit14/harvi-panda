import os
import argparse
import shutil

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-in_dir", "--InDir", required=True, help="Directory to Extract Gelsight Videos From")
    parser.add_argument("-out_dir", "--OutDir", required=True, help="Directory to Store Gelsight Videos")
    args = parser.parse_args()

    f_dir = args.InDir
    output_dir = args.OutDir

    os.makedirs(output_dir, exist_ok=True)

    print(f_dir)
    print(output_dir)

    materials = [m for m in os.listdir(f_dir) if os.path.isdir(os.path.join(f_dir, m))]

    print(materials)

    for m in materials:
        material_path = os.path.join(f_dir, m)
        print(f"going to jar {material_path}")

        samples = [s for s in os.listdir(material_path) if os.path.isdir(os.path.join(material_path, s))]
        print(samples)

        i = 0

        for s in samples:
            s_path = os.path.join(material_path, s)
            for f in os.listdir(s_path):
                if f.endswith(".mp4"):
                    src_path = os.path.join(s_path, f)
                    video_name = f"{m}_{i}.mp4"
                    i = i+1
                    dest_path = os.path.join(output_dir, video_name)
                    shutil.copy(src_path, dest_path)

            # try:
            #     pickle_jar = jar_pickles(sample_path)
            #     print(f"pickles in {sample_path} have been jarred!")
            #     out_dir = os.path.join(output_dir, m)
            #     os.makedirs(out_dir, exist_ok=True)
            #     out_path = os.path.join(out_dir, f"{s}.npz")
            #     print(f"writing jar to {out_path}")

            #     np.savez(
            #         out_path,
            #         timestamps=pickle_jar["timestamps"],
            #         pressures=pickle_jar["pressures"],
            #         joint_positions=pickle_jar["joint_positions"],
            #         joint_velocities=pickle_jar["joint_velocities"],
            #         net_velocities=pickle_jar["net_velocities"],
            #     )

            # except Exception as e:
            #     print(f"Exception for {s}: {e}")

if __name__ == "__main__":
    main()