#!/usr/bin/env python3
"""
Clearine
Yet Another GTK3-based logout-window overlay for independent windowmanager

usage:

   -h  --help  show help docs

 configuration file location:

   Clearine basically read configuration from  "~/.config/clearine.conf"  .
   if that file is unavailable, I will read from  "/etc/clearine.conf"  insteads.

"""

import os
import sys
import time
import getopt
import signal
import logging
import subprocess
import configparser

try:
    import gi

except:
    print("no modules named 'gi', please install python-gobject")
    sys.exit()

try:
    import cairo

except:
    print("no modules named 'cairo', please install python-cairo")
    sys.exit()

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk, Gdk, Pango, GLib
from gi.repository.GdkPixbuf import Pixbuf
from Clearine.helper import SignalHandler
from Clearine.helper import Helper

config = {}
shortcuts = {}
root_module = os.path.dirname(os.path.abspath(__file__))
class Clearine(Gtk.Window):
    def __init__(self):
        super(Clearine, self).__init__()
        # initialize a fullscreen window
        self.setcontent()
        self.setprops()

    def setprops(self):
        self.set_visual(self.get_screen().get_rgba_visual())
        self.set_app_paintable(True)

        self.fullscreen()
        self.set_skip_pager_hint(True)
        self.set_keep_above(True)
        self.realize()

        self.connect('destroy', Gtk.main_quit)
        self.connect('draw', self.draw_background)
        self.connect('delete-event', Gtk.main_quit)
        self.connect('key-press-event', self.on_keypressed)
        self.connect('window-state-event', self.on_state_changed)

    def setcontent(self):
        # fetch a plain-text clearine.conf configuration
        global config
        global shortcuts

        status = logging.getLogger(self.__class__.__name__)
        dotcat = configparser.ConfigParser()

        file_home = "%s/.config/clearine.conf" % os.environ['HOME']
        file_etc = "/etc/clearine.conf"
        file_share = "/usr/share/clearine/clearine.conf"
        file_dot_config = "%s/.config/clearine/clearine.conf" % os.environ['HOME']
        file_default = "%s/data/clearine.conf" % root_module

        try:
            if os.path.exists(file_home):
                status.info("load config from: %s"% (file_home))
                dotcat.read(file_home)
            elif os.path.exists(file_dot_config):
                status.info("load config from: %s"% (file_dot_config))
                dotcat.read(file_dot_config)
            elif os.path.exists(file_etc):
                status.info("load config from: %s"% (file_etc))
                dotcat.read(file_etc)
            elif os.path.exists(file_share):
                status.info("load config from: %s"% (file_share))
                dotcat.read(file_share)
            elif os.path.exists(file_default):
                status.info("load config from: %s"% (file_default))
                dotcat.read(file_default)
        except:
            status.error("failed to find configuration file.  exiting.")
            sys.exit()

        def find_key(data, section, key, default):
            helper = Helper()
            try:
                if data is "arr":
                    return dotcat.get(section, key).split(",")
                if data is "str":
                    return dotcat.get(section, key, raw=True)
                if data is "int":
                    return dotcat.getint(section, key)
                if data is "flo":
                    return dotcat.getfloat(section, key)
                if data is "clr":
                    data = dotcat.get(section, key, raw=True)
                    if data.startswith("#") or data.startswith("rgba("):
                        return data
                    elif data.startswith("{") and data.endswith("}"):
                        data = data.lstrip('{').rstrip('}')
                        return helper.xrdb(data)

            except:
                status.info("failed to find key named '%s' in section '[%s]'.  use fallback value insteads." % (key, section))
                return default

        config["button-label-font"]        = find_key("str", "button", "label-font",        "DejaVu Sans Book")
        config["button-label-size"]        = find_key("int", "button", "label-size",        9)
        config["button-label-color"]       = find_key("clr", "button", "label-color",       "#101314")
        config["button-height"]            = find_key("int", "button", "height",            70)
        config["button-icon-height"]       = find_key("int", "button", "icon-height",       32)
        config["button-icon-width"]        = find_key("int", "button", "icon-width",        32)
        config["button-items"]             = find_key("arr", "button", "items",             "suspend, logout, lock, hibernate, restart, shutdown, cancel")
        config["button-margin-bottom"]     = find_key("int", "button", "margin-bottom",     30)
        config["button-margin-left"]       = find_key("int", "button", "margin-left",       10)
        config["button-margin-right"]      = find_key("int", "button", "margin-right",      10)
        config["button-margin-top"]        = find_key("int", "button", "margin-top",        30)
        config["button-spacing"]           = find_key("int", "button", "spacing",           10)
        config["button-theme"]             = find_key("str", "button", "theme",             "Clearine-Fallback")
        config["button-width"]             = find_key("int", "button", "width",             100)
        config["button-opacity-normal"]    = find_key("flo", "button", "opacity-normal",    0.7)
        config["button-opacity-focus"]     = find_key("flo", "button", "opacity-focus",     1.0)
        config["card-background-color"]    = find_key("clr", "card",   "background-color",  "#e1e5e8")
        config["card-border-radius"]       = find_key("int", "card",   "border-radius",     20)
        config["card-padding-bottom"]      = find_key("int", "card",   "padding-bottom",    10)
        config["card-padding-left"]        = find_key("int", "card",   "padding-left",      10)
        config["card-padding-right"]       = find_key("int", "card",   "padding-right",     10)
        config["card-padding-top"]         = find_key("int", "card",   "padding-top",       10)
        config["main-mode"]                = find_key("str", "main",   "mode",              "V")
        config["main-spacing"]             = find_key("int", "main",   "spacing",           10)
        config["main-gap-left"]            = find_key("int", "main",   "gap-left",          50)
        config["main-gap-right"]           = find_key("int", "main",   "gap-right",         50)
        config["main-gap-top"]             = find_key("int", "main",   "gap-top",           50)
        config["main-gap-bottom"]          = find_key("int", "main",   "gap-bottom",        50)
        config["main-opacity"]             = find_key("flo", "main",   "opacity",           0.8)
        config["widget-firstline-font"]    = find_key("str", "widget", "firstline-font",    "DejaVu Sans ExtraLight")
        config["widget-firstline-size"]    = find_key("int", "widget", "firstline-size",    90)
        config["widget-firstline-color"]   = find_key("clr", "widget", "firstline-color",   "#e1e5e8")
        config["widget-firstline-format"]  = find_key("str", "widget", "firstline-format",  "%H.%M")
        config["widget-secondline-font"]   = find_key("str", "widget", "secondline-font",   "DejaVu Sans Book")
        config["widget-secondline-size"]   = find_key("int", "widget", "secondline-size",    14)
        config["widget-secondline-color"]  = find_key("clr", "widget", "secondline-color",  "#e1e5e8")
        config["widget-secondline-format"] = find_key("str", "widget", "secondline-format", "%A, %d %B %Y")
        config["command-logout"]           = find_key("str", "command", "logout",           "pkexec pkill X")
        config["command-restart"]          = find_key("str", "command", "restart",          "pkexec reboot -h now")
        config["command-shutdown"]         = find_key("str", "command", "shutdown",         "pkexec shutdown -h now")
        config["command-lock"]             = find_key("str", "command", "lock",             "i3lock")
        config["command-suspend"]          = find_key("str", "command", "suspend",          "systemctl suspend")
        config["command-hibernate"]        = find_key("str", "command", "hibernate",          "systemctl hibernate")

        shortcuts = {
            find_key("str", "shortcuts", "cancel", "Escape"):   "cancel",
            find_key("str", "shortcuts", "lock", "K"):          "lock",
            find_key("str", "shortcuts", "suspend", "P"):       "suspend",
            find_key("str", "shortcuts", "hibernate", "H"):     "hibernate",
            find_key("str", "shortcuts", "logout", "L"):        "logout",
            find_key("str", "shortcuts", "restart", "R"):       "restart",
            find_key("str", "shortcuts", "shutdown", "S"):      "shutdown"
        }

        # Setup all content inside Gtk.Window
        if config["main-mode"] == "horizontal":
            button_group = Gtk.VBox()
            content = Gtk.HBox()
        else:
            button_group = Gtk.HBox()
            content = Gtk.VBox()

        button_group.set_margin_top(config["button-margin-top"])
        button_group.set_margin_start(config["button-margin-left"])
        button_group.set_margin_bottom(config["button-margin-bottom"])
        button_group.set_margin_end(config["button-margin-right"])
        button_group.set_spacing(config["button-spacing"])

        card_container = Gtk.Box()
        card_container.set_margin_top(config["card-padding-top"])
        card_container.set_margin_start(config["card-padding-left"])
        card_container.set_margin_bottom(config["card-padding-bottom"])
        card_container.set_margin_end(config["card-padding-right"])
        card_container.pack_start(button_group, False, False, False)

        card = Gtk.Box()
        card.pack_start(card_container, False, False, False)

        container = Gtk.Grid()
        if config["main-mode"] == "horizontal":
            container.set_halign(Gtk.Align.END)
            container.set_valign(Gtk.Align.CENTER)
        else:
            container.set_halign(Gtk.Align.CENTER)
            container.set_valign(Gtk.Align.START)

        container.attach(card, 1, 1, 1, 1)

        self.first_widget = Gtk.Label()
        self.first_widget.set_label(time.strftime(config["widget-firstline-format"]))

        self.second_widget = Gtk.Label()
        self.second_widget.set_label(time.strftime(config["widget-secondline-format"]))

        widgets = Gtk.Grid()
        if config["main-mode"] == "horizontal":
            widgets.set_halign(Gtk.Align.START)
            widgets.set_valign(Gtk.Align.CENTER)
        else:
            widgets.set_halign(Gtk.Align.CENTER)
            widgets.set_valign(Gtk.Align.END)

        widgets.attach(self.first_widget, 1, 1, 1, 1)
        widgets.attach(self.second_widget, 1, 2, 1, 1)

        content.set_margin_start(config["main-gap-left"])
        content.set_margin_end(config["main-gap-right"])
        content.set_margin_top(config["main-gap-top"])
        content.set_margin_bottom(config["main-gap-bottom"])
        content.set_spacing(config["main-spacing"])
        content.pack_start(widgets, True, True, 0)
        content.pack_end(container, True, True, 0)

        GLib.timeout_add(200, self.update_widgets)
        self.card_style = Gtk.CssProvider()
        self.card_css = """
            .clearine-button {{
                background: {_cbg};
                color: {_bcol};
                font-family: '{_bfont}';
                font-size: {_bsize}px;
                box-shadow: none;
                opacity: {_bopa};
                border-width: 0;
            }}
            .clearine-button:focus {{
                opacity: {_bopaf};
                border-width: 0;
            }}
            .clearine-card {{
                background: {_cbg};
                border-width: 0;
                border-radius:{_crad}px;
            }}
            .clearine-widget-first {{
                color: {_w1col};
                font-family:'{_w1font}';
                font-size: {_w1size}px;
            }}
            .clearine-widget-second {{
                color: {_w2col};
                font-family:'{_w2font}';
                font-size: {_w2size}px;
            }}
            """.format(
                _bsize=str(config["button-label-size"]),
                _bcol=str(config["button-label-color"]),
                _bfont=str(config["button-label-font"]),
                _bopa=str(config["button-opacity-normal"]),
                _bopaf=str(config["button-opacity-focus"]),
                _cbg=str(config["card-background-color"]),
                _crad=str(config["card-border-radius"]),
                _w1col=str(config["widget-firstline-color"]),
                _w2col=str(config["widget-secondline-color"]),
                _w1font=str(config["widget-firstline-font"]),
                _w2font=str(config["widget-secondline-font"]),
                _w1size=str(config["widget-firstline-size"]),
                _w2size=str(config["widget-secondline-size"]),
            )

        self.card_style.load_from_data(self.card_css.encode())

        Gtk.StyleContext.add_class(card.get_style_context(), "clearine-card")
        Gtk.StyleContext.add_class(self.first_widget.get_style_context(), "clearine-widget-first")
        Gtk.StyleContext.add_class(self.second_widget.get_style_context(), "clearine-widget-second")

        Gtk.StyleContext.add_provider(card.get_style_context(), self.card_style, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        Gtk.StyleContext.add_provider(self.first_widget.get_style_context(), self.card_style, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        Gtk.StyleContext.add_provider(self.second_widget.get_style_context(), self.card_style, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        for button in config["button-items"]:
            try:
                count += 1
            except NameError:
                count = 1

            self.draw_button(button, button_group, count)

        body = Gtk.EventBox()
        body.add(content)
        body.connect('button-press-event', Gtk.main_quit)
        self.add(body)

    def update_widgets(self):
        # update first and second-line widget
        self.first_widget.set_label(time.strftime(config["widget-firstline-format"]))
        self.second_widget.set_label(time.strftime(config["widget-secondline-format"]))

    def draw_button(self, name, widget, index):
        # setup a buttons inside card
        status = logging.getLogger(self.__class__.__name__)
        button_name = name.strip()

        dir_ic_home = "%s/.themes/%s/clearine" % (os.environ['HOME'], config["button-theme"])
        dir_ic_share = "%s/%s/clearine" % ("%s/share/themes" % sys.prefix, config["button-theme"])
        dir_ic_share_fb = "%s/%s/clearine" % ("%s/share/themes" % sys.prefix, 'Clearine-Fallback')
        dir_ic_default = "%s/data" % root_module
        print(dir_ic_share)

        ic_png_home = "%s/%s.png" % (dir_ic_home, button_name)
        ic_png_share = "%s/%s.png" % (dir_ic_share, button_name)
        ic_svg_home = "%s/%s.svg" % (dir_ic_home, button_name)
        ic_svg_share = "%s/%s.svg" % (dir_ic_share, button_name)
        ic_svg_share_fb = "%s/%s.svg" % (dir_ic_share_fb, button_name)
        ic_svg_default = "%s/%s.svg" % (dir_ic_default, button_name)

        if os.path.exists(ic_png_home):
            iconfile = ic_png_home
        elif os.path.exists(ic_svg_home):
            iconfile = ic_svg_home
        elif os.path.exists(ic_png_share):
            iconfile = ic_png_share
        elif os.path.exists(ic_svg_share):
            iconfile = ic_svg_share
        elif os.path.exists(ic_svg_share_fb):
            iconfile = ic_svg_share_fb
        elif os.path.exists(ic_svg_default):
            iconfile = ic_svg_default
        else:
            status.info("No Clearine theme available, exiting")
            sys.exit()

        icon_buffer = Pixbuf.new_from_file_at_size(iconfile, config["button-icon-width"], config["button-icon-height"])

        icon = Gtk.Image()
        icon.set_from_pixbuf(icon_buffer)
        icon.set_margin_bottom(10)
        icon.set_margin_top(10)

        button = Gtk.Button()
        button.set_always_show_image(True)
        button.set_image_position(2)
        button.set_label(button_name.capitalize())
        button.set_image(icon)
        button.connect("clicked", self.do, button_name)
        button.set_size_request(config["button-width"], config["button-height"])
        button.set_can_focus(True)

        Gtk.StyleContext.add_class(button.get_style_context(), "clearine-button")
        Gtk.StyleContext.add_provider(button.get_style_context(), self.card_style, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        widget.pack_start(button, False, False, False)


    def draw_background(self, widget, context):
        # setup a semi-transparent background
        context.set_source_rgba(0, 0, 0, config["main-opacity"])
        context.set_operator(cairo.OPERATOR_SOURCE)
        context.paint()
        context.set_operator(cairo.OPERATOR_OVER)

    def do(self, widget, button):
        # handle every button action
        if button == 'cancel':
            sys.exit()
        else:
            os.system(config["command-%s" % button])

    def on_keypressed (self, widget, event):
        # handling an event when user press some key
        key = Gdk.keyval_name(event.keyval)

        if key in shortcuts.keys():
            command = shortcuts[key]
            if command == "cancel":
                sys.exit()
            else:
                os.system(config["command-%s" % command])

    def on_state_changed(self, widget, event):
         if event.new_window_state:
            self.fullscreen()

def main():
    status_format = logging.StreamHandler(sys.stdout)
    status_format.setFormatter(logging.Formatter("Clearine: %(message)s"))
    status = logging.getLogger()
    status.addHandler(status_format)
    status.setLevel(logging.INFO)

    try:
        if len(sys.argv) > 1:
            options, arguments = getopt.getopt(sys.argv[1:], "h", ["help"])
            for option, argument in options:
                if option in ("-h", "--help"):
                    print (__doc__)
                    return 0
    except:
        status.error("unused options '%s'.  see -h (or --help) for more information" % sys.argv[1])
        return 2

    handle = SignalHandler()
    signal.signal(signal.SIGINT, handle.SIGINT)
    w = Clearine()
    w.show_all()
    Gtk.main()

if __name__ == "__main__":
    sys.exit(main())

