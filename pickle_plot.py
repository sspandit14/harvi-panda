import numpy as np
import matplotlib.pyplot as plt
import os
import argparse

print("plotting pickles...")

parser = argparse.ArgumentParser()
parser.add_argument("-in_dir", "--InDir", required=True, help="Directory to Read Jars to be Plotted")
parser.add_argument("-out_dir", "--OutDir", required=True, help="Directory to Store Visuals")
args = parser.parse_args()

pickle_jars_dir = "./pickle_jars"
visual_jars_dir = "./pickle_jar_visuals"

in_dir = args.InDir
out_dir = args.OutDir

pickle_jars_dir = os.path.join(pickle_jars_dir, in_dir)
visual_jars_dir = os.path.join(visual_jars_dir, out_dir)
visual_jars_aio_dir = os.path.join(visual_jars_dir, "all-in-one")

if not os.path.exists(pickle_jars_dir):
    print(f"input directory doesn't exist...")
    exit()

os.makedirs(visual_jars_dir, exist_ok=True)
os.makedirs(visual_jars_aio_dir, exist_ok=True)

material_jars = [m for m in os.listdir(pickle_jars_dir) if os.path.isdir(os.path.join(pickle_jars_dir, m))]
print(material_jars)

for mat_jar in material_jars:
    samples = [s for s in os.listdir(os.path.join(pickle_jars_dir, mat_jar)) if s.endswith(".npz")]
    out_dir = os.path.join(visual_jars_dir, mat_jar)
    os.makedirs(out_dir, exist_ok=True)
    print(out_dir)
    print(samples)

    for s in samples:
        print(s)
        data = np.load(os.path.join(pickle_jars_dir, mat_jar, s), allow_pickle=True)

        timestamps = data["timestamps"]
        pressures = data["pressures"]
        net_velocities = data["net_velocities"]

        start_time = timestamps[0]
        times = np.array([(t - start_time).total_seconds() for t in timestamps])

        s_name = os.path.splitext(s)[0]

        plt.figure()
        plt.plot(times, pressures)
        plt.xlabel("Time (s)")
        plt.ylabel("Pressure")
        plt.title("Pressure vs Time")
        plt.ylim(bottom=0)
        plt.ylim(top=30)
        plt.xlim(left=0)
        out_path = os.path.join(out_dir, f"{s_name}_TP.png")
        plt.savefig(out_path)
        aio_path = os.path.join(visual_jars_aio_dir, f"{mat_jar}_{s_name}_TP.png")
        plt.savefig(aio_path)
        plt.close()

        plt.figure()
        plt.plot(times, net_velocities)
        plt.xlabel("Time (s)")
        plt.ylabel("Net Joint Velocity")
        plt.xlim(left=0)
        out_path = os.path.join(out_dir, f"{s_name}_TNV.png")
        plt.savefig(out_path)
        aio_path = os.path.join(visual_jars_aio_dir, f"{mat_jar}_{s_name}_TNV.png")
        plt.savefig(aio_path)
        plt.close()

print("pickles plotted!")