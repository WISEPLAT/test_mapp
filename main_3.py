#xgettext -L python --output=messages.pot main.py main_3_interface.kv
#xgettext -L python --output=po\en.po main.py main_3_interface.kv
#xgettext -L python --output=po\zh.po main.py main_3_interface.kv
#msgmerge --update --no-fuzzy-matching --backup=off po/en.po messages.pot
#msgmerge --update --no-fuzzy-matching --backup=off po/zh.po messages.pot
#mkdir data\locales\en\LC_MESSAGES
#mkdir data\locales\zh\LC_MESSAGES
#msgfmt -c -o data/locales/en/LC_MESSAGES/langapp.mo po/en.po
#msgfmt -c -o data/locales/zh/LC_MESSAGES/langapp.mo po/zh.po


from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ListProperty
from kivy.uix.floatlayout import FloatLayout

from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import OneLineIconListItem, MDList
from kivymd.uix.tab import MDTabsBase


# https://github.com/tito/kivy-gettext-example
from kivy.lang import Observable
import gettext
from os.path import dirname, join
class Lang(Observable):
    observers = []
    lang = None

    def __init__(self, defaultlang):
        super(Lang, self).__init__()
        self.ugettext = None
        self.lang = defaultlang
        self.switch_lang(self.lang)

    def _(self, text):
        return self.ugettext(text)

    def fbind(self, name, func, args, **kwargs):
        if name == "_":
            self.observers.append((func, args, kwargs))
        else:
            return super(Lang, self).fbind(name, func, *args, **kwargs)

    def funbind(self, name, func, args, **kwargs):
        if name == "_":
            key = (func, args, kwargs)
            if key in self.observers:
                self.observers.remove(key)
        else:
            return super(Lang, self).funbind(name, func, *args, **kwargs)

    def switch_lang(self, lang):
        # get the right locales directory, and instanciate a gettext
        locale_dir = join(dirname(__file__), 'data', 'locales')
        locales = gettext.translation('langapp', locale_dir, languages=[lang])
        self.ugettext = locales.gettext
        self.lang = lang

        # update all the kv rules attached to this text
        for func, largs, kwargs in self.observers:
            func(largs, None, None)
tr = Lang("en")


KV = open('main_3_interface.kv', 'r').read()


class ContentNavigationDrawer(BoxLayout):
    pass


class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()
    text_color = ListProperty((0, 0, 0, 1))


class DrawerList(ThemableBehavior, MDList):
    def set_color_item(self, instance_item):
        """Called when tap on a menu item."""

        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color

class Tab(FloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''


class TestNavigationDrawer(MDApp):
    lang = StringProperty('en')

    def build(self):
        self.lang = "en"
        return Builder.load_string(KV)

    def on_start(self):
        icons_item = {
            "folder": "My files",
            "account-multiple": "Shared with me",
            "star": "Starred",
            "history": "Recent",
            "checkbox-marked": "Shared with me",
            "upload": "Upload",
        }
        for icon_name in icons_item.keys():
            self.root.ids.content_drawer.ids.md_list.add_widget(
                ItemDrawer(icon=icon_name, text=icons_item[icon_name])
            )

    def on_star_click(self):
        print("clicked")
        self.lang = "zh"


    def on_lang(self, instance, lang):
        print('switched')
        tr.switch_lang(lang)


TestNavigationDrawer().run()