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

        btn1 = Gtk.Button("Add Normal Cert Fingerprint")
        btn1.connect("clicked", self.normal_cert_fingerprint)
        box.add(btn1)

        csr_btn = Gtk.Button("Select key to create CSR")
        csr_btn.connect("clicked", self.csr_func)
        box.add(csr_btn)

    def ca_keycert(self, widget):

        #Getting CA credentials and create ca key/cert

        dialog = CA2(self)
        response = dialog.run()

        cmd1 = 'openssl req \
        -new \
        -newkey rsa:{bit} \
        -days {days} \
        -nodes \
        -x509 \
        -subj "/C={country}/ST={state}/L={city}/O={ou}/CN={cn}" \
        -keyout {cn}.key \
        -out {cn}.crt'.format(bit=ca_vals[0], days=ca_vals[1], country=ca_vals[2], state=ca_vals[3], city=ca_vals[4], ou=ca_vals[5], cn=ca_vals[6])
        execute_it(cmd1)

        #adding ca-keys into schema
        anahtarlar = keys.get_strv("anahtarlar")
        ## read ca-key
        keyname = ca_vals[6] + ".key"
        file = open(keyname,mode='r')
        newkey = file.read()
        file.close()
        anahtarlar.append(newkey)
        keys.set_strv("anahtarlar", anahtarlar)

        #adding ca certification
        cmd = "openssl x509 -noout -fingerprint -sha1 -inform pem -in " + ca_vals[6] + ".crt"
        raw_finger = execute_it(cmd)[17:-1]
        cacertler = keys.get_strv("ca-certler")
        cacertler.append(raw_finger)
        keys.set_strv("ca-certler", cacertler)


        ####????
        '''if response == Gtk.ResponseType.OK:
            print("OK")
            print(response)
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancelled otoca")'''
        ####????


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

    def csr_func(self,widget):
        dialog = Gtk.FileChooserDialog("Select KEY to create csr", self, Gtk.FileChooserAction.OPEN,
        ("Cancel", Gtk.ResponseType.CANCEL, "Ok", Gtk.ResponseType.OK))
        response = dialog.run()
        
        if response == Gtk.ResponseType.OK:
            head, tail = os.path.split(dialog.get_filename())
            csrname = tail[:-4] + ".csr"
            #fullpath = head + "/" + csrname
            cmd2 = 'openssl req \
            -new \
            -subj "/C={country}/ST={state}/L={city}/O={ou}/CN={tail}" \
            -key {key} \
            -out {csrname}'.format(country="tr", state="state", city="city", ou="ou", tail=tail, key=dialog.get_filename(), csrname=csrname)
            execute_it(cmd2)

            file = open(csrname,mode='r')
            newcsr = file.read()
            file.close()

            csrler = keys.get_strv("csrler")
            csrler.append(newcsr)
            keys.set_strv("csrler", csrler)

        elif response == Gtk.ResponseType.CANCEL:
            print("Cancelled cert")
        dialog.destroy()


bit = Gtk.Entry()
days = Gtk.Entry()
country = Gtk.Entry()
state = Gtk.Entry()
city = Gtk.Entry()
ou = Gtk.Entry()
name = Gtk.Entry()

ca_vals=[]
class CA2(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, title="CA Anahtar/Sertifika", transient_for=parent, flags=0)

        self.set_default_size(200, 100)
        self.set_border_width(10)

        # Content area
        area = self.get_content_area()
        ca_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        
        # def create_key(bit, days, country, state, city, ou, cn):
        bitlabel = Gtk.Label("Enter Bit:")
        ca_box.add(bitlabel)
        ca_box.add(bit)

        dayslabel = Gtk.Label("Enter days:")
        ca_box.add(dayslabel)
        ca_box.add(days)

        countrylabel = Gtk.Label("Enter country (XX):")
        ca_box.add(countrylabel)
        ca_box.add(country)

        statelabel = Gtk.Label("Enter state:")
        ca_box.add(statelabel)
        ca_box.add(state)

        citylabel = Gtk.Label("Enter city:")
        ca_box.add(citylabel)
        ca_box.add(city)

        oulabel = Gtk.Label("Enter organizational unit:")
        ca_box.add(oulabel)
        ca_box.add(ou)

        namelabel = Gtk.Label("Enter key/crt name:")
        ca_box.add(namelabel)
        ca_box.add(name)

        okbutton = Gtk.Button("OK")
        okbutton.connect("clicked",self.ca_returns)
        ca_box.add(okbutton)

        area.add(ca_box)
        self.show_all()

        
    def ca_returns(self, widget):
        print("ca_returns func worked")
        ca_vals.append(bit.get_text())
        ca_vals.append(days.get_text())
        ca_vals.append(country.get_text())
        ca_vals.append(state.get_text())
        ca_vals.append(city.get_text())
        ca_vals.append(ou.get_text())
        ca_vals.append(name.get_text())
        Gtk.ResponseType.OK
        self.destroy()
        #return True, ca_vals


win = MainWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()