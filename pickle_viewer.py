import numpy as np
import matplotlib.pyplot as plt

data = np.load("mat1_low-med.npz", allow_pickle=True)

timestamps = data["timestamps"]
pressures = data["pressures"]
net_velocities = data["net_velocities"]

start_time = timestamps[0]
times = np.array([(t - start_time).total_seconds() for t in timestamps])

plt.figure()
plt.plot(times, pressures)
plt.xlabel("Time (s)")
plt.ylabel("Pressure")
plt.title("Pressure vs Time")
plt.show()

plt.figure()
plt.plot(times, net_velocities)
plt.xlabel("Time (s)")
plt.ylabel("Net Joint Velocity")
plt.title("Net Velocity vs Time")
plt.show()

plt.figure()

plt.plot(times, pressures, label="Pressure")
plt.plot(times, net_velocities, label="Net Velocity")

plt.xlabel("Time (s)")
plt.title("Pressure & Velocity vs Time")
plt.legend()

plt.show()