# pygnomescast (without sound)
Python librarie To Record Desktop on Gnome Sell

# Requires
python3-dbus(python3) or python-dbus(python2)

pygobject3


# Fedora

sudo dnf install pygobject3 python3-gobject gtk3 python-dbus python3-dbus

# Ubuntu
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0 python-dbus python3-dbus


# Screencast()

file_template: the template for the filename to use  #default "Record-%d-%t" (String)

draw_cursor : Show/Hide Mouse Cursor (true or false) #default "true" (String)

framerate   : the number of frames per second that should be recorded if possible 30  # default "30" (String)

pipeline    : the GStreamer pipeline used to encode recordings   # default "vp8enc min_quantizer=13 max_quantizer=13 cpu-used=5 deadline=1000000 threads=%T ! queue ! webmmux" (String)

Screencast.start() Return:

success: whether the screencast was started successfully (True Or False) (1 or 0)

filename_used: the file where the screencast is being saved (String)

Screencast.stop() Return:

success: whether stopping the recording was successful (True Or False) (1 or 0)



# ScreencastArea()

x: the X coordinate of the area to capture (int)

y: the Y coordinate of the area to capture (int)

width: the width of the area to capture    (int)

height: the height of the area to capture  (int)

file_template: the template for the filename to use  #default "Record-%d-%t" (String)

draw_cursor : Show/Hide Mouse Cursor (true or false) #default "true" (String)

framerate   : the number of frames per second that should be recorded if possible 30 # default "30" (String)

pipeline    : the GStreamer pipeline used to encode recordings   # default "vp8enc min_quantizer=13 max_quantizer=13 cpu-used=5 deadline=1000000 threads=%T ! queue ! webmmux" (String)

ScreencastArea.start() Return:

success: whether the screencast was started successfully (True Or False) (1 or 0) 

filename_used: the file where the screencast is being saved (String)

ScreencastArea.stop() Return:

success: whether stopping the recording was successful (True Or False) (1 or 0)


# For more info

https://gitlab.gnome.org/GNOME/gnome-shell/blob/master/data/org.gnome.Shell.Screencast.xml
