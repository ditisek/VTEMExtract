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
# v1.4 - Port GUI to wx
# v1.5 - Add File rename to gps date functions
# v1.6 - Add laser merge with data
# v1.7 - Sync data to $TD_VZ and not gps to correct data dropped

import os
import csv
import math
import geotech
import wx


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


def vtem_extract(d, kst, kml):
    # file_names = get_file.get_file()
    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
    # dialog = wx.FileDialog(None, 'Open', wildcard=wildcard, style=style)
    dialog = wx.FileDialog(None, 'Open', wildcard='*.d', style=style | wx.FD_MULTIPLE)
    if dialog.ShowModal() == wx.ID_OK:
        # path = dialog.GetPath()
        path = dialog.GetPaths()
    else:
        path = None
    file_names = path
    current_path = os.path.realpath(__file__).rsplit("\\", 1)[0]
    lno = '0'
    ralt = '0'
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

    rem_d = d
    kst_create = kst
    kml_create = kml

    if kst_create == 1:
        print('kst is true')
        file_kst = path + '\\PlotEM.kst'
        geotech.create_kst_xml(file_kst, current_path)

    if kml_create == 1:
        print('kml is true')
        file_csv = path + '\\VTEMExtracted.csv'
        geotech.create_kml(file_csv)

    if rem_d == 1:
        for file in files_d:
            # os.remove(path + '\\' + file)
            os.remove(file)
            print("{} deleted".format(file))


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((291, 507))
        self.SetTitle("Extract by David")

        self.panel_1 = wx.Panel(self, wx.ID_ANY)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        bitmap_Geotech = wx.StaticBitmap(self.panel_1, wx.ID_ANY, wx.Bitmap("C:/Users/David/Google Drive/Programming/Python/GUI Builder/MyGUI/Geotech.bmp", wx.BITMAP_TYPE_ANY))
        sizer_1.Add(bitmap_Geotech, 0, 0, 0)

        static_line_1 = wx.StaticLine(self.panel_1, wx.ID_ANY)
        sizer_1.Add(static_line_1, 0, wx.EXPAND, 0)

        label_vtemextract = wx.StaticText(self.panel_1, wx.ID_ANY, "VTEMExtract")
        label_vtemextract.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        sizer_1.Add(label_vtemextract, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 1)

        static_line_5 = wx.StaticLine(self.panel_1, wx.ID_ANY)
        sizer_1.Add(static_line_5, 0, wx.ALL | wx.EXPAND, 1)

        self.checkbox_removeD = wx.CheckBox(self.panel_1, wx.ID_ANY, "Remove D Files")
        self.checkbox_removeD.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        sizer_1.Add(self.checkbox_removeD, 0, wx.ALL, 2)

        self.checkbox_createKST = wx.CheckBox(self.panel_1, wx.ID_ANY, "Create KST Template")
        self.checkbox_createKST.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.checkbox_createKST.SetValue(1)
        sizer_1.Add(self.checkbox_createKST, 0, wx.ALL, 2)

        self.checkbox_createkml = wx.CheckBox(self.panel_1, wx.ID_ANY, "Create KML files")
        self.checkbox_createkml.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.checkbox_createkml.SetValue(1)
        sizer_1.Add(self.checkbox_createkml, 0, wx.ALL, 2)

        self.button_vtemextract = wx.Button(self.panel_1, wx.ID_ANY, "Extract VTEM data")
        self.button_vtemextract.SetMinSize((140, 25))
        self.button_vtemextract.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        sizer_1.Add(self.button_vtemextract, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)

        self.button_extractbin = wx.Button(self.panel_1, wx.ID_ANY, "Extract BIN file")
        self.button_extractbin.SetMinSize((120, 25))
        self.button_extractbin.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        sizer_1.Add(self.button_extractbin, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)

        self.button_createkst = wx.Button(self.panel_1, wx.ID_ANY, "Create KST template")
        self.button_createkst.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        sizer_1.Add(self.button_createkst, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)

        self.button_createkml = wx.Button(self.panel_1, wx.ID_ANY, "Create KML file")
        self.button_createkml.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        sizer_1.Add(self.button_createkml, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)

        static_line_6 = wx.StaticLine(self.panel_1, wx.ID_ANY)
        sizer_1.Add(static_line_6, 0, wx.EXPAND, 0)

        static_line_3 = wx.StaticLine(self.panel_1, wx.ID_ANY)
        sizer_1.Add(static_line_3, 0, wx.EXPAND, 0)

        label_1 = wx.StaticText(self.panel_1, wx.ID_ANY, "File Rename Tools (due\nto incorrect system time)", style=wx.ALIGN_CENTER_HORIZONTAL)
        label_1.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        sizer_1.Add(label_1, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)

        static_line_7 = wx.StaticLine(self.panel_1, wx.ID_ANY)
        sizer_1.Add(static_line_7, 0, wx.EXPAND, 0)

        static_line_4 = wx.StaticLine(self.panel_1, wx.ID_ANY)
        sizer_1.Add(static_line_4, 0, wx.EXPAND, 0)

        self.button_dfilerename = wx.Button(self.panel_1, wx.ID_ANY, "Rename D Files")
        self.button_dfilerename.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        sizer_1.Add(self.button_dfilerename, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)

        self.button_renamedgps = wx.Button(self.panel_1, wx.ID_ANY, "Rename DGPS")
        self.button_renamedgps.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        sizer_1.Add(self.button_renamedgps, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)

        self.button_renamelalt = wx.Button(self.panel_1, wx.ID_ANY, "Rename LALT")
        self.button_renamelalt.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        sizer_1.Add(self.button_renamelalt, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)

        self.panel_1.SetSizer(sizer_1)

        self.Layout()

        self.Bind(wx.EVT_BUTTON, self.vtem_pressed, self.button_vtemextract)
        self.Bind(wx.EVT_BUTTON, self.bin_pressed, self.button_extractbin)
        self.Bind(wx.EVT_BUTTON, self.kst_pressed, self.button_createkst)
        self.Bind(wx.EVT_BUTTON, self.kml_pressed, self.button_createkml)
        self.Bind(wx.EVT_BUTTON, self.rename_d_pressed, self.button_dfilerename)
        self.Bind(wx.EVT_BUTTON, self.rename_dgps_pressed, self.button_renamedgps)
        self.Bind(wx.EVT_BUTTON, self.rename_lalt_pressed, self.button_renamelalt)
        # end wxGlade

    def vtem_pressed(self, event):  # wxGlade: MyFrame.<event_handler>
        d = self.checkbox_removeD.GetValue()
        kst = self.checkbox_createKST.GetValue()
        kml = self.checkbox_createkml.GetValue()
        vtem_extract(d, kst, kml)
        print("Extract done")
        event.Skip()

    def bin_pressed(self, event):  # wxGlade: MyFrame.<event_handler>
        path = MyFileDialog(None, wildcard='*.bin')
        file = path.EventHandler.Paths
        geotech.bin_extract(file[0])
        print("Bin extraction done!!!")
        event.Skip()

    def kst_pressed(self, event):  # wxGlade: MyFrame.<event_handler>
        path = MyFileDialog(None, wildcard='*.csv')
        file = path.EventHandler.Paths
        current_path = os.path.realpath(__file__).rsplit("\\", 1)[0]
        geotech.create_kst_xml(file[0], current_path)
        print("KST template created")
        event.Skip()

    def kml_pressed(self, event):  # wxGlade: MyFrame.<event_handler>
        path = MyFileDialog(None, wildcard='*.csv')
        file = path.EventHandler.Paths
        # path = path.rsplit("\\", 1)[0]
        geotech.create_kml(file[0])
        print("KML file created")
        event.Skip()

    def rename_d_pressed(self, event):  # wxGlade: MyFrame.<event_handler>
        path = MyFileDialog(None, wildcard='*.d')
        files = path.EventHandler.Paths
        geotech.dfile_rename_gps(files)
        print("D-Files renamed")
        event.Skip()

    def rename_dgps_pressed(self, event):  # wxGlade: MyFrame.<event_handler>
        path = MyFileDialog(None, wildcard='A*.log')
        files = path.EventHandler.Paths
        geotech.gpsfile_rename_gps(files)
        print("GPS files renamed!")
        event.Skip()

    def rename_lalt_pressed(self, event):  # wxGlade: MyFrame.<event_handler>
        print("Not implemented yet!")
        # print(file)
        event.Skip()


# end of class MyFrame
class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True


class MyFileDialog(wx.FileDialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFileDialog.__init__
        # kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
        kwds["style"] = kwds.get("style", 0) | wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE
        wx.FileDialog.__init__(self, *args, **kwds)
        self.SetTitle("dialog")

        self.ShowModal()
# end of class MyFileDialog


# end of class MyApp
if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
