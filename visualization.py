import numpy as np
import time
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import serial
import struct
import tkinter as tk

def read_serial(show_z):
    #serial port communication
    #boolean variable show_z determines if z axis should be returned
    ser = serial.Serial('COM9', 1000000, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE)

    roll = 0
    pitch = 0
    yaw = 0

    #averaging over 10 samples in order to reduce fluctuations
    samples = 10
    for i in range(samples):
        data1 = ser.read(4)
        data2 = ser.read(4)
        data3 = ser.read(4)
        roll_temp, = struct.unpack('<f', data1)
        pitch_temp, = struct.unpack('<f', data2)
        yaw_temp, = struct.unpack('<f', data3)
        roll += roll_temp
        pitch += pitch_temp
        yaw += yaw_temp

    ser.close()

    roll /= samples
    pitch /= samples
    yaw /= samples


    if show_z:
        return [-pitch, -roll, -yaw]
    else:
        return [-pitch, -roll, 0]



def rotateXYZ(node, angles):
    #function rotating point in 3d space by angles in 3 axes
    x = node[0]
    y = node[1]
    z = node[2]
    roll = angles[0]
    pitch = angles[1]
    yaw = angles[2]
    #rotate around x
    y = y * np.cos(roll) - z * np.sin(roll)
    z = z * np.cos(roll) + y * np.sin(roll)
    # rotate around y
    x = x * np.cos(pitch) - z * np.sin(pitch)
    z = z * np.cos(pitch) + x * np.sin(pitch)
    # rotate around z
    x = x * np.cos(yaw) - y * np.sin(yaw)
    y = y * np.cos(yaw) + x * np.sin(yaw)

    return [x, y, z]

def plot_data():
    #when global variable plot_on is True function acts as loop in tkinter gui

    global calibration

    #set of nodes making rectangle representing sensor board in 3d space
    nodes = [[-1, -1, 0], [1, -1, 0], [1, 1, 0], [-1, 1, 0]]

    x = []
    y = []
    z = []

    angles = read_serial(c1_state)
    angles[0] -= calibration[0]
    angles[1] -= calibration[1]
    if c1_state:
        angles[2] -= calibration[2]

    for node in nodes:
        xyz = rotateXYZ(node, angles)
        x.append(xyz[0])
        y.append(xyz[1])
        z.append(xyz[2])

    #converting angles from radian to degrees
    x_val = angles[0] * 180 / np.pi
    y_val = angles[1] * 180 / np.pi
    z_val = angles[2] * 180 / np.pi

    #updating labels
    lb_x_val.configure(text=f"{x_val:.3f}")
    lb_y_val.configure(text=f"{y_val:.3f}")
    lb_z_val.configure(text=f"{z_val:.3f}")

    #setting up canvas and plotting nodes
    ax.cla()
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_xlim3d(-2, 2)
    ax.set_ylim3d(-2, 2)
    ax.set_zlim3d(-2, 2)
    ax.plot_trisurf(x, y, z)
    plt.draw()

    if plot_on:
        #calling plot_data function with after method makes it act as infinite loop
        window.after(200, plot_data)
    else:
        ax.cla()


def c1_toggle():
    global c1_state
    c1_state = not c1_state

def plot_start():
    global plot_on
    plot_on = True
    plot_data()

def plot_stop():
    global plot_on
    plot_on = False


calibration = read_serial(True)
#matplotlib real time 3d plot setup
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

plot_on = False

#gui setup
window = tk.Tk()
window.title("Gyroscope")

btn1 = tk.Button(window,text = "start", command = plot_start)
btn1.grid(column=0, row=0)
btn2 = tk.Button(window,text = "stop", command = plot_stop)
btn2.grid(column=0, row=2)

c1_state = False
c1 = tk.Checkbutton(window, text = "enable z axis",command = c1_toggle)
c1.grid(column=0, row=1)

#angle labels
lb_x_txt = tk.Label(window, text="roll:")
lb_x_txt.grid(column=1, row=0)
lb_x_val = tk.Label(window, text="0.000")
lb_x_val.grid(column=2, row=0)
lb_y_txt = tk.Label(window, text="pitch:")
lb_y_txt.grid(column=1, row=1)
lb_y_val = tk.Label(window, text="0.000")
lb_y_val.grid(column=2, row=1)
lb_z_txt = tk.Label(window, text="yaw:")
lb_z_txt.grid(column=1, row=2)
lb_z_val = tk.Label(window, text="0.000")
lb_z_val.grid(column=2, row=2)

window.mainloop()