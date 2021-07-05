from sqlite3.dbapi2 import connect
from tkinter import *
from tkinter import messagebox
from ttkbootstrap import *
import time
import random
import pygame
import webbrowser
from PIL import Image, ImageTk
from tkinter import filedialog
from mutagen.mp3 import MP3
import back


class body:

    pygame.mixer.init()

    global bondo
    global stopped
    stopped = False
    bondo = False

    def __init__(self, root) -> None:
        self.root = root
        self.gana = None
        self.root.title("GSauce's music Player")
        self.s = Style()
        self.s.theme_use('cyborg')
        self.s.configure('TButton', font='Helvetica 18')

        self.root.resizable(width=False, height=False)

        menu = Menu(self.root)
        self.file = Menu(menu)
        self.file.add_command(label='Add Songs  A', command=self.add_songs)
        self.file.add_command(label='Open recent   O', command=self.openrecent)
        self.file.add_command(label='Save   Ctrl+S',
                              command=self.save_playlist)
        self.file.add_separator()
        self.file.add_command(label='Show Favourites F',command=self.play_favs)
        self.file.add_separator()
        self.file.add_command(label='Exit', command=self.root.quit)
        menu.add_cascade(label='File', menu=self.file)
        self.edit = Menu(menu)
        self.edit.add_command(label='Help', command=self.helpy)
        menu.add_cascade(label='Help', menu=self.edit)
        self.root.config(menu=menu)

        self.frame = Frame(self.root, bg='black', width=600, pady=5, height=30)
        self.frame.grid(row=0, column=0, columnspan=2)

        img = Image.open("raju.jpg")
        img = img.resize((200, 240), Image.ANTIALIAS)
        img1 = ImageTk.PhotoImage(img)

        ll = Label(self.root, image=img1)
        ll.image = img1
        ll.grid(row=1, column=1, rowspan=13)

     # ------------------random color generator---------------------------------

     # --------------------------binding keys-------------------------
        self.root.bind("<a>", lambda x: self.add_songs())
        self.root.bind("<space>", lambda a: self.pause(bondo))
        self.root.bind("<s>", lambda x: self.stop())
        self.root.bind("<o>", lambda x: self.openrecent())
        self.root.bind("<p>", lambda x: self.play())
        self.root.bind("<f>", lambda x: self.play_favs())
        self.root.bind("<Right>", lambda x: self.nextsong())
        self.root.bind("<Left>", lambda x: self.previous())
     # --------------------------binding keys-------------------------

        
        self.frame2 = Frame(self.root, width=100)
        self.frame2.grid(row=17, column=0, columnspan=2)

        # self.pbar=ttk.Progressbar(self.root,orient='horizontal',length=580,value=0)
        # self.pbar.grid(row=16,columnspan=2,column=0)

        self.slide = ttk.Scale(self.root, from_=0, to=100, orient=HORIZONTAL,
                               value=0, length=580, command=self.seek)
        self.slide.grid(row=16, column=0, columnspan=2)

    # display playlist on the screen
        self.display = Listbox(self.root, width=30, height=15, bg='black', borderwidth=0, highlightthickness=0,
                               fg='violet', selectbackground='purple')
        self.display.grid(row=1, column=0, rowspan=15)

        self.display.bind('<<ListboxSelect>>', self.favcheck)
    # this will show th song length
        self.slen = Label(self.root, text='', fg='#d608ff')
        self.slen.grid(row=15, column=1)

        # all necessary buttons
        self.fav = ttk.Button(self.root, text='\u2764', style='info.TButton', width=7,
                              command=self.favo)  # \ufe0f
        self.fav.grid(row=14, column=1)
        back = ttk.Button(self.frame2, text='\u23EE', style='info.TButton',
                          width=7, command=self.previous)
        back.grid(row=0, column=0, pady=1, padx=2)
        fwr = ttk.Button(self.frame2, text='\u23ED',
                         style='info.TButton', width=7, command=self.nextsong)
        fwr.grid(row=0, column=4, pady=1, padx=2)
        play = ttk.Button(self.frame2, text='\u23F5',
                          style='info.TButton', width=7, command=self.play)
        play.grid(row=0, column=2, pady=1, padx=2)
        pause = ttk.Button(self.frame2, text='\u23F8',
                           style='info.TButton', width=7, command=lambda: self.pause(bondo))
        pause.grid(row=0, column=3, pady=1, padx=2)
        stop = ttk.Button(self.frame2, text='\u23F9',
                          style='info.TButton', width=7, command=self.stop)
        stop.grid(row=0, column=1, pady=1, padx=2)
    # checking if a song is fav

    def favcheck(self, e):
        i=self.display.curselection()[0]
        if back.find(sid=i+1)[0][3]:

            self.fav.config(style='danger.TButton')
        else:
            self.fav.config(style='info.TButton')
        pass
    
    def play_favs(self):
        self.display.delete(0,'end')
        for s in back.playfavs():
            self.display.insert(END, s[1])

    
    # select favourite song button function
    def favo(self):
        gaan = self.display.get(ACTIVE)

        if back.find(gaan)[0][3]:

            back.fav(gaan, 0)

            self.fav.config(style='info.TButton')
        else:

            back.fav(gaan, 1)
            self.fav.config(style='danger.TButton')

    def save_playlist(self):
        # to save the playlist in a local database
        for s in self.song:
            a = s
            a = a.replace('D:/EntertainmenT/songs/', '')
            a = a.replace('.mp3', '')
            back.insert(a, s)
        
        messagebox.showinfo('GSauce','yo MARIO, playlist saved!!!')

    def openrecent(self):
        self.display.delete(0,'end')
        for s in back.show():
            self.display.insert(END, s[1])
        

    def seek(self, x):
        # gaan=self.display.get(ACTIVE)
        # pygame.mixer.music.load(self.gana)
        # pygame.mixer.music.play(loops=0,start=int(self.slide.get()))

        pass

    def helpy(self):
        webbrowser.open('help.txt')
        # open help.txt in Notepad

    def add_songs(self):
        # adding songs to the listbox screen
        self.song = filedialog.askopenfilenames(initialdir='D:/EntertainmenT/songs/',
                                                title='Add songs', filetypes=(("mp3 files", "*.mp3"),))
        for s in self.song:

            s = s.replace('D:/EntertainmenT/songs/', '')
            s = s.replace('.mp3', '')
            self.display.insert(END, s)

    def play(self):
        # play function is triggered when play button is pushed
        if self.display.curselection() == ():
            messagebox.showerror(
                "Music Plyer", "Please select a song first!\n Areeh gaan ta k select korbe?")
        else:
            gaan = self.display.get(ACTIVE)
            self.gaanbaja(gaan)
            # self.showtime()

    def gaanbaja(self, gaan):
        if back.find(gaan)[0][3]:

            self.fav.config(style='danger.TButton')
        else:
            self.fav.config(style='info.TButton')

        self.gana = f'D:/EntertainmenT/songs/{gaan}.mp3'
        pygame.mixer.music.load(self.gana)
        pygame.mixer.music.play(loops=0)
        self.update_pbar()

    def pause(self, le):
        # to pause and resume the song

        global bondo
        bondo = le
        if bondo:
            pygame.mixer.music.unpause()
            bondo = False
        else:
            pygame.mixer.music.pause()
            bondo = True

    def nextsong(self):
        nxt = self.display.curselection()
        nxt = nxt[0]+1
        gaan = self.display.get(nxt)
        self.gaanbaja(gaan)
        self.display.selection_clear(0, END)
        self.display.activate(nxt)
        self.display.selection_set(nxt, last=None)

    def previous(self):
        nxt = self.display.curselection()
        nxt = nxt[0]-1
        gaan = self.display.get(nxt)
        self.gaanbaja(gaan)

        self.display.selection_clear(0, END)
        self.display.activate(nxt)
        self.display.selection_set(nxt, last=None)

    def stop(self):
        pygame.mixer.music.stop()
        self.display.select_clear(ACTIVE)
        global stopped
        stopped = True

    # updating the progress bar

    def update_pbar(self):
        hexa = ['0', '1', '2', '3', '4', '5', '6', '7',
                '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
        global bondo
        global stopped
        ct = pygame.mixer.music.get_pos()/1000
        loadsong = MP3(self.gana)
        song_length = loadsong.info.length
        # v=int(((ct+1)/song_length)*100)
        if bondo == False:
            r = random.choice(hexa)
            g = random.choice(hexa)
            b = random.choice(hexa)
            result = r+g+b
            self.frame.config(bg='#'+result)

        if stopped:
            self.slide.config(value=0)
            self.frame.config(bg='black')
            stopped = False
            pass
        elif int(ct) < int(song_length):

            self.slide.config(to=int(song_length), value=int(ct))
        #     self.pbar['value']=v
        #     self.root.update_idletasks()
            t = time.strftime('%M:%S', time.gmtime(song_length))
            el = time.strftime('%M:%S', time.gmtime(ct))
            self.slen.config(text=el + ' | '+t)

            self.slide.after(1000, self.update_pbar)
        # self.pbar['value']=v+1


if __name__ == "__main__":
    win = Tk()
    body(win)
    win.mainloop()
