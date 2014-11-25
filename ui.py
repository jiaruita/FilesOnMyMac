from Tkinter import *
import file_obj
import os
class App(object):
    def __init__(self, master):
        self.master = master
        self.PAGE_SIZE = 10
        self.counter = 0
        frame = Frame(master)
        frame.pack()
        
        self.btn_scan = Button(frame, text="SCAN",  command=self.scan_all)
        self.btn_scan.grid(row=0,column=0,sticky=W)

        self.btn_next = Button(frame, text="NEXT", command=self.next_page)
        self.btn_next.grid(row=0,column=1,sticky=W)

        self.btn_prev = Button(frame, text="PREV", command=self.prev_page)
        self.btn_prev.grid(row=0,column=2,sticky=W)

        self.list = Listbox(frame, width=100, heigh=30)
        self.list.grid(row=1,column=0,columnspan=3,sticky=W)

        self.btn_copy = Button(frame, text="COPY PATH", command=self.copy_path)
        self.btn_copy.grid(row=2,column=0,sticky=W)

        self.btn_show_in_finder = Button(frame, text="SHOW IN FINDER", command = self.show_in_finder)
        self.btn_show_in_finder.grid(row=2,column=1,sticky=W)

    def scan_all(self):
        print "scan all"
        self.heap = file_obj.heapify_dir('/')
        self.sorted_list = []
        self.next_page()
        


    def next_page(self, page_size=None):
        print "next page"
        if page_size is None:
            page_size = self.PAGE_SIZE
        if self.counter < len(self.sorted_list):
            next_items = self.sorted_list[self.counter:self.counter+page_size]
        else:
            next_items = file_obj.get_one_page(self.heap, page_size)
            if len(next_items) == 0:
                return
            self.sorted_list.extend(next_items)
        self.counter = self.counter + page_size
        self.list.delete(0,END)
        for item in next_items:
            self.list.insert(END, item)

    def prev_page(self, page_size=None):
        print "prev page"
        if page_size is None:
            page_size = self.PAGE_SIZE
        self.counter = self.counter - page_size
        if self.counter <= 0:
            self.counter = self.counter + page_size
            return
        else:
            self.counter = self.counter - page_size
        prev_items = self.sorted_list[self.counter:self.counter + page_size]
        self.list.delete(0,END)
        for item in prev_items:
            self.list.insert(END, item)
        self.counter = self.counter + page_size

    def copy_path(self):
        content = self.list.get(self.list.curselection())
        print content
        left = content.find('/')
        right = content.find('Size:')
        result = content[left:right].strip()
        print result
        self.master.clipboard_clear()
        self.master.clipboard_append(result)

    def show_in_finder(self):
        content = self.list.get(self.list.curselection())
        left = content.find('/')
        right = content.find('Size:')
        right = content.rfind('/')
        result = content[left:right].strip()
        os.system('open "%s"' %(result))

root = Tk()
root.geometry("800x600+0+0")
app = App(root)
root.mainloop()
