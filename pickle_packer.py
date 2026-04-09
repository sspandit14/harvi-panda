import os
import argparse
import shutil

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-in_dir", "--InDir", required=True, help="Directory to Read Samples From")
    parser.add_argument("-out_dir", "--OutDir", required=True, help="Directory to Store Renamed Samples")
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
        print(f"packing {material_path}")

        sample_info = m.split("_", 3)

        if len(sample_info) != 4:
            print(f"check folder name for {m}")
            continue

        date, mat_no, mat_name, sample_no = sample_info

        out_dir = os.path.join(output_dir, f"{mat_no}_{mat_name}")

        os.makedirs(out_dir, exist_ok=True)

        out_name = f"{sample_no}_{date}"

        out_path = os.path.join(out_dir, out_name)

        if os.path.exists(out_path):
            print(f"{out_path} already exists, skipping...")
            continue

        shutil.move(str(material_path), str(out_path))
        print(f"moved {material_path} to {out_path}")

if __name__ == "__main__":
    main()