import screenlets
from screenlets.options import StringOption, IntOption
from urllib import urlopen, urlencode
import cairo
import pango
import gtk
import logging
import gobject

class TelusBalanceScreenlet (screenlets.Screenlet):
    """Telus Balance Screenlet"""

    # default meta-info for Screenlets
    __name__    = 'TelusBalance'
    __version__ = '0.1'
    __author__  = 'Tim Voet'
    __desc__    = 'A screenlet to check the balance of pay as you go Telus users.'

    __timeout = None
    username = None
    password = None
    update_interval = None

    def __init__ (self, **keyword_args):
        screenlets.Screenlet.__init__(self, width=300, height=150,
            uses_theme=True, **keyword_args)
        # set theme
        self.theme_name = "thingrey"
        # add option group
        self.add_options_group('Account', 'This is settings for Account Information ')
        # add editable option
        self.add_option(StringOption('Account', # group name
            'username',                      # attribute-name
            self.username,                       # default-value
            'Username',                      # widget-label
            'This is your Username' # description
            ))        # add editable option
        self.add_option(StringOption('Account', # group name
            'password',                      # attribute-name
            self.password,                       # default-value
            'Password',                      # widget-label
            'This is your Password', # description
            password=True
            ))
        self.add_option(IntOption('Account',
            'update_interval',
            self.update_interval,
            'Update interval ( in hours )',
            'The amount of time between checks.',
            min=0, max=23
            ))
    def on_init (self):
        pass

        # attribute-"setter", handles setting of attributes
    def __setattr__(self, name, value):
        # call Screenlet.__setattr__ in baseclass (ESSENTIAL!!!!)
        screenlets.Screenlet.__setattr__(self, name, value)
        # check for this Screenlet's attributes, we are interested in:
        if name == "update_interval":
            if value > 0:
                self.__dict__['update_interval'] = value
                if self.__timeout:
                    gobject.source_remove(self.__timeout)
                self.__timeout = gobject.timeout_add(int(value * 60 * 60 * 1000), self.update)
            else:
                # TODO: raise exception!!!
                self.__dict__['update_interval'] = 1
                pass
        elif name =="account":
            if len(value) > 0:
                self.__dict__['account'] = value
                self.account_usage = AccountUsage(value)
                self.update()
            else:
                pass

    def on_draw (self, ctx):
         pass
    def on_draw_shape (self, ctx):
        self.on_draw(ctx)
