import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gio, Gtk
import os.path
import subprocess

G_ID = "apps.gsettings-ornekuygulama"
G_PATH = "/apps/gsettings-ornekuygulama/"
F_PATH = "/usr/share/glib-2.0/schemas/" + G_ID + ".gschema.xml"
keys = Gio.Settings.new(G_ID)

if not os.path.isfile(F_PATH): 
    print("GSettings Miço XML is not found!")
    exit


def execute_it(cmd):
    output = subprocess.check_output(['bash','-c', cmd])
    return output.decode("utf-8")


class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Miço")
        self.set_default_size(200, 100)
        self.set_border_width(30)
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(box)

        ca_btn = Gtk.Button("Create CA key/crt")
        ca_btn.connect("clicked", self.ca_keycert)
        box.add(ca_btn)

        btn1 = Gtk.Button("Add Normal Cert")
        btn1.connect("clicked", self.normal_cert_fingerprint)
        box.add(btn1)

    def ca_keycert(self, widget):
        dialog = CA2(self)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            print("OK")
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancelled otoca")

        dialog.destroy()

    #optional: select_folder
    def normal_cert_fingerprint(self, widget):
        dialog = Gtk.FileChooserDialog("Select the certificate", self, Gtk.FileChooserAction.OPEN,
        ("Cancel", Gtk.ResponseType.CANCEL, "Ok", Gtk.ResponseType.OK))
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            # print("Secilen anahtar " + dialog.get_filename())
            cmd = "openssl x509 -noout -fingerprint -sha1 -inform pem -in " + dialog.get_filename()
            raw_finger = execute_it(cmd)[17:-1]
            normalcertler = keys.get_strv("normalcertler")
            normalcertler.append(raw_finger)
            keys.set_strv("normalcertler", normalcertler)
            print(normalcertler)

        elif response == Gtk.ResponseType.CANCEL:
            print("Cancelled cert")
        dialog.destroy()

class CA2(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, title="CA Anahtar/Sertifika", transient_for=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )

        self.set_default_size(200, 100)
        self.set_border_width(10)

        # Content area
        area = self.get_content_area()
        ca_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        
        # def create_key(bit, days, country, state, city, ou, cn):
        bitlabel = Gtk.Label("Enter Bit:")
        bit = Gtk.Entry()
        ca_box.add(bitlabel)
        ca_box.add(bit)

        dayslabel = Gtk.Label("Enter days:")
        days = Gtk.Entry()
        ca_box.add(dayslabel)
        ca_box.add(days)

        countrylabel = Gtk.Label("Enter country (XX):")
        country = Gtk.Entry()
        ca_box.add(countrylabel)
        ca_box.add(country)

        statelabel = Gtk.Label("Enter state:")
        state = Gtk.Entry()
        ca_box.add(statelabel)
        ca_box.add(state)

        citylabel = Gtk.Label("Enter city:")
        city = Gtk.Entry()
        ca_box.add(citylabel)
        ca_box.add(city)

        oulabel = Gtk.Label("Enter organizational unit:")
        ou = Gtk.Entry()
        ca_box.add(oulabel)
        ca_box.add(ou)

        namelabel = Gtk.Label("Enter key/crt name:")
        name = Gtk.Entry()
        ca_box.add(namelabel)
        ca_box.add(name)

        okbutton = Gtk.Button("OK")
        okbutton.connect("clicked", self.ca_returns)
        ca_box.add(okbutton)


        area.add(ca_box)
        self.add(bit)
        self.show_all()

        
    def ca_returns(self, widget):
        print("ca_returns func worked")
        Gtk.ResponseType.OK
        self.destroy()
        return True


win = MainWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
