# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import re
import socket
import subprocess

from libqtile import hook, layout, widget, bar
from typing import List  # noqa: F401

from libqtile import bar, layout, widget, extension
from libqtile.config import Click, Drag, Group, Key, Screen, Rule
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
terminal = guess_terminal()

# The autostart for the system
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])

keys = [
    # Switch between windows in current stack pane
    Key([mod], "k", lazy.layout.down(),
        desc="Move focus down in stack pane"),
    Key([mod], "j", lazy.layout.up(),
        desc="Move focus up in stack pane"),

    # Move windows up or down in current stack
    Key([mod, "control"], "k", lazy.layout.shuffle_down(),
        desc="Move window down in current stack "),
    Key([mod, "control"], "j", lazy.layout.shuffle_up(),
        desc="Move window up in current stack "),

    # Switch window focus to other pane(s) of stack
    Key([mod], "space", lazy.layout.next(),
        desc="Switch window focus to other pane(s) of stack"),

    # Swap panes of split stack
    Key([mod, "shift"], "space", lazy.layout.rotate(),
        desc="Swap panes of split stack"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.restart(), desc="Restart qtile"),
    Key([mod, "control"], "w", lazy.shutdown(), desc="Shutdown qtile"),
    Key([mod], "r", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),

    Key([mod], "d", lazy.run_extension(extension.DmenuRun(
                dmenu_prompt="",
                dmenu_font="Ubuntu Bold",
                background="#282a36",
                foreground="#434758",
                selected_background= "#ffb612",
                selected_foreground="#fff",
    ))), 
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    
        ]


# Bar Colors
def init_colors():
     return [["#282a36", "#282a36"],
             ["#434758", "#434758"],
             ["#282a36", "#282a36"],
             ["#282a36", "#282a36"],
             ["#282a36", "#282a36"]]

# Workspaces and names
def init_group_names():
    return [("BASE", {'layout': 'monadtall'}),
            ("WWW",  {'layout': 'monadwide'}),
            ("DEV",  {'layout': 'monadtall'}),
            ("REC",  {'layout': 'max'}),
            ("EDU",  {'layout': 'BoJackOS'}),
            ("SYS",  {'layout': 'max'}),
            ("MUS",  {'layout': 'max'}),
            ("VID",  {'layout': 'max'}),
            ("OPT",  {'layout': 'floating'})]


def init_groups():
    return [Group(name, **kwargs) for name, kwargs in group_names]

if __name__ in ["config", "__main__"]:
    group_names = init_group_names()
    groups = init_groups()

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))            # Switch to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name)))     # Send current window to another group

# Workspace layouts
layouts = [
    layout.MonadWide(margin=5, 
                     max_ratio=0.90, 
                     min_ratio=0.20, 
                     change_size=10, 
                     ),
#    layout.MonadTall(),
    layout.Max(),
#    layout.Stack(num_stacks=2),
    layout.Floating(),
    layout.TreeTab(font = "Ubuntu",
                   fontsize = 12,
                   sections = ["Action Board", "To-Do"],
                   border_width = 3,
                   active_fg = '#ffffff',
                   active_bg = '#ffb612',
                   inactive_bg = '#606060',
                   inactive_fg = '#ababab',
                   panel_width = 110,
                   name = 'BoJackOS',
                  ),
    # Try more layouts by unleashing below layouts.
    # layout.Bsp(),
    # layout.Columns(),
    # layout.Matrix(),
    layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

### Mouse Callbacks ####

def open_dmenu(qtile):
    qtile.cmd_spawn('dmenu_run')


colors = [["#000000", "#000000"], # panel background
          ["#434758", "#000000"], # background for current screen tab
          ["#dddddd", "#dddddd"], # font color for group names
          ["#ffb612", "#ffb612"], # border line color for current tab
          ["#000000", "#434758"], # border line color for other tab and odd widgets
          ["#101820", "#101820"], # color for the even widgets
          ["#e1acff", "#e1acff"]] # window name

prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(
    font="Ubuntu Bold",
    fontsize = 12,
    padding = 6,
    background=colors[2]
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [   
                widget.Image(
                             filename = "~/Downloads/start2.png",
                             foreground = colors[3],
                             background = colors[3],
                             mouse_callbacks = {'Button1': open_dmenu},
                            ),
                widget.Sep(linewidth = 12, foreground = colors[5], background = colors[0]),
               #  widget.GroupBox(font = "sans", fontsize = 12, borderwidth = 1, padding_y = 5, padding_x = 5, foreground = '#ffb612', background = '#101820',),
                widget.GroupBox(
                       font = "Ubuntu Bold",
                       fontsize = 12,
                       margin_y = 3,
                       margin_x = 0,
                       padding_y = 5,
                       padding_x = 3,
                       borderwidth = 3,
                       active = colors[2],
                       inactive = colors[2],
                       rounded = False,
                       highlight_color = colors[1],
                       highlight_method = "line",
                       this_current_screen_border = colors[3],
                       this_screen_border = colors [4],
                       other_current_screen_border = colors[0],
                       other_screen_border = colors[0],
                       foreground = colors[4],
                       background = colors[0]
                       ),

                widget.Prompt(foreground = colors[2], background = colors[3]),
                widget.Sep(linewidth = 1, foreground = colors[3], background = colors[3]),
                widget.WindowName(foreground = colors[2], background = colors[0]),
                widget.Chord(
                    chords_colors={
                        'launch': ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                # widget.TextBox("default config", name="default"),
                # widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
                widget.Systray(foreground = colors[0], background = colors[0]),
                # widget.Net(interface="eno0"),
                widget.Sep(linewidth = 1, foreground = colors[3], background = colors[3]),
                # widget.KhalCalendar(background = '#101820',),
                widget.Clock(format='%a %I:%M %p  %m-%d-%Y', foreground = colors[2], background = colors[0]),
                widget.Sep(linewidth = 1, foreground = colors[3], background = colors[3]),
                widget.CheckUpdates(foreground = colors[2], background = colors[0]),
                widget.CurrentLayout(foreground = colors[2], background = colors[0]),
                widget.QuickExit(default_text = '[ Exit ]', countdown_start = 1, background = colors[4]),
            ],
            24,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
# wmname = "LG3D"
