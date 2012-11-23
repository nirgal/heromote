#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# heromote - remotely control gopro here cameras
# Copyright (C) 2012 Jean-Michel Vourgère
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
from time import sleep
import struct
import urllib.request

PASSWORD=None

GP_PARAM_READ  = 1
GP_PARAM_WRITE = 2

CAMERA_PARAMETERS = {
    'CM': {
        'txt': 'Camera mode',
        'perm': GP_PARAM_READ | GP_PARAM_WRITE,
        'values': {
            0: 'Video',
            1: 'Photo',
            2: 'Burst',
            3: 'Time Lapse',
            4: 'Delayed',
            5: 'Play',
            7: 'Config',
            },
        },
    'DM': {
        'txt': 'Default mode',
        'perm': GP_PARAM_READ | GP_PARAM_WRITE,
        'values': {
            0: 'Video',
            1: 'Photo',
            2: 'Burst',
            3: 'Time Lapse',
            },
        },
    'TI': {
        'txt': 'Time lapse',
        'perm': GP_PARAM_READ | GP_PARAM_WRITE,
        'values': {
            0: '0.5 s',
            1: '1 s',
            2: '2 s',
            5: '5 s',
            10: '10 s',
            30: '30 s',
            60: '60 s',
            },
        },
    'EX': {
        'txt': 'Spot',
        'perm': GP_PARAM_READ | GP_PARAM_WRITE,
        'values': {
            0: 'Off',
            1: 'On',
            },
        },
    'AO': {
        'txt': 'Auto poweroff',
        'perm': GP_PARAM_READ | GP_PARAM_WRITE,
        'values': {
            0: 'Never',
            1: '60 s',
            2: '120 s',
            3: '300 s',
            },
        },
    'FV': {
        'txt': '1080p field of view',
        'perm': GP_PARAM_READ | GP_PARAM_WRITE,
        'values': {
            0: 'Wide',
            1: 'Medium',
            2: 'Narrow',
            },
        },
    'PR': {
        'txt': 'Photo resolution',
        'perm': GP_PARAM_READ | GP_PARAM_WRITE,
        'values': {
            0: '11MP wide',
            1: '8MP medium',
            2: '5MP wide',
            3: '5MP medium',
            },
        },
    'VR': {
        'txt': 'Video resolution',
        'perm': GP_PARAM_READ | GP_PARAM_WRITE,
        'values': {
            0: 'WVGA 50',
            1: 'WVGA 100',
            2: '720p 25',
            3: '720p 50',
            4: '960p 25',
            5: '960p 50',
            6: '1080p 25',
            7: '1080p 30 Protune',
            11: '1080p 25 Protune',
            8: '1080p 24 Protune',
            9: '960p 48 Protune',
            10: '720p 60 Protune',
            },
        },
    'PH': { # Name is a guess
        'txt': 'Printed hours',
        'perm': GP_PARAM_READ,
        },
    'PM': { # Name is a guess
        'txt': 'Printed minutes',
        'perm': GP_PARAM_READ,
        },
    'PS': { # Name is a guess
        'txt': 'Printed seconds',
        'perm': GP_PARAM_READ,
        },
    'BS': {
        'txt': 'Beep sound',
        'perm': GP_PARAM_READ | GP_PARAM_WRITE,
        'values': {
            0: 'Off',
            1: '70%',
            2: '100%',
            },
        },
    'LB': {
        'txt': 'Led blinking',
        'perm': GP_PARAM_READ | GP_PARAM_WRITE,
        'values': {
            0: 'Off',
            1: '2',
            2: '4',
            },
        },
    'PV': {
        'txt': 'Preview',
        'perm': GP_PARAM_READ | GP_PARAM_WRITE,
        'values': {
            0: 'Off',
            1: 'On', # ffplay "http://10.5.5.9:8080/live/amba.m3u8"
            },
        },
    'UP': {
        'txt': 'Upside Down',
        'perm': GP_PARAM_READ | GP_PARAM_WRITE,
        'values': {
            0: 'Off',
            1: 'On',
            },
        },
    'OS': { # Name is a guess
        'txt': 'On screen display',
        'perm': GP_PARAM_READ,
        'values': {
            0: 'Off',
            1: 'On',
            },
        },
    'VM': {
        'txt': 'PAL',
        'perm': GP_PARAM_READ | GP_PARAM_WRITE,
        'values': {
            0: 'Off',
            1: 'On',
            },
        },
    'LL': {
        'txt': 'Locate',
        'perm': GP_PARAM_READ | GP_PARAM_WRITE,
        'values': {
            0: 'Off',
            1: 'On',
            },
        },
    'US': {
        'txt': 'USB mode',
        'perm': GP_PARAM_READ,
        'values': {
            0: 'Off',
            1: 'On',
            },
        },
    'BL': {
        'txt': 'Battery level',
        'perm': GP_PARAM_READ,
        },
    'BC': {
        'txt': 'Battery charging',
        'perm': GP_PARAM_READ,
        },
    'SH': {
        'txt': 'Shoot',
        'perm': GP_PARAM_READ | GP_PARAM_WRITE,
        'values': {
            0: 'Off',
            1: 'On',
            },
        },
    'RP': { # Name is a guess
        'txt': 'Remaining photo',
        'perm': GP_PARAM_READ,
        },
    'NP': { # Name is a guess
        'txt': 'Number of photos',
        'perm': GP_PARAM_READ,
        },
    'RV': { # Name is a guess
        'txt': 'Remaining video minutes',
        'perm': GP_PARAM_READ,
        },
    'NV': { # Name is a guess
        'txt': 'Number of videos',
        'perm': GP_PARAM_READ,
        },
    'DL': {
        'txt': 'Delete last',
        'perm': GP_PARAM_WRITE,
        },
    'DA': {
        'txt': 'Delete all',
        'perm': GP_PARAM_WRITE,
        },
    'TM': {
        'txt': 'Date/Time',
        'perm': GP_PARAM_WRITE,
        # time set: TM?p=%0c%0b%14%16%23%32 (yMDhms) \00+yMDhms
        },
    'AI': {
        'txt': 'Unkown AI parameter (audio input?)',
        'perm': GP_PARAM_WRITE,
        'values': {
            0: 'Unknown value 0',
            1: 'Unknown value 1',
            2: 'Unknown value 2',
            3: 'Unknown value 3',
            4: 'Unknown value 4',
            5: 'Unknown value 5',
            6: 'Unknown value 6',
            },
        },
    'MM': {
        'txt': 'Unkown MM parameter', # mic mode ?
        'perm': GP_PARAM_WRITE,
        'values': {
            0: 'Unknown value 0',
            1: 'Unknown value 1',
            },
        },
    'PI': { # Ping cam ?
        'txt': 'Unkown PI parameter',
        'perm': GP_PARAM_WRITE,
        },
    'CN': {
        'txt': 'Unkown CN parameter',
        'perm': GP_PARAM_WRITE,
        },
    'OB': {
        'txt': 'One button mode',
        'perm': GP_PARAM_WRITE,
        'values': {
            0: 'Off',
            1: 'On',
            },
        },
    #PB...
    #DF... delete file?
    #IF
    #WI -> 0 disables wifi. can be sent to either /bacac or /camera
    #BM -> 0, 1 or 2  blue booth mode ? can be sent to either /bacac or /camera
    #PM
    #BO -> /bacpac 0=off
    #OO
    #BP
    #SP
    #DS 0/1
    #HS
    #WS
    #IT
    #JW jump wifi mode?
    #
    'PW': {
        'txt': 'Camera power',
        'perm': GP_PARAM_WRITE,
        'values': {
            0: 'Off',
            1: 'On',
            2: 'Unknown',
            },
        },
    }


__opener__ = None
def httpopen(url):
    global __opener__
    if __opener__ is None:
        __opener__ = urllib.request.build_opener()
    http_response = __opener__.open(url)
    return http_response


bcv = httpopen('http://10.5.5.9/bacpac/cv').read()
print('bacpac CV:', repr(bcv))
bacpac_version = struct.unpack('BBB', bcv[9:12])
bacpac_version = '.'.join([str(x) for x in bacpac_version])
print('bacpac version:', bacpac_version)
bacpac_mac = bcv[12:18]
bacpac_mac = ':'.join(['%02x' % x for x in bacpac_mac])
print('bacpac mac:', bacpac_mac)
bacpac_name = bcv[19:].decode('utf-8')
print('bacpac name:', bacpac_name)

bsd = httpopen('http://10.5.5.9/bacpac/sd').read()
print('bacpac SD:', repr(bsd))
PASSWORD = bsd[2:].decode('utf-8')
print('bacpac password', PASSWORD)
 
try:
    ccv = httpopen('http://10.5.5.9/camera/cv').read()
    print('camera CV:', repr(ccv))
    # b'\x00\x00\x01\x13HD2.08.12.198.47.00\x05HERO2'
    dlen = struct.unpack('B', ccv[3:4])[0]
    camera_version = ccv[4:4+dlen].decode('UTF-8')
    print('camera version', camera_version)
    ipos = 4+dlen
    dlen = struct.unpack('B', ccv[ipos:ipos+1])[0]
    ipos += 1
    camera_model = ccv[ipos:ipos+dlen].decode('UTF-8')
    print('camera_model', camera_model)
except urllib.error.HTTPError:
    print('Error communicating with camera')


def perm_to_text(reg):
    read_flag = (reg['perm'] & GP_PARAM_READ) and 'r' or '-'
    write_flag = (reg['perm'] & GP_PARAM_WRITE) and 'w' or '-'
    return read_flag + write_flag

def print_reg(name, value):
    cam_reg = CAMERA_PARAMETERS[name]
    if 'values' in cam_reg:
        disp_value = '%s (%s)' % (value, cam_reg['values'][value])
    else:
        disp_value = '%s' % value
    print ('%s %s (%s): %s' % (
        name,
        perm_to_text(cam_reg),
        cam_reg['txt'],
        disp_value,
        ))

def dump_bacpac():
    bse = httpopen('http://10.5.5.9/bacpac/se?t=%s' % PASSWORD).read()
    print("bacpac SE:", repr(bse))
    pad0, bacpac_battery, pad1, pad2, pad3, pad4, pad5, pad6, pad7, pad8, pad9, pada, padb, padc, padd, pade = struct.unpack('BbBBBBBBBBBBBBBB', bse)
    assert pad0 == 0
    if bacpac_battery == -1:
        print("bacpac battery: charging")
    elif bacpac_battery == -2:
        print("bacpac battery: using camera power")
    else:
        print('bacpac battery:', bacpac_battery, '%')
    print ('pad1:', pad1)
    print ('pad2:', pad2)
    print ('pad3:', pad3)
    print ('pad4:', pad4)
    print ('pad5:', pad5)
    print ('pad6:', pad6)
    print ('pad7:', pad7)
    print ('pad8:', pad8)
    print ('pad9:', pad9)
    print ('pada:', pada)
    print ('padb:', padb)
    print ('padc:', padc)
    print ('Cam attached:', padd)
    print ('pade:', pade)
    #cam off:               6:0 7:0  8:0 9:1 a:0 b:255 c:255 e:0
    #usb mode only, cam on: 6:0 7:0  8:1 9:0 a:1 b:1   c:0   e:0
    #cam fully on:          6:0 7:34 8:1 9:0 a:1 b:1   c:0   e:1

def dump_camera():
    try:
        cse = httpopen('http://10.5.5.9/camera/se?t=%s' % PASSWORD).read()
    except urllib.error.HTTPError:
        print ("Can't access camera")
        return
    #print("camera SE: ", repr(cse))
    decoded_cse = struct.unpack('>BBBBBBBBBBBBBBBBBBBBBhhhhBB', cse)
    pad0, mode, pad1, default_mode, spot, time_lapse, autooff, video_fov, photo_res, video_res, pad2, pad3, disp_hour, disp_min, disp_sec, pad7, sound, led, flags, battery, pad8, remaining_photo, nphoto, remaining_video_min, nvideo, shoot, pada = decoded_cse
    assert pad0 == 0
    assert pad3 == 255
    preview = bool(flags & 0x01)
    updown = bool(flags & 0x04)
    osd = bool(flags & 0x10)
    pal = bool(flags & 0x20) 
    locate = bool(flags & 0x40) 
    usb = bool(flags & 0x80)
    assert flags & 0x06 == 0
    charging = bool(battery & 0x80)
    battery = battery & 0x7F

    print_reg('CM', mode)
    print ('pad1 (audio):', pad1)
    print_reg('DM', default_mode)
    print_reg('TI', time_lapse)
    print_reg('EX', spot)
    print_reg('AO', autooff)
    print_reg('FV', video_fov)
    print_reg('PR', photo_res)
    print ('pad2 (audio):', pad2)
    print_reg('VR', video_res)
    print_reg('PH', disp_hour)
    print_reg('PM', disp_min)
    print_reg('PS', disp_sec)
    print ('pad7 (playback):', pad7) # playback
    print_reg('BS', sound)
    print_reg('LB', led)
    #print ('flag:', flags)
    print_reg('PV', preview)
    print_reg('UP', updown)
    print_reg('OS', osd)
    print_reg('VM', pal)
    print_reg('LL', locate)
    print_reg('US', usb)
    print_reg('BL', battery)
    print_reg('BC', charging)
    print ('pad8:', pad8)
    print_reg('RP', remaining_photo)
    print_reg('NP', nphoto)
    print_reg('RV', remaining_video_min)
    print_reg('NV', nvideo)
    print_reg('SH', shoot)
    print ('pada:', pada) # busy=1 videorec=2 PVready+pic=4 usb_only=4 video_mode=6
    #                 4 2 1
    # Setup/Lapse     0 0 0
    # BusyBurst       0 0 X
    # Video rec       0 X 0
    # Photo/USB       X 0 0
    # VideoOnT        X X 0
    #amba404 -> "preview now supported"



def main():
    from optparse import OptionParser
    parser = OptionParser(usage='%prog [options] { dump | monitor | list [RR] | RR=value}')
    parser.add_option('-t', '--target',
        action='store', dest='target', default='auto',
        help='Specifiy where to send command. Default=auto. Allowed values=auto,camera,bacpac')

    options, args = parser.parse_args()

    if len(args) < 1:
        print ("missing argument", file=sys.stderr)
        sys.exit(1)

    if args[0] == 'dump':
        dump_bacpac()
        dump_camera()
        return
    
    if args[0] == 'monitor':
        while True:
            dump_bacpac()
            dump_camera()
            sleep(1)
    
    if args[0] == 'list':
        if len(args) == 1:
            for reg_name in CAMERA_PARAMETERS:
                reg = CAMERA_PARAMETERS[reg_name]
                print(perm_to_text(reg), reg_name, reg['txt'])
        else:
            for reg_name in args[1:]:
                reg = CAMERA_PARAMETERS[reg_name]
                if reg['perm'] == GP_PARAM_READ:
                    txtperm = 'READONLY'
                elif reg['perm'] == GP_PARAM_WRITE:
                    txtperm = 'READONLY'
                elif reg['perm'] == GP_PARAM_READ | GP_PARAM_WRITE:
                    txtperm = 'READ+WRITE'
                else:
                    txtperm = ''
                print(reg_name, ':', reg['txt'], '(', txtperm, ')')
                if 'values' in reg:
                    for val, txt in reg['values'].items():
                        print('\t', val, ':', txt)
        return
        
    command = args[0].split('=', 1)
    assert(len(command) == 2)
    reg_name, value = command
    print (reg_name, '<-', value)
    value = int(value)
    assert value < 256
    target = options.target
    if target == 'auto':
        if reg_name in ('PW', 'WI', 'BM'): # sent to the bacpac, not the camera
            target = 'bacpac'
        else:
            target = 'camera'
    url = 'http://10.5.5.9/' + target + '/'+ reg_name + '?t=' + PASSWORD + '&p=%' + '%02x' % value
    print (url)
    rsp = httpopen(url).read()
    print ("HTTP response:", rsp)
    print_reg(reg_name, value)



if __name__ == '__main__':
    main()
