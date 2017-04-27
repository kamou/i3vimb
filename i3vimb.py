#!/bin/python
import i3ipc

class vimbWS(object):
    def __init__(self):
        self.i3 = i3ipc.Connection()
        self.i3.on("window::new", self.new_window)
        self.i3.on("window::close", self.close_window)
        self.i3.on("binding::symbol", self.killed)
        self.searchbar_loaded = False
        self.num_tabs = 0
        self.i3.command("workspace browser")
        self.firsttab_set_split = False

        leaves = self.i3.get_tree().leaves()
        for l in leaves:
            if l.window_instance == "vimb_searchbar":
                exit(0)

    def run(self):
        self.i3.command("exec vimb http://startpage.com/ --name=vimb_searchbar")
        self.i3.main()

    def killed(self, i3, e):
        print e
        print dir(e)

    def new_window(self, i3, e):
        if e.container.window_instance == "vimb_searchbar":
            e.container.command("mark searchbar")

        if e.container.window_instance == "vimb":
            if self.num_tabs == 0:
                e.container.command("move to mark searchbar")
                e.container.command("move window to right")
                e.container.command("move window to right")
                e.container.command("mark first_tab")
                e.container.command("splitv")

                e.container.command('[con_mark="searchbar"]resize shrink right')
                e.container.command('[con_mark="searchbar"]resize shrink right')
                e.container.command('[con_mark="searchbar"]resize shrink right')
            elif self.num_tabs == 1:
                e.container.command("move window to mark first_tab")
                i3.command('[con_mark="first_tab"] focus')
                i3.command('[con_mark="first_tab"] layout tabbed')
                # e.container.command("layout tabbed")
            else:
                e.container.command("move to mark first_tab")
            e.container.command("focus")

            self.num_tabs += 1

    def close_window(self, i3, e):
        if e.container.window_instance == "vimb_searchbar" and self.num_tabs:
            i3.command("exec vimb http://startpage.com/ --name=vimb_searchbar")
        elif e.container.window_instance == "vimb_searchbar":
            exit(0)
        if e.container.window_instance == "vimb":
            self.num_tabs -= 1



vimb = vimbWS()
vimb.run()
