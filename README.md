# Clearine

Beautiful Logout UI for X11 window manager.
Inspired from oblogout and Android Oreo's power menu.

## Preview

* [Horizontal mode](https://user-images.githubusercontent.com/9277632/47901195-29e2bd00-de77-11e8-8ffc-0d422161bea4.png)
* [Vertical mode](https://user-images.githubusercontent.com/9277632/47901203-2ea77100-de77-11e8-8b85-321c7b2e8bfd.png)

## Dependencies

- python (version 3)
- python-gobject
- python-cairo


## Installation

For Arch user, you can install it via AUR insteads:

    $ yaourt -S clearine-git

For Void user :

    $ sudo xbps-install -S clearine

---
## Install from source

Install the dependencies first:

    $ sudo pacman -S python-cairo python-gobject # Arch Linux

clone this repo into your local storage:

    $ git clone https://github.com/yuune/clearine.git
    $ cd clearine

then install via pip:

    $ pip install .

if you not using pip, you can run setup.py directly:

    $ python3 setup.py install --prefix=/usr --root="/" --optimize=1



## Configuration file

Clearine basically read configuration from  "~/.config/clearine.conf"  .
if that file is unavailable, clearine will read from  "/etc/clearine.conf" or "/usr/share/clearine/clearine.conf" insteads.


## Configuration format

The configuration format is using section-style like this :
```
[main]
    # set background opacity
    opacity = 0.8
    # set gaps
    gap-left = 70
    gap-right = 70
    gap-top = 70
    gap-bottom = 70
    # set mode (vertical/horizontal)
    mode = horizontal
    # set spacing between card and widget
    spacing = 20

[command]
    # set command to launch when the button is clicked
    logout = openbox --exit
    restart = systemctl reboot
    shutdown = systemctl poweroff

[card]
    # set background color and border radius for card
    background-color = #e1e5e8
    border-radius = 5
    # set padding
    padding-bottom = 10
    padding-left = 10
    padding-right = 10
    padding-top = 10

[button]
    # button theme name
    theme = Clearine-Fallback
    # button item sort
    items = logout, restart, shutdown, cancel
    # set button text font and text color
    label-font = DejaVu Sans Book 9
    label-size = 9
    label-color = #101314
    # set button width and height
    width = 70
    height = 70
    # set button icon width and height
    icon-width = 32
    icon-height = 32
    # set per-button margin
    margin-bottom = 0
    margin-left = 0
    margin-right = 0
    margin-top = 0
    # set spacing between button
    spacing = 0
    # opacity
    opacity-normal = 0.7
    opacity-focus = 1.0

[widget]
    # set widget first line font, size, color and format
    firstline-font = DejaVu Sans ExtraLight
    firstline-size = 90
    firstline-color = #e1e5e8
    firstline-format = %H.%M
    # set widget second line font, size, color and format
    secondline-font = DejaVu Sans Book
    secondline-size = 14
    secondline-color = #e1e5e8
    secondline-format = %A, %d %B %Y
```

For the color, you can use hex format like this :
```
[card]
    background-color = #e1e5e8
```
or you can get color from your X resources, by using format like this:
```
[card]
    background-color = {background}

[widget]
    firstline-color = {color6}
```

## Themes

You can use the png or svg for the icon button.

See `/usr/share/themes/Clearine-Fallback` for example


## Credits

* [Google Material Design Icon Family](https://google.github.io/material-design-icons/)
* [@fikriomar26](https://github.com/fikriomar16)

## License

The code is available under the [MIT license](LICENSE).
