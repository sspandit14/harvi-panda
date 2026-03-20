import pickle
import numpy as np
import os
from datetime import datetime
import argparse

def get_timestamp(f_name):
    f_name = f_name.replace(".pkl", "")
    f_name = f_name.replace("_", ":")
    f_name = f_name.replace("T", " ")

    return datetime.fromisoformat(f_name)

def jar_pickles(d_name):
    pickles = sorted([p for p in os.listdir(d_name) if p.endswith(".pkl")])

    print("Found", len(pickles), "pickle files")

    times = []
    pressures = []
    joint_positions = []
    joint_velocities = []
    net_velocities = []
    ee_pos_quats = []

    for p in pickles:
        path = os.path.join(d_name, p)

        with open(path, "rb") as f:
            data = pickle.load(f)

        times.append(get_timestamp(p))
        pressures.append(data["pressure"][0])
        joint_positions.append(data["joint_positions"])
        jv = data["joint_velocities"]
        joint_velocities.append(jv)
        net_velocities.append(np.linalg.norm(jv))
        ee_pos_quats.append(data["ee_pos_quat"])

    pickle_jar = {
        "timestamps": np.array(times),
        "pressures": np.array(pressures),
        "joint_positions": np.array(joint_positions),
        "joint_velocities": np.array(joint_velocities),
        "net_velocities": np.array(net_velocities),
    }

    return pickle_jar

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-dir", "--Directory")
    args = parser.parse_args()

    f_dir = "df"

    if args.Directory:
        f_dir = args.Directory
    else:
        print("Enter directory name bozo")
        exit()

    print(f_dir)

    pickle_jar = jar_pickles(f_dir)
    
    np.savez(
        f"{f_dir}.npz",
        timestamps=pickle_jar["timestamps"],
        pressures=pickle_jar["pressures"],
        joint_positions=pickle_jar["joint_positions"],
        joint_velocities=pickle_jar["joint_velocities"],
        net_velocities=pickle_jar["net_velocities"],
    )

if __name__ == "__main__":
    main()