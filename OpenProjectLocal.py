import tkinter as tk
from tkinter import filedialog, messagebox
import os, os.path
import subprocess
import requests
import webbrowser

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

        self.checkForDockerDaemon()

    def create_widgets(self):
        self.winfo_toplevel().title("Local OpenProject.org")

        self.baseframe = tk.Frame(width=500, height=500, bg="")
        self.baseframe.pack(fill=tk.BOTH)

        self.logoframe = tk.Frame(self.baseframe, height=200)
        self.logoframe.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.logo = tk.Label(self.logoframe, text="Launch OpenProject.org")
        self.logo.pack(side="top")

        self.statusframe = tk.Frame(self.baseframe)
        self.statusframe.pack(side=tk.TOP, expand=1)

        self.statuslabel = tk.Label(self.statusframe, text="Service status")
        self.statuslabel.grid(row=0, column=0, columnspan=2)
        self.dockerstatus = tk.Frame(self.statusframe, width=35, height=35, bg="red")
        self.dockerstatus.grid(row=1, column=0)
        self.containerstatus = tk.Frame(self.statusframe, width=35, height=35, bg="red")
        self.containerstatus.grid(row=2, column=0)

        self.dockerstatuslabel = tk.Label(self.statusframe, text="Docker")
        self.dockerstatuslabel.grid(row=1, column=1, sticky=tk.W)
        self.containerstatuslabel = tk.Label(self.statusframe, text="OpenProject")
        self.containerstatuslabel.grid(row=2, column=1, sticky=tk.W)

        self.footerframe = tk.Frame(self.baseframe)
        self.footerframe.pack(side="bottom", fill=tk.X, expand=1)

        self.footertext = tk.Label(self.footerframe, text="With ♥ from Datahives Opensource")
        self.footertext.pack()

        self.buttonframe = tk.Frame(self.baseframe)
        self.buttonframe.pack(side="bottom", fill=tk.X, expand=1)

        self.startbutton = tk.Button(
            self.buttonframe, text="Start OpenProject.org", command=self.start_openproject, height=3)
        self.startbutton.pack(side="top", fill=tk.X)
        self.quitbutton = tk.Button(
            self.buttonframe, text="Quit", fg="red", command=self.stop_openproject, height=1)
        self.quitbutton.pack(side="bottom", fill=tk.X)

    def start_openproject(self):
        foldername = filedialog.askdirectory()

        datapath = os.path.join(foldername, "pgdata")
        logpath = os.path.join(foldername, "logs")
        staticpath = os.path.join(foldername, "static")
        # if(not os.path.isdir(datapath)):
        #     os.makedirs(datapath)
        # if(not os.path.isdir(logpath)):
        #     os.makedirs(logpath)
        # if(not os.path.isdir(staticpath)):
        #     os.makedirs(staticpath)

        # start docker 
        runcommand = "docker run -d --rm -p 8080:80 --name openproject -e SECRET_KEY_BASE=secret -v "+datapath+":/var/lib/postgresql/9.6/main -v "+logpath+":/var/log/supervisor -v "+staticpath+":/var/db/openproject openproject/community:8"
        print(runcommand)

        subprocess.run(runcommand, shell=True)

        url = "http://localhost:8080"
        isReady = False
        while not isReady:
            try:
                response = requests.get(url)
                if int(response.status_code) == 200:
                    isReady = True
            except:
                isReady = False

        self.containerstatus["bg"] = "green"

        # launch webbrowser
        webbrowser.open_new_tab(url)

    def stop_openproject(self):
        # stop container
        try:
            runcommand = "docker stop openproject"
            subprocess.run(runcommand, shell=True, check=True)
        except:
            None

        self.master.destroy()

    def checkForDockerDaemon(self, *args):

        # isReady = False
        try:
            status = subprocess.run(
                'docker ps', shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            isReady = True
        except:
            self.status = None
            isReady = False
        if isReady:
            self.dockerstatus["bg"] = "green"
        else:
            self.dockerstatus["bg"] = "red"
            messagebox.showerror("Docker not running", "Docker daemon is not running. Please relaunch the program after Docker is ready.")



root = tk.Tk()
root.geometry("300x250")
app = Application(master=root)
app.mainloop()



