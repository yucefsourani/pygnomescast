#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  pygnomescast.py
#  
#  Copyright 2018 youcef sourani <youssef.m.sourani@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import dbus
import time
import subprocess
import gi
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk



def gnome_shell_version():
    try:
        bus         = dbus.SessionBus()
        obj         = bus.get_object("org.gnome.Shell","/org/gnome/Shell")
        intf        = dbus.Interface(obj,"org.freedesktop.DBus.Properties")
        return intf.Get("org.gnome.Shell","ShellVersion")
    except :
        return False
        
        
        
def is_gnome_shell():
    if gnome_shell_version():
        return True
    return False



def get_audio_source():
    all_    = subprocess.Popen("""pactl list | grep -A2 'Source #' | grep 'Name: ' | cut -d" " -f2""",stdout=subprocess.PIPE,shell=True).communicate()[0].decode("utf-8").strip().split("\n")
    return all_



def get_audio_source_monitor():
    monitor =  subprocess.Popen("""pactl list | grep -A2 'Source #' | grep 'Name: .*\.monitor$' | cut -d" " -f2""",stdout=subprocess.PIPE,shell=True).communicate()[0].decode("utf-8").strip().split("\n")
    return monitor



class MonitorInfo(object):
    def __init__(self,monitor):
        self.monitor   = monitor
        self.x         = self.monitor.get_geometry().x
        self.y         = self.monitor.get_geometry().y
        self.width     = self.monitor.get_geometry().width
        self.height    = self.monitor.get_geometry().height
        self.info      = {"monitor":self.monitor,"x":self.x,"y":self.y,"width":self.width,"height":self.height}
        
        
        
class ScreenInfo(object):
    def __init__(self,screen):
        self.screen    = screen
        self.width     = self.screen.get_width()
        self.height    = self.screen.get_height()
        self.info      = {"screen":self.screen,"width":self.width,"height":self.height}
        
        
        
class MonitorScreenInfo(object):
    display         = Gdk.Display().get_default()
    
    @staticmethod
    def get_default_display():
        return MonitorScreenInfo.display
    
    @staticmethod
    def get_screens_number():
        return MonitorScreenInfo.display.get_n_screens()
        
    @staticmethod
    def get_screens():
        display       = MonitorScreenInfo.display
        screen_number = display.get_n_screens()
        return [ScreenInfo(display.get_screen(screennumber)) for screennumber in range(screen_number) ]
        
    @staticmethod
    def get_monitors_number():
        return MonitorScreenInfo.display.get_n_monitors()
        
    @staticmethod
    def get_monitors():
        display        = MonitorScreenInfo.display
        monitor_number = display.get_n_monitors()
        return [MonitorInfo(display.get_monitor(monitornumber)) for monitornumber in range(monitor_number) ]
        


class Screencast(object):
    def __init__(self,file_template="Record-%d-%t",draw_cursor="true",\
                framerate="30",\
                pipeline="vp8enc min_quantizer=13 max_quantizer=13 cpu-used=5 deadline=1000000 threads=%T ! queue ! webmmux"):
                    
        self.bus           = dbus.SessionBus()
        self.__obj         = self.bus.get_object("org.gnome.Shell.Screencast","/org/gnome/Shell/Screencast")
        self.__intf        = dbus.Interface(self.__obj,"org.gnome.Shell.Screencast")
        
        self.file_template = file_template
        self.draw_cursor   = draw_cursor
        self.framerate     = framerate
        self.pipeline      = pipeline
        
    def start(self):
        return self.__intf.Screencast(self.file_template,\
                                     {"draw-cursor":self.draw_cursor,"framerate":self.framerate,"pipeline":self.pipeline})
        
    def stop(self):
        return self.__intf.StopScreencast()
        
        
        
class ScreencastArea(object):
    def __init__(self,x,y,width,height,file_template="Record-%d-%t",\
                 draw_cursor="true",framerate="30",\
                 pipeline="vp8enc min_quantizer=13 max_quantizer=13 cpu-used=5 deadline=1000000 threads=%T ! queue ! webmmux"):
        self.bus           = dbus.SessionBus()
        self.__obj         = self.bus.get_object("org.gnome.Shell.Screencast","/org/gnome/Shell/Screencast")
        self.__intf        = dbus.Interface(self.__obj,"org.gnome.Shell.Screencast")
        
        self.x             = x
        self.y             = y
        self.width         = width
        self.height        = height
        self.file_template = file_template
        self.draw_cursor   = draw_cursor
        self.framerate     = framerate
        self.pipeline      = pipeline
        
    def start(self):
        return self.__intf.ScreencastArea(self.x,self.y,self.width,self.height,\
                                      self.file_template,\
                                      {"draw-cursor":self.draw_cursor,"framerate":self.framerate,"pipeline":self.pipeline})
        
    def stop(self):
        return self.__intf.StopScreencast()
        
        
if __name__ == "__main__":
    
    #Get Gnome Shell Version
    print(gnome_shell_version())
    print("\n")
    
    
    # Check If is Gnome Shell
    print(is_gnome_shell())
    print("\n")
    
    
    
    # Get Audio Source
    print(get_audio_source())
    print(get_audio_source_monitor())
    print("\n")
    
    
    # Get Default Display
    print(MonitorScreenInfo.get_default_display())
    print("\n")
    
    
    
    # Get Screens Info
    print(MonitorScreenInfo.get_screens_number())      # Get Number Off Screens
    print(MonitorScreenInfo.get_screens())             # Get All Screen
    print(MonitorScreenInfo.get_screens()[0].width)    # Get width For First Screen
    print(MonitorScreenInfo.get_screens()[0].height)   # Get height For First Screen

    print(MonitorScreenInfo.get_screens()[0].info)   # Get All Info
    for key,value in MonitorScreenInfo.get_screens()[0].info.items(): # Get All Info
        print("{} : {}".format(key,value))
    print("\n")
    

    # Get Monitors Info
    print(MonitorScreenInfo.get_monitors_number())      # Get Number Off Monitors
    print(MonitorScreenInfo.get_monitors())             # Get All Monitors
    print(MonitorScreenInfo.get_monitors()[0].width)    # Get width For First Monitors
    print(MonitorScreenInfo.get_monitors()[0].height)   # Get height For First Monitors
    print(MonitorScreenInfo.get_monitors()[0].x)        # Get x For First Monitors
    print(MonitorScreenInfo.get_monitors()[0].y)        # Get y For First Monitors

    print(MonitorScreenInfo.get_monitors()[0].info)   # Get All Info
    for key,value in MonitorScreenInfo.get_monitors()[0].info.items(): # Get All Info
        print("{} : {}".format(key,value))
    print("\n")
    


    # Example Screencast
    #screencast = Screencast(file_template="/home/youcef/Record-%d-%t.webm",draw_cursor="true",framerate="30",\
     #           pipeline="vp8enc min_quantizer=13 max_quantizer=13 cpu-used=5 deadline=1000000 threads=%T ! queue ! webmmux")
    
    # ملاحظة إذا حددنا فقط الإسم ولم نحدد المسار في file_template
    #سيتم الحفظ في مجلد الفيديو في مجلد المنزل الخاص بالمستخدم إن لم يكن مجلد الفيديو موجود سيتم الحفظ في مجلد المنزل
    # ملاحظة اخرى إن وجدو سيتم تلقائيا تحديد تاريخ ووقت بدأ التسجيل بدل %d %t
    screencast = Screencast(file_template="Record-%d-%t.webm",draw_cursor="true",framerate="30",\
                pipeline="vp8enc min_quantizer=13 max_quantizer=13 cpu-used=5 deadline=1000000 threads=%T ! queue ! webmmux")
    
    print( screencast.start() )
    time.sleep(5)
    print( screencast.stop() )
    print("\n")
    
    
    
    # Example ScreencastArea
    #x = MonitorScreenInfo.get_monitors()[0].x
    x = MonitorScreenInfo.get_monitors()[0].x + 10
    
    #y = MonitorScreenInfo.get_monitors()[0].y
    y = MonitorScreenInfo.get_monitors()[0].y + 22
    
    #width = MonitorScreenInfo.get_monitors()[0].width
    width = MonitorScreenInfo.get_monitors()[0].width / 2
    
    #height = MonitorScreenInfo.get_monitors()[0].height
    height = MonitorScreenInfo.get_monitors()[0].height / 2

    #screencastarea = ScreencastArea(x,y,width,height,file_template="/home/youcef/Record-%d-%t.webm",draw_cursor="true",framerate="30",\
                #pipeline="vp8enc min_quantizer=13 max_quantizer=13 cpu-used=5 deadline=1000000 threads=%T ! queue ! webmmux")
    
    screencastarea = ScreencastArea(x,y,width,height,file_template="Record-%d-%t.webm",draw_cursor="true",framerate="30",\
                pipeline="vp8enc min_quantizer=13 max_quantizer=13 cpu-used=5 deadline=1000000 threads=%T ! queue ! webmmux") 
    
    print( screencastarea.start() )
    time.sleep(5)
    print( screencastarea.stop() )
    
