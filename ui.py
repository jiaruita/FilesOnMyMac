from Tkinter import *
import file_obj
class App(object):
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()

        self.btn_scan = Button(frame, text="SCAN",  command=self.scan_all)
        self.btn_scan.pack(side=LEFT)

        self.btn_next = Button(frame, text="NEXT", command=self.next_page)
        self.btn_next.pack()

        self.btn_prev = Button(frame, text="PREV", command=self.prev_page)
        self.btn_preb.pack()

    def scan_all(self):
        print "scan all"
        #file_obj.heapify_dir()
        


    def next_page(self):
        print "next page"

    def prev_page(self):
        print "prev page"

    
