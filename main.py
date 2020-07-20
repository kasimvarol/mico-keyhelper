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
    '''li = list(cmd.split(" ")) 
    subprocess.run(li)'''
    output = subprocess.check_output(['bash','-c', cmd])
    return output.decode("utf-8")

class App(object):
    def __init__(self):
        

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        btn1 = Gtk.Button("Choose File")
        btn1.connect("clicked", self.on_file_clicked)
        box.add(btn1)


        window = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
        window.set_title('Miço')
        window.set_border_width(64)
        window.connect("delete-event", Gtk.main_quit)
        window.add(box)
        window.show_all()
        Gtk.main()

    #optional: select_folder
    def on_file_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Select the certificate", None, Gtk.FileChooserAction.OPEN,
        ("Cancel", Gtk.ResponseType.CANCEL, "Ok", Gtk.ResponseType.OK))
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            # print("Secilen anahtar " + dialog.get_filename())
            cmd = "openssl x509 -noout -fingerprint -sha1 -inform pem -in " + dialog.get_filename()
            raw_finger = execute_it(cmd)[17:-1]

            normalcertler = keys.get_strv("normalcertler")
            normalcertler.append(raw_finger)
            keys.set_strv(str(normalcertler))
            print(normalcertler)

        elif response == Gtk.ResponseType.CANCEL:
            print("Cancelled")
        dialog.destroy()
    
if __name__ == "__main__":
    app = App()



