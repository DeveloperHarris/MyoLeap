# Leap Motion Imports
import os, sys, inspect
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib/leap/x64' if sys.maxsize > 2**32 else '../leap/lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))
import Leap


# Open Myo Imports
import open_myo as myo

def main():

    # Setup LeapMotion Controller
    controller = Leap.Controller()
    print('Leap Controller Setup')


    def process_emg(emg, last_quat, last_acc, last_gyro):
        frame = controller.frame()
        hands = frame.hands

        if (hands.is_empty):
            pass
        else:
            print('EMG: ', emg, 'IMU: ', (last_quat, last_acc, last_gyro), 'Frame: ', frame.serialize)


    def process_imu(quat, acc, gyro, last_emg):
        pass
        
    def process_sync(arm, x_direction):
        print(arm, x_direction)

    def process_classifier(pose):
        print(pose)

    def process_battery(batt):
        print("Battery level: %d" % batt)

    def led_emg(emg):
        if(emg[0] > 80):
            myo_device.services.set_leds([255, 0, 0], [128, 128, 255])
        else:
            myo_device.services.set_leds([128, 128, 255], [128, 128, 255])


    # Setup Myo EMG Band
    myo_mac_addr = myo.get_myo()
    print("Myo MAC address: %s" % myo_mac_addr)
    myo_device = myo.Device()
    myo_device.services.sleep_mode(1) # never sleep
    myo_device.services.set_leds([128, 128, 255], [128, 128, 255])  # purple logo and bar LEDs)
    myo_device.services.vibrate(1) # short vibration
    fw = myo_device.services.firmware()
    print("Myo Firmware version: %d.%d.%d.%d" % (fw[0], fw[1], fw[2], fw[3]))
    batt = myo_device.services.battery()
    print("MYO Battery level: %d" % batt)
    # myo_device.services.emg_filt_notifications()
    myo_device.services.emg_raw_notifications()
    myo_device.services.imu_notifications()
    # myo_device.services.classifier_notifications()
    myo_device.services.battery_notifications()
    myo_device.services.set_mode(myo.EmgMode.RAW_UNFILT, myo.ImuMode.DATA, myo.ClassifierMode.ON)
    myo_device.add_emg_event_handler(process_emg)
    # myo_device.add_emg_event_handler(led_emg)
    myo_device.add_imu_event_handler(process_imu)
    # myo_device.add_sync_event_handler(process_sync)
    # myo_device.add_classifier_event_hanlder(process_classifier)

    while True:
        if myo_device.services.waitForNotifications(1):
            continue
        print("Waiting...")

if __name__ == "__main__":
    main()


