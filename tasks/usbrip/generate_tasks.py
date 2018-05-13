import random
import argparse
import re
import datetime
import string
import json
import os.path
import shutil

ALPHABET = string.ascii_uppercase+string.digits
VENDORS = ['JetFlash', 'Atmel Corp.', 'HP', 'Kingston', 'Saitek', 'Toshiba']
with open('flags.json') as file:
    FLAGS = json.load(file)
DIRNAME = 'tasks'
LOG_PATH = './clear_log.log'

TEMPLATE = '''{attach} ubuntu-Lenovo-G500 kernel: usb 3-1: new high-speed USB device number 2 using xhci_hcd
{attach} ubuntu-Lenovo-G500 kernel: usb 3-1: New USB device found, idVendor=8564, idProduct=1000
{attach} ubuntu-Lenovo-G500 kernel: usb 3-1: New USB device strings: Mfr=1, Product=2, SerialNumber=3
{attach} ubuntu-Lenovo-G500 kernel: usb 3-1: Product: Mass Storage Device
{attach} ubuntu-Lenovo-G500 kernel: usb 3-1: Manufacturer: {vendor}
{attach} ubuntu-Lenovo-G500 kernel: usb 3-1: SerialNumber: {serial}{flag_letter}
{attach} ubuntu-Lenovo-G500 mtp-probe: checking bus 3, device 2: "/sys/devices/pci0000:00/0000:00:14.0/usb3/3-1"
{attach} ubuntu-Lenovo-G500 mtp-probe: bus: 3, device: 2 was not an MTP device
{attach} ubuntu-Lenovo-G500 kernel: usb-storage 3-1:1.0: USB Mass Storage device detected
{attach} ubuntu-Lenovo-G500 kernel: scsi host4: usb-storage 3-1:1.0
{attach} ubuntu-Lenovo-G500 kernel: usbcore: registered new interface driver usb-storage
{attach} ubuntu-Lenovo-G500 kernel: usbcore: registered new interface driver uas
{attach} ubuntu-Lenovo-G500 kernel: scsi 4:0:0:0: Direct-Access     JetFlash Transcend 8GB    8.07 PQ: 0 ANSI: 4
{attach} ubuntu-Lenovo-G500 kernel: sd 4:0:0:0: Attached scsi generic sg2 type 0
{attach} ubuntu-Lenovo-G500 kernel: sd 4:0:0:0: [sdc] 15679488 512-byte logical blocks: (8.03 GB/7.48 GiB)
{attach} ubuntu-Lenovo-G500 kernel: sd 4:0:0:0: [sdc] Write Protect is off
{attach} ubuntu-Lenovo-G500 kernel: sd 4:0:0:0: [sdc] Mode Sense: 23 00 00 00
{attach} ubuntu-Lenovo-G500 kernel: sd 4:0:0:0: [sdc] Write cache: disabled, read cache: enabled, doesn't support DPO or FUA
{attach} ubuntu-Lenovo-G500 kernel:  sdc: sdc1
{attach} ubuntu-Lenovo-G500 kernel: sd 4:0:0:0: [sdc] Attached SCSI removable disk
{attach} ubuntu-Lenovo-G500 dbus[832]: [system] Activating via systemd: service name='org.freedesktop.hostname1' unit='dbus-org.freedesktop.hostname1.service'
{attach} ubuntu-Lenovo-G500 systemd[1]: Starting Hostname Service...
{attach} ubuntu-Lenovo-G500 udisksd[805]: Mounted /dev/sdc1 at /media/sanyabas/ESD-USB on behalf of uid 1000
{attach} ubuntu-Lenovo-G500 dbus[832]: [system] Successfully activated service 'org.freedesktop.hostname1'
{attach} ubuntu-Lenovo-G500 systemd[1]: Started Hostname Service.
{attach} ubuntu-Lenovo-G500 dbus-daemon[2589]: Activating service name='org.gnome.Shell.HotplugSniffer'
{attach} ubuntu-Lenovo-G500 dbus-daemon[2589]: Successfully activated service 'org.gnome.Shell.HotplugSniffer'
{attach} ubuntu-Lenovo-G500 nautilus[5147]: Called "net usershare info" but it failed: Failed to execute child process “net” (No such file or directory)
{attach} ubuntu-Lenovo-G500 systemd[1]: Starting Cleanup of Temporary Directories...
{attach} ubuntu-Lenovo-G500 systemd-tmpfiles[5219]: [/usr/lib/tmpfiles.d/var.conf:14] Duplicate line for path "/var/log", ignoring.
{attach} ubuntu-Lenovo-G500 systemd[1]: Started Cleanup of Temporary Directories.
{attach} ubuntu-Lenovo-G500 dbus-daemon[2589]: Activating via systemd: service name='org.gnome.zeitgeist.Engine' unit='zeitgeist.service'
{attach} ubuntu-Lenovo-G500 systemd[2573]: Starting Zeitgeist activity log service...
{attach} ubuntu-Lenovo-G500 zeitgeist-maybe-vacuum[5279]: Performing VACUUM operation... OK
{attach} ubuntu-Lenovo-G500 dbus-daemon[2589]: Activating via systemd: service name='org.gnome.zeitgeist.SimpleIndexer' unit='zeitgeist-fts.service'
{attach} ubuntu-Lenovo-G500 dbus-daemon[2589]: Successfully activated service 'org.gnome.zeitgeist.Engine'
{attach} ubuntu-Lenovo-G500 systemd[2573]: Started Zeitgeist activity log service.
{attach} ubuntu-Lenovo-G500 systemd[2573]: Starting Zeitgeist full-text search indexer...
{attach} ubuntu-Lenovo-G500 zeitgeist-daemon[5290]: #033[31m[11:31:31.207115 WARNING]#033[0m zeitgeist-daemon.vala:334: Failed to execute child process “zeitgeist-datahub” (No such file or directory)
{attach} ubuntu-Lenovo-G500 zeitgeist-daemon[5290]: #033[31m[11:31:31.208333 WARNING]#033[0m zeitgeist-daemon.vala:127: Unable to parse version info!
{attach} ubuntu-Lenovo-G500 zeitgeist-daemon[5290]: #033[31m[11:31:31.212080 WARNING]#033[0m zeitgeist-daemon.vala:127: Unable to parse version info!
{attach} ubuntu-Lenovo-G500 dbus-daemon[2589]: Successfully activated service 'org.gnome.zeitgeist.SimpleIndexer'
{attach} ubuntu-Lenovo-G500 systemd[2573]: Started Zeitgeist full-text search indexer.
{attach} ubuntu-Lenovo-G500 dbus-daemon[2589]: Activating service name='org.gnome.Nautilus'
{attach} ubuntu-Lenovo-G500 dbus-daemon[2589]: Successfully activated service 'org.gnome.Nautilus'
{attach} ubuntu-Lenovo-G500 dbus[832]: [system] Activating via systemd: service name='org.freedesktop.hostname1' unit='dbus-org.freedesktop.hostname1.service'
{attach} ubuntu-Lenovo-G500 systemd[1]: Starting Hostname Service...
{attach} ubuntu-Lenovo-G500 dbus[832]: [system] Successfully activated service 'org.freedesktop.hostname1'
{attach} ubuntu-Lenovo-G500 systemd[1]: Started Hostname Service.
{attach} ubuntu-Lenovo-G500 nautilus[5405]: Called "net usershare info" but it failed: Failed to execute child process “net” (No such file or directory)
{deattach} ubuntu-Lenovo-G500 udisksd[805]: Cleaning up mount point /media/sanyabas/ESD-USB (device 8:33 is not mounted)
{deattach} ubuntu-Lenovo-G500 udisksd[805]: Unmounted /dev/sdc1 on behalf of uid 1000
{deattach} ubuntu-Lenovo-G500 kernel: usb 3-1: USB disconnect, device number 2'''


def read_log(path):
    with open(path) as file:
        return file.readlines()


def clear_log(lines):
    reg = re.compile('usb|identity|gnome-calendar|dhcp4|ureadahead')
    return list(filter(lambda line: not bool(reg.search(line)), lines))


def generate_usb_events(path, team_id, flag):
    lines = read_log(path)
    lines = clear_log(lines)
    result = lines
    prev_number = 0
    for char in flag:
        number = random.randint(prev_number, min(
            prev_number+1000, len(result)-1))
        number = find_split(result[number][:15], result, number)
        line = result[number]
        date_part = line[:15]
        prev_number += 1700
        print(char, number)
        result = generate_usb_event(result, number, date_part, char)
    with open(os.path.join(DIRNAME, f'{team_id}.log'), 'w') as file:
        file.writelines(result)


def find_split(date_part, lines, index):
    reg = re.compile(date_part)
    for num in range(index, len(lines)):
        if reg.search(lines[num]):
            continue
        return num-1


def generate_flash():
    serial = ''.join([random.choice(ALPHABET) for _ in range(8)])
    vendor = random.choice(VENDORS)
    return vendor, serial


def generate_usb_event(lines, index, date_part, flag_letter):
    fmt = '%b %d %H:%M:%S'
    parsed = datetime.datetime.strptime(date_part, fmt)
    deattach = parsed+datetime.timedelta(seconds=1)
    str_attach = parsed.strftime(fmt)
    str_deattach = deattach.strftime(fmt)
    vendor, serial = generate_flash()
    event = TEMPLATE.format(attach=str_attach, flag_letter=flag_letter,
                            deattach=str_deattach, vendor=vendor, serial=serial)
    with_endings = map(lambda st: st+'\n', event.split('\n'))
    return insert(lines, index, with_endings)


def insert(arr, index, elems):
    result = arr[:index+1]
    result.extend(elems)
    result.extend(arr[index+1:])
    return result


def main():
    if os.path.exists(DIRNAME):
        shutil.rmtree(DIRNAME, ignore_errors=True)
    os.makedirs(DIRNAME)
    for team_id, flag in FLAGS:
        generate_usb_events(LOG_PATH, team_id, flag)


if __name__ == '__main__':
    main()
