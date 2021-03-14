# Geotech d-file extractor
# Point to directory containing d-files
# program will generate a .csv ascii file
# named VTEMExtracted with data at GPS freq
#
# v0.1 - original program
# v0.2 - added line no to extracted string
# v0.3 - added system log text file to end of read
# v0.4 - added speed in knots and climb rate in ft/min
# v0.5 - add data checks
# v0.6 - GPGGA data check modified to include length only
# v0.7 - Fixed GPGGA data check to exclude empty strings
# v0.9 - Change code to Python v3.9
# v1.0 - Start with code cleanup and syntax changes, auto read channels
# v1.1 - Add ability to select multiple files
# v1.2 - Add GUI with checkbox
# v1.3 - Add Gyro extraction
# v1.4 - Port GUI to wx, check if files exist before overwriting

from tkinter import *
import os
import csv
import math
from geotech import *

master = Tk()


def distance(lat1, lng1, lat2, lng2):
    # return distance as meter if you want km distance, remove "* 1000"
    radius = 6371 * 1000

    d_lat = (lat2 - lat1) * math.pi / 180
    d_lng = (lng2 - lng1) * math.pi / 180

    lat1 = lat1 * math.pi / 180
    lat2 = lat2 * math.pi / 180

    val = math.sin(d_lat / 2) * math.sin(d_lat / 2) + math.sin(d_lng / 2) * \
          math.sin(d_lng / 2) * math.cos(lat1) * math.cos(lat2)
    ang = 2 * math.atan2(math.sqrt(val), math.sqrt(1 - val))
    return radius * ang


def vtem_extract():
    file_names = get_file()
    current_path = os.path.realpath(__file__).rsplit("\\", 1)[0]
    # utc = '0'
    lno = '0'
    ralt = '0'
    # lat = '0'
    # lon = '0'
    # height = '0'
    # nosats = '0'
    pkir = '0'
    pkbz = '0'
    pkbx = '0'
    pkby = '0'
    pkvr = '0'
    pksz = '0'
    pksx = '0'
    b = 0
    srz15 = '0'
    srz24 = '0'
    srz33 = '0'
    srz44 = '0'
    brz15 = '0'
    brz24 = '0'
    brz33 = '0'
    brz44 = '0'
    srx15 = '0'
    srx24 = '0'
    srx33 = '0'
    srx44 = '0'
    sry15 = '0'
    sry24 = '0'
    sry33 = '0'
    sry44 = '0'
    rf15 = '0'
    rf24 = '0'
    rf33 = '0'
    rf44 = '0'
    pwl = '0'
    mag1 = '0'
    mag2 = '0'
    lat1 = 0
    lon1 = 0
    height1 = '0'
    # speed = '0'
    # crate = '0'
    total_lines = 0
    gyro1 = '0'
    gyro2 = '0'
    gyro3 = '0'
    header = set()

    files_d = file_names

    path = files_d[0].rsplit('\\', 1)[0]

    print('No files selected : ' + str(len(files_d)))

    open(files_d[0], 'r')
    # readcsv = csv.reader(files_d[0])
    with open(files_d[0], 'r') as infile:
        readcsv = csv.reader(infile)
        for row in readcsv:
            if row[0].startswith('$TDINFO'):
                chsel = str(row[2])
            elif row[0].startswith('$TDTDEM'):
                nomagssel = str(row[11])

    fnameout = path + '\VTEMExtracted.csv'
    fout = open(fnameout, 'w')
    if chsel == "2":
        fout.write('UTC,lno,lat,lon,height,nosats,ralt,pkir,pkbz,'
                   'pkvr,pksz,srz15,srz24,srz33,srz44,brz15,brz24,brz33,'
                   'brz44,rf15,rf24,rf33,rf44,pwline,'
                   'mag1,mag2,speed,climbrate,gyro1,gyro2,gyro3\n')
    elif chsel == "3":
        fout.write('UTC,lno,lat,lon,height,nosats,ralt,pkir,pkbx,pkbz,'
                   'pkvr,pksx,pksz,srz15,srz24,srz33,srz44,brz15,brz24,brz33,'
                   'brz44,srx15,srx24,srx33,srx44,rf15,rf24,rf33,rf44,pwline,'
                   'mag1,mag2,speed,climbrate,gyro1,gyro2,gyro3\n')
    elif chsel == "4":
        fout.write('UTC,lno,lat,lon,height,nosats,ralt,pkir,pkbx,pkby,pkbz,'
                   'pkvr,pksx,pksy,pksz,srz15,srz24,srz33,srz44,brz15,brz24,'
                   'brz33,brz44,srx15,srx24,srx33,srx44,sry15,sry24,sry33,'
                   'sry44,rf15,rf24,rf33,rf44,pwline,mag1,mag2,speed,climbrate,'
                   'gyro1,gyro2,gyro3\n')

    for a in range(len(files_d)):
        print(files_d[a])

        open(files_d[a], 'r')

        # readcsv = csv.reader(files_d[a])

        fout = open(fnameout, 'a')

        print(a + 1)

        with open(files_d[a], 'r') as infile:
            readcsv = csv.reader(infile)

            for row in readcsv:
                header.add(row[0])
                total_lines += 1
                if row[0].startswith('$TDINFO'):
                    # print 'tdinfo'
                    SamplR = str(row[1])
                    Chan = str(row[2])
                    loopd = str(row[3])
                    gain = str(row[7])
                    stype = str(row[9])
                    sn = str(row[10])

                elif row[0].startswith('$TDTDEM'):
                    # print 'tdtdem'
                    Ver = str(row[1])
                    basef = str(row[2])
                    dc = str(row[3])
                    volt = str(row[4])
                    noch = str(row[5])
                    pmon = str(row[9])
                    nomags = str(row[11])

                elif row[0].startswith('$RDALT'):
                    ralt = str(row[1])

                elif row[0].startswith('$LINE'):
                    lno = str(row[1])

                elif row[0].startswith('$TD_PKV'):
                    if row[1] != "nan":
                        pkvr = str(row[1])
                        pksz = str(row[2])
                        if int(noch) > 2:
                            pksx = str(row[3])
                        if int(noch) == 4:
                            pksy = str(row[4])

                elif row[0].startswith('$TD_PKI'):
                    if row[1] != "nan":
                        pkir = str(row[1])
                        pkbz = str(row[2])
                        if int(noch) > 2:
                            pkbx = str(row[3])
                        if int(noch) == 4:
                            pkby = str(row[4])

                elif row[0].startswith('$TD_VZ'):
                    if (len(row) > 45) and (row[15] != "nan"):
                        srz15 = str(row[15])
                        srz24 = str(row[24])
                        srz33 = str(row[33])
                        srz44 = str(row[44])

                elif row[0].startswith('$TD_BZ'):
                    if (len(row) > 45) and (row[15] != "nan"):
                        brz15 = str(row[15])
                        brz24 = str(row[24])
                        brz33 = str(row[33])
                        brz44 = str(row[44])

                elif row[0].startswith('$TD_VX'):
                    if (len(row) > 45) and (row[15] != "nan"):
                        srx15 = str(row[15])
                        srx24 = str(row[24])
                        srx33 = str(row[33])
                        srx44 = str(row[44])

                elif row[0].startswith('$TD_VY'):
                    if (len(row) > 45) and (row[15] != "nan"):
                        sry15 = row[15]
                        sry24 = row[24]
                        sry33 = row[33]
                        sry44 = row[44]

                elif row[0].startswith('$TD_RF'):
                    if (len(row) > 45) and (row[15] != "nan"):
                        rf15 = str(row[15])
                        rf24 = str(row[24])
                        rf33 = str(row[33])
                        rf44 = str(row[44])

                elif row[0].startswith('$PWL'):
                    pwl = str(row[1])

                elif row[0].startswith('$GRD4A'):
                    if len(row) > 2:
                        mag1 = str(row[1])
                        mag2 = str(row[2])

                elif row[0].startswith('$GRDI'):
                    if len(row) > 2:
                        mag1 = str(row[2])

                elif row[0].startswith('$MG'):
                    if len(row) > 2:
                        mag1 = str(row[1].strip())

                elif row[0].startswith('$GYRO'):
                    if len(row) > 3:
                        gyro1 = str(row[1].strip())
                        gyro2 = str(row[2].strip())
                        gyro3 = str(row[3].strip())

                elif row[0].startswith('$GPGGA'):
                    if row[1] != '' and len(row) == 15:
                        utc = str(row[1])
                        lati = row[2]
                        lat_directioni = row[3]
                        loni = row[4]
                        lon_directioni = row[5]
                        nosats = str(row[7])
                        height = str(row[9])

                        crate = (float(height) - float(height1)) * 1000
                        if crate > 5000 or crate < -5000:
                            crate = "0"
                        crate = str(crate)

                        height1 = height

                        # convert latitude
                        if lati.strip():
                            lati = round(math.floor(float(lati) / 100)
                                         + (float(lati) % 100) / 60, 6)
                            if lat_directioni == 'S':
                                lati = lati * -1

                        # convert logitude
                        if loni.strip():
                            loni = round(math.floor(float(loni) / 100)
                                         + (float(loni) % 100) / 60, 6)
                            if lon_directioni == 'W':
                                loni = loni * -1

                        lat = str(lati)
                        lon = str(loni)

                        # speed conversion
                        speed = str(distance(float(lat), float(lon),
                                             lat1, lon1) / 0.1)
                        if float(speed) > 200 or float(speed) < -200:
                            speed = "0"
                        lat1 = float(lat)
                        lon1 = float(lon)

                        if chsel == "2":
                            fout.write(utc + ',' + lno + ',' + lat + ',' +
                                       lon + ',' + height + ',' + nosats + ',' +
                                       ralt + ',' + pkir + ',' + pkbz + ',' +
                                       pkvr + ',' + pksz + ',' + srz15 + ',' +
                                       srz24 + ',' + srz33 + ',' + srz44 + ',' +
                                       brz15 + ',' + brz24 + ',' + brz33 + ',' +
                                       brz44 + ',' + rf15 + ',' + rf24 + ',' +
                                       rf33 + ',' + rf44 + ',' + pwl + ',' +
                                       mag1 + ',' + mag2 + ',' + speed + ',' +
                                       crate + ',' + gyro1 + ',' + gyro2 + ',' +
                                       gyro3 + '\n')
                        elif chsel == "3":
                            fout.write(utc + ',' + lno + ',' + lat + ',' +
                                       lon + ',' + height + ',' + nosats + ',' +
                                       ralt + ',' + pkir + ',' + pkbx + ',' +
                                       pkbz + ',' + pkvr + ',' + pksx + ',' +
                                       pksz + ',' + srz15 + ',' + srz24 + ',' +
                                       srz33 + ',' + srz44 + ',' + brz15 + ',' +
                                       brz24 + ',' + brz33 + ',' + brz44 + ',' +
                                       srx15 + ',' + srx24 + ',' + srx33 + ',' +
                                       srx44 + ',' + rf15 + ',' + rf24 + ',' +
                                       rf33 + ',' + rf44 + ',' + pwl + ',' +
                                       mag1 + ',' + mag2 + ',' + speed + ',' +
                                       crate + ',' + gyro1 + ',' + gyro2 + ',' +
                                       gyro3 + '\n')
                        elif chsel == "4":
                            fout.write(utc + ',' + lno + ',' + lat + ',' + lon + ',' + height + ',' +
                                       nosats + ',' + ralt + ',' + pkir + ',' + pkbx + ',' +
                                       pkby + ',' + pkbz + ',' + pkvr + ',' + pksx + ',' + pksy + ',' +
                                       pksz + ',' + srz15 + ',' + srz24 + ',' + srz33 + ',' +
                                       srz44 + ',' + brz15 + ',' + brz24 + ',' + brz33 + ',' +
                                       brz44 + ',' + srx15 + ',' + srx24 + ',' + srx33 + ',' +
                                       srx44 + ',' + sry15 + ',' + sry24 + ',' + sry33 + ',' +
                                       sry44 + ',' + rf15 + ',' + rf24 + ',' + rf33 + ',' +
                                       rf44 + ',' + pwl + ',' + mag1 + ',' + mag2 + ',' + speed + ',' +
                                       crate + ',' + gyro1 + ',' + gyro2 + ',' + gyro3 + '\n')

                b += 1

            fout.close()

    print("Total lines read: {}".format(total_lines))
    print(f"{len(header)} headers:")
    for item in header:
        print(item)

    fnameout = path + '\sysinfo.txt'
    fout = open(fnameout, 'w')

    l = '-' * 22

    print('{0}\n System Information :\n{0}\nSample Rate :\t\t{1:>6}\n'
          'No of Channels :\t{2:>6}\nSoftware Version :\t{3:>6}\n'
          'Loop diameter :\t\t{4:>6}\nSystem Type :\t\t{5:>6}\n'
          'Serial No :\t\t{6:>6}\nSystem Gain :\t\t{7:>6}\n'
          'Base Frequency :\t{8:>6}\nDuty Cycle :\t\t{9:>6}\n'
          'Voltage :\t\t{10:>6}\nNo Mags :\t\t{11:>6}\n'
          'Power Monitor :\t\t{12:>6}\n'
          .format(l, SamplR, Chan, Ver, loopd, stype, sn, gain, basef,
                  dc, volt, nomags, pmon))
    fout.write('{0}\n System Information :\n{0:>6}\nSample Rate :\t\t{1:>6}\n'
               'No of Channels :\t{2:>6}\nSoftware Version :\t{3:>6}\n'
               'Loop diameter :\t\t{4:>6}\nSystem Type :\t\t{5:>6}\n'
               'Serial No :\t\t{6:>6}\nSystem Gain :\t\t{7:>6}\n'
               'Base Frequency :\t{8:>6}\nDuty Cycle :\t\t{9:>6}\n'
               'Voltage :\t\t{10:>6}\nNo Mags :\t\t{11:>6}\n'
               'Power Monitor :\t\t{12:>6}\n'
               .format(l, SamplR, Chan, Ver, loopd, stype, sn, gain, basef,
                       dc, volt, nomags, pmon))

    fout.close()

    rem_d = var1.get()
    kst_create = var2.get()
    kml_create = var3.get()

    if kst_create == 1:
        create_kst_xml(path, current_path)

    if kml_create == 1:
        create_kml(path)

    if rem_d == 1:
        for file in files_d:
            # os.remove(path + '\\' + file)
            os.remove(file)
            print("{} deleted".format(file))


def var_states():
    print("d: %d\nkst: %d\nkml: %d" % (var1.get(), var2.get(), var3.get()))


def d_create():
    print("Hello")


def kst_create():
    path = get_file("*.csv")
    path = path[0].rsplit("\\", 1)[0]
    current_path = os.path.realpath(__file__).rsplit("\\", 1)[0]
    create_kst_xml(path, current_path)


def kml_create():
    path = get_file("*.csv")
    path = path[0].rsplit("\\", 1)[0]
    create_kml(path)


Label(master, text="Settings:").grid(row=0, sticky=W)
var1 = IntVar()
Checkbutton(master, text="Remove D Files", variable=var1).grid(row=1, sticky=W)
var2 = IntVar(value=1)
Checkbutton(master, text="Create KST Template", variable=var2).grid(row=2, sticky=W)
var3 = IntVar(value=1)
Checkbutton(master, text="Create KML File", variable=var3).grid(row=3, sticky=W)
Button(master, text='Extract VTEM',
       command=vtem_extract).grid(row=4, sticky=W, pady=4, padx=45)
Button(master, text='Extract BIN',
       command=bin_extract).grid(row=5, sticky=W, pady=4, padx=50)
Button(master, text='Create KST Template',
       command=kst_create).grid(row=6, sticky=W, pady=4, padx=25)
Button(master, text='Create KML',
       command=kml_create).grid(row=7, sticky=W, pady=4, padx=50)
Button(master, text='Quit',
       command=master.quit).grid(row=8, sticky=W, pady=4, padx=70)
mainloop()
