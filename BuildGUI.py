from Tkinter import *


class BuildGUI(Frame):
    def __init__(self):
        self.fields = 'Answers', 'All submissions', 'Students list', 'Output'
        self.default_values = [r'D:\Documents\App_Camp\AppCamp_for_Dr.Allan\answers',
                               r'D:\Documents\App_Camp\AppCamp_for_Dr.Allan\submissions',
                               r'D:\Documents\App_Camp\AppCamp_for_Dr.Allan\students_list',
                               r'D:\Documents\App_Camp\AppCamp_for_Dr.Allan\output2']
        self.field_values={}

        root = Tk()
        root.title('App Camp Code Analyzer')
        ents = self.makeform(root, self.fields)
        root.bind('<Return>', (lambda event, e=ents: self.fetch(e)))
        b1 = Button(root, text='Show',command=(lambda e=ents: self.fetch(e)))
        b1.pack(side=LEFT, padx=5, pady=5)
        b2 = Button(root, text='Run', command=(lambda e=ents: self.action(root, ents)))
        b2.pack(side=LEFT, padx=5, pady=5)

        root.mainloop()

    def fetch(self, entries):
       for entry in entries:
          field = entry[0]
          text  = entry[1].get()
          print('%s: "%s"' % (field, text))
          self.field_values[field]=text


    def makeform(self, root, fields):
       entries = []
       counter=0
       for field in fields:
          row = Frame(root)
          lab = Label(row, width=35, text=field, anchor='w')
          v = StringVar(row, value=self.default_values[counter])
          ent = Entry(row, width=50, textvariable=v)
          row.pack(side=TOP, fill=X, padx=10, pady=5)
          lab.pack(side=LEFT)
          ent.pack(side=RIGHT, expand=YES, fill=X)
          entries.append((field, ent))
          counter+=1
       return entries

    def action(self, root, ents):
        #get values
        for entry in ents:
          field = entry[0]
          text  = entry[1].get()
          print('%s: "%s"' % (field, text))
          self.field_values[field]=text

        # print 'hhhhhhhh'
        root.quit()
