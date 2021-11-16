import os 
import sys
from tkinter import *
from tkinter import filedialog, font 
from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter import simpledialog
from PyDictionary import PyDictionary
from tkfontchooser import askfont
from googletrans import Translator
from tkinter.ttk import *

translator=Translator()
dictionary=PyDictionary()

class TextEditor:
    def __init__(self,master=None,**kwargs):
        self.window=master #tạo cửa sổ Tk
        self.window.title("Untitled-Text editor program")
        self.file = None #đường dẫn của file
        self.window_width = kwargs["width"] #độ rộng cửa sổ
        self.window_height = kwargs["height"] #chiều dài cửa sổ
        screen_width = self.window.winfo_screenwidth() #lay thong tin chieu rong man hin
        screen_height = self.window.winfo_screenheight() #lay thong tin chieu dai man hinh
    
        x = int((screen_width / 2) - (self.window_width / 2)) #tạo căn chỉnh toạ độ x
        y = int((screen_height / 2) - (self.window_height / 2)) #tạo căn chỉnh toạn độ y

        #dat vi tri cho cua so, dài x rộng, cách vị trí (0, 0) x và y
        self.window.geometry("{}x{}+{}+{}".format(self.window_width, self.window_height, x, y))

        #dat ten font mac dinh
        self.font_name = StringVar(self.window)
        self.font_name.set("Arial")

        #dat co chu mac dinh
        self.font_size = StringVar(self.window)
        self.font_size.set("25")

        #tao vung soạn thao trong cua so hien tai, font mac dinh
        self.text_area = Text(self.window, font=(self.font_name.get(), self.font_size.get()),undo=True)

        #tạo 2 thanh cuon
        self.VerticalScroll_bar = Scrollbar(self.window)
        self.HorizontalScroll_bar=Scrollbar(self.window,orient=HORIZONTAL)
        #cai thuoc tinh cho 2 thanh cuon
        self.VerticalScroll_bar.grid(row=0,column=1,sticky=N+S)  #đặt thanh cuộn dọc vào côt 1 (bên phải màn hình)
        self.HorizontalScroll_bar.grid(row=1,column=0,sticky=E+W) #đặt thanh cuộn ngang vào dòng 1 (bên dưới màn hình)
        self.window.grid_rowconfigure(0, weight=1) #tao bố cục grid cho window
        self.window.grid_columnconfigure(0, weight=1)
        self.text_area.grid(row=0,column=0,sticky=N + E + S + W)
        self.text_area.config(yscrollcommand=self.VerticalScroll_bar.set,xscrollcommand=self.HorizontalScroll_bar.set,wrap="none")
        self.VerticalScroll_bar.config(command=self.text_area.yview) #cập nhật thanh cuộn
        self.HorizontalScroll_bar.config(command=self.text_area.xview) #cập nhật thanh cuộn

        #tao menu
        self.menu_bar = Menu(self.window)
        self.window.config(menu=self.menu_bar)

        #tao menu file
        self.file_menu = Menu(self.menu_bar, tearoff=0) #tearoff = 0 để xoá dòng gạch chân đầu tiên
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New   ", command=self.new_file,accelerator="Ctrl+N") #thêm nhãn new, chạy hàm new_file (ở bên dưới), phím tắt ctrl + n
        self.file_menu.add_command(label="Open   ", command=self.open_file,accelerator="Ctrl+O")
        self.file_menu.add_command(label="Save   ", command=self.save_file,accelerator="Ctrl+S")
        self.file_menu.add_command(label="Save As...   ", command=self.saveAs_file)
        self.file_menu.add_separator() #thêm gạch ngăn cách
        self.file_menu.add_command(label="Exit   ", command=self.on_closing)

        #tạo menu edit
        self.edit_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Cut   ", command=self.cut, accelerator="Ctrl+X")
        self.edit_menu.add_command(label="Copy   ", command=self.copy, accelerator="Ctrl+C")
        self.edit_menu.add_command(label="Paste   ", command=self.paste, accelerator="Ctrl+V")
        self.edit_menu.add_command(label="Delete   ",command=self.delete)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Undo   ",command=self.text_area.edit_undo,accelerator="Ctrl+Z")
        self.edit_menu.add_command(label="Redo   ",command=self.text_area.edit_redo,accelerator="Ctrl+Y")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Find",command=self.find,accelerator="Ctrl+F")
        self.edit_menu.add_command(label="Replace",command=self.openFindReplaceDialog,accelerator="Ctrl+R")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Font",command=self.change_font)

        #tạo menu help
        self.help_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About   ", command=self.about,accelerator="Ctrl+H")

        #tạo menu chuột phải
        self.mouse = Menu(self.menu_bar, tearoff = 0)
        self.mouse.add_command(label ="Cut   ",command=self.cut,accelerator="Ctrl+X")
        self.mouse.add_command(label ="Copy   ",command=self.copy,accelerator="Ctrl+C")
        self.mouse.add_command(label ="Paste   ",command=self.paste,accelerator="Ctrl+V")
        self.mouse.add_command(label ="Delete   ",command=self.delete)
        self.mouse.add_separator()
        self.mouse.add_command(label="Undo   ",command=self.text_area.edit_undo,accelerator="Ctrl+Z")
        self.mouse.add_command(label="Redo   ",command=self.text_area.edit_redo,accelerator="Ctrl+Y")
        self.mouse.add_separator()
        self.mouse.add_command(label="Dictionary(English)",command=self.getMeaning)
        self.mouse.add_command(label="Translate to Vietnamese",command=self.TranslateToVietNam)
        self.mouse.add_command(label="Translate to English",command=self.TranslateToEnglish)

        #gán lệnh
        self.text_area.bind("<Control-c>",lambda event:self.copy)
        self.text_area.bind("<Control-v>",lambda event:self.paste)
        self.text_area.bind("<Control-x>",lambda event:self.cut)  
        self.text_area.bind("<Control-z>",lambda event:self.text_area.edit_undo)
        self.text_area.bind("<Control-y>",lambda event:self.text_area.edit_redo)
        self.text_area.bind("<Button-3>",self.do_popup)
        self.text_area.bind("<Button-1>",lambda event: self.text_area.tag_remove("found",1.0,END))
        self.text_area.bind("<Key>",lambda event: self.text_area.tag_remove("found",1.0,END))
        self.window.bind("<Control-s>",self.save_file)
        self.window.bind("<Control-n>",self.new_file)
        self.window.bind("<Control-o>",self.open_file)
        self.window.bind("<Control-h>",self.about)
        self.window.bind("<Control-f>",self.find)
        self.window.bind("<Control-r>",self.openFindReplaceDialog)

       #giao thức đóng
        self.window.protocol("WM_DELETE_WINDOW",self.on_closing)


    
    def change_font(self):
        chooseFont=askfont(self.window) #mở cửa sổ cài đặt font
        if chooseFont=="":
            return
        else:
            resultFont=font.Font(family=chooseFont["family"], #tên
                                    size=chooseFont["size"], #cỡ
                                        weight=chooseFont["weight"], #đậm
                                            slant=chooseFont["slant"], #xiên
                                                underline=chooseFont["underline"], #gạch chân
                                                    overstrike=chooseFont["overstrike"]) #gán font
            self.text_area.configure(font=resultFont) #gán giá trị của resultfont cho text_area
            return
        

    def new_file(self,event=None):
        self.window.title("Untitled-Text editor program") #đặt tên file
        self.text_area.delete(1.0, END) #xoá hết nội dung trong text_area
        self.file=None #reset lại đường dẫn của file


    def open_file(self,event=None):
        self.file = askopenfilename(defaultextension=".txt", #kiểu file mặc định là .txt
                                file=[("All Files", "*.*"),
                                        ("Text Documents", "*.txt")]) #gọi cửa sổ mở file

        if self.file == "": #trống thì không mở file nào
            self.file=None
            return

        else:
            try:
                self.window.title(os.path.basename(self.file)) #lấy tên file
                self.text_area.delete(1.0, END) #xoá text area hiện tại
                file = open(self.file, "r",encoding="utf-8") #mở file
                self.text_area.insert(1.0, file.read()) #cop nội dung vào text area
                file.close()
            except Exception: #nếu có lỗi thì thoát hàm
                pass

    def save_file(self,event=None):
        if self.file==None: #nếu file hiện tại chưa có địa chỉ
            self.file = filedialog.asksaveasfilename(initialfile='unititled.txt',
                                                    defaultextension=".txt",
                                                        filetypes=[("All Files", "*.*"),
                                                        ("Text Documents", "*.txt")])  #mở cửa sổ lưu file

            if self.file == "": #vẫn không có địa chỉ thì đóng cửa sổ này
                self.file=None #reset lại đường dẫn của file
                return

            else:
                try:
                    self.window.title(os.path.basename(self.file)) #lấy tên file
                    file = open(self.file, "w",encoding="utf-8") #mở file hiện tại
                    file.write(self.text_area.get(1.0, END).rstrip()) #cop tất cả dữ liệu trên text_area vào file này
                    file.close()
                except Exception:
                    pass
        else:
            file = open(self.file, "w",encoding="utf-8") #mở file với chế độ ghi
            file.write(self.text_area.get(1.0, END).rstrip()) #cop tất cả dữ liệu trên text_area vào file này
            file.close() #đóng file
    
    def saveAs_file(self, event = None):
        self.file = filedialog.asksaveasfilename(initialfile='unititled.txt',
                                                defaultextension=".txt",
                                                    filetypes=[("All Files", "*.*"),
                                                    ("Text Documents", "*.txt")]) #mở cửa sổ save as

        if self.file == "": #không lấy được đường dẫn thì đóng cửa sổ
            self.file=None #reset lại đường dẫn của file
            return

        else:
            try:
                self.window.title(os.path.basename(self.file)) #lấy tên
                file = open(self.file, "w",encoding="utf-8") #mở file hiện tại
                file.write(self.text_area.get(1.0, END).rstrip()) #mở file
                file.close() #đóng nó
            except Exception:
                pass
    
    #hàm tra từ điển tiếng anh
    def getMeaning(self,event=None):
        try:
            result=dictionary.meaning(self.text_area.selection_get()) #lấy nghĩa của từ
            string="" #tạo chuỗi kết quả trống
            for word in result.keys():
                string+=word+" : "+"\n- ".join(list(result[word])) #nối thêm các nghĩa của từ
                string+="\n"
            showinfo(title=self.text_area.selection_get(), message=string) #in ra chuỗi chứa nghĩa của từ
        except:
            showinfo(title=self.text_area.selection_get(), message="Retry") #in ra thông báo lỗi nếu không tìm thấy
    
    #hàm dịch tiếng anh sang tiếng việt
    def TranslateToVietNam(self,event=None):
        translated=translator.translate(self.text_area.selection_get(),src='en',dest='vi') #dịch phần được chọn sang tiếng việt
        if(translated.text==self.text_area.selection_get()+"." or translated.text==self.text_area.selection_get() ): #từ tiếng việt or không có nghĩa thì không dịch
            showinfo(title=self.text_area.selection_get(), message="Retry")
        elif(translated.text==self.text_area.selection_get().title()+"." or translated.text==self.text_area.selection_get().title()):
            showinfo(title=self.text_area.selection_get(), message="Retry")
        else:
            showinfo(title=self.text_area.selection_get(), message=translated.text) #hiện cửa sổ thông báo nghĩa

    #hàm dịch tiếng viêt sang tiếng anh
    def TranslateToEnglish(self,event=None):
        translated=translator.translate(self.text_area.selection_get(),src='vi',dest='en')
        if(translated.text==self.text_area.selection_get()+"." or translated.text==self.text_area.selection_get()):
            showinfo(title=self.text_area.selection_get(), message="Retry")
        elif(translated.text==self.text_area.selection_get().title()+"." or translated.text==self.text_area.selection_get().title()):
            showinfo(title=self.text_area.selection_get(), message="Retry")
        else:
            showinfo(title=self.text_area.selection_get(), message=translated.text)


    def cut(self):
        self.text_area.event_generate("<<Cut>>") #tạo sự kiện cut

    def copy(self):
        self.text_area.event_generate("<<Copy>>") #tạo sự kiện coppy

    def paste(self):
        self.text_area.event_generate("<<Paste>>") #tạo sự kiện paste

    def delete(self):
        try:
            self.text_area.delete("sel.first","sel.last") #xoá phần được chọn
        except:
            pass
    
    #hàm tìm kiếm
    def find(self,event=None):
        self.text_area.tag_remove("found",1.0,END) #xoá tag tất cả
        if self.text_area.get(1.0,END).strip()=="": #trang trắng thì không chạy
            return
        else:
            answer=simpledialog.askstring("Find","Find what: ",parent=self.text_area) #hiển thị cửa sổ find
            if answer.strip()=="":
                showinfo("Find","Can't not find") #nếu không nhập -> không tìm được
                return
            elif answer==None: #ấn cancel hoặc X thì dừng
                return
            else:
                index=1.0 #vị trí bắt đầu tìm kiếm
                count=0
                while True:
                    index=self.text_area.search(answer,index,stopindex=END,nocase=1) #tìm kiếm từ
                    if not index: break
                    count+=1 #số từ tìm được tăng lên
                    lastIndex = "%s+%dc" %(index,len(answer)) #vị trí cuối được gán bằng kết thúc của từ
                    self.text_area.tag_add("found",index,lastIndex) #gán tag cho từ vừa tìm được
                    index=lastIndex #cập nhật vị trí
                self.text_area.tag_config("found",background="blue") #những từ được gắn tag thì sẽ bôi đen
                if(count==0):
                    showinfo("Find","Can't not find") #không tìm được thì hiện thông báo
                return

    def about(self,event=None):
        showinfo("Text Editor", "BTL nhom 21") #hiện cửa sổ infor
    
    def out(self): #đóng chương trình
        sys.exit()
    
    def do_popup(self,event): #hiện menu của chuột
        try:
            self.mouse.tk_popup(event.x_root, event.y_root) #hiện menu của chuột tại vị trí con trỏ chuột
        finally:
            self.mouse.grab_release() #thoát

    #hàm chạy chương trình
    def run(self):
        self.window.mainloop() #chạy cửa sổ windows

    #mở cửa sổ tìm và sửa
    def openFindReplaceDialog(self, event=None):
        if(self.text_area.get(1.0,END).strip()==""): #trang trống thì không chạy
            return 
        if getattr(self, "findReplace", None): #kiểm tra findReplace có tồn tại không
            self.findReplace.deiconify() #mở cửa sổ
        else:
            self.findReplace = FindReplaceDialog(self.window,self.text_area, True) #mở toplever hộp thoại tìm kiếm

    #hàm xử lí khi đóng
    def on_closing(self):
        if self.file==None and self.text_area.get(1.0,END)=="\n": #không có tên file, khôgn có nội dung -> đóng
            self.out()
        #file mở nhưng không chỉnh sửa cũng đóng
        elif self.file!=None and self.text_area.get(1.0,END).rstrip()==open(os.path.abspath(self.file),"r",encoding="utf-8").read().rstrip(): 
            self.out()
        else:
            answer=askyesnocancel("Text Editor","Do you want to save this file ?") #mở cửa sổ hỏi có lưu hay không
            if answer:
                if(self.file==None): #không có đường dẫn, tạo đường dẫn và lưu file
                    self.saveAs_file()
                    self.out()
                else:
                    self.save_file() #lưu file
                    self.out()
            elif answer is None: #không trả lời -> đóng cửa sổ
                return
            else: #không lưu, thoát
                self.out()

class FindReplaceDialog(Toplevel): #cửa sổ find and repalce
    def __init__(self, master , textWidget, withdrawInsteadOfDestroy=False, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.transient(master) #tạo cửa sổ tạm thời
        self.resizable(False, False) #không thay đổi kích thước
        self.title("Find And Replace")

        frame = FindReplaceFrame(self, textWidget) #tạo frame cho toplever
        frame.pack(fill="both", padx=10, pady=10) 

        #thiết lập kích thước cho cửa sổ
        x = master.winfo_rootx() + (master.winfo_width()/2) - (self.winfo_reqwidth()/2)
        y = master.winfo_rooty() + (master.winfo_height()/2) - (self.winfo_reqheight()/2)
        self.geometry(f'+{int(x)}+{int(y)}')

        #xử lí khi đóng
        if withdrawInsteadOfDestroy: 
            self.protocol("WM_DELETE_WINDOW", self.withdraw)
        

class FindReplaceFrame(Frame): 
    def __init__(self, master, textWidget, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.textWidget = textWidget #gán nội dung của text_area vào để tìm kiếm
        self.findStartPos = 1.0 #vị trí bắt đầu tìm

        #gán thuộc tính cho frame
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, pad=8)
        self.rowconfigure(1, pad=8)

        Label(self, text="Find: ").grid(row=0, column=0, sticky="nw") #tạo label Find
        self.findEntry = Entry(self) #tạo ô để ghi nội dung
        self.findEntry.grid(row=0, column=1, sticky="new")
        self.findEntry.focus()

        Label(self, text="Replace: ").grid(row=1, column=0, sticky="nw") #tạo label Replace
        self.replaceEntry = Entry(self)
        self.replaceEntry.grid(row=1, column=1, sticky="new")

        buttonFrame = Frame(self) #container
        buttonFrame.grid(row=2, column=0, columnspan=2, sticky="nsew") #vị trí các nút
        self.findNextButton = Button(buttonFrame, text="Find Next", command=self.findNext)  #nút findnext
        self.findNextButton.grid(row=0, column=0, padx=(0, 5))
        self.replaceButton = Button(buttonFrame, text="Replace", command=self.replace) #nút replace
        self.replaceButton.grid(row=0, column=1, padx=(0, 5))
        self.replaceAllButton = Button(buttonFrame, text="Replace All", command=self.replaceAll) #nút replace all
        self.replaceAllButton.grid(row=0, column=2)

        optionsFrame = Frame(self) #tạo ô checkbox
        optionsFrame.grid(row=3, column=0, sticky="nsew")
        self.matchCaseVar = BooleanVar(self, True)
        self.matchCaseCheckbutton = Checkbutton(optionsFrame, text="Match Case", variable=self.matchCaseVar) #nút matchcase
        self.matchCaseCheckbutton.grid(row=0, column=0, sticky="nw")
        

    def findNext(self):
        key = self.findEntry.get().strip() #từ cần tìm kiếm
        pos = self.textWidget.search(key, INSERT, nocase=not self.matchCaseVar.get()) #tìm vị trí bắt đầu của từ đó 
        if pos:
            endIndex = f'{pos}+{len(key)}c' #vị trí kết thúc
            if self.textWidget.tag_ranges(SEL): 
                self.textWidget.tag_remove(SEL, SEL_FIRST, SEL_LAST) #xoá tag khỏi đoạn này
            self.textWidget.tag_add(SEL, pos, endIndex) #thêm tag vào từ
            self.textWidget.tag_configure(SEL, background="blue") #từ có tag thì bôi đen
            self.textWidget.tag_add("found", pos, endIndex) #thêm tag vào từ
            self.textWidget.tag_configure("found", background="blue")
            self.textWidget.mark_set(INSERT, endIndex) #đánh dấu vị trí để tiếp tục tìm kiếm
            self.textWidget.see(endIndex)

    def replace(self):
        key = self.findEntry.get().strip() #nhận từ cần tìm
        repl = self.replaceEntry.get().strip() #nhận từ thay đổi

        selRange = self.textWidget.tag_ranges(SEL) #nhận vào khoảng cần tìm kiếm
        if selRange: 
            selection = self.textWidget.get(selRange[0], selRange[1])
            if not self.matchCaseVar.get(): # viết thường hết để so sánh 2 giá trị
                key = key.lower()
                selection = selection.lower()
            if key == selection:
                self.textWidget.delete(selRange[0], selRange[1]) #xoá đoạn sel
                self.textWidget.insert(selRange[0], repl) #chèn từ thay thế vào
                mark=f"{selRange[0]}+{len(repl)}c" #vị trí cuối cùng của từ
                self.textWidget.tag_add("found",selRange[0],mark)
                self.textWidget.tag_configure("found",background="blue") #đánh dấu từ
        self.findNext() #tìm từ tiếp theo

    #hàm sửa toàn bộ
    def replaceAll(self):
        start = "1.0" #bắt đầu từ kí tự đầu tiên
        key = self.findEntry.get().strip() #nhận từ cần tìm
        repl = self.replaceEntry.get().strip() #nhận từ thay đổi
        count = 0
        
        while True:
            pos = self.textWidget.search(key, start, "end") #trả về vị trí đầu tiên tìm thấy
            if pos:
                self.textWidget.delete(pos, f"{pos}+{len(key)}c") #xoá từ từ tim được
                self.textWidget.insert(pos, repl) #thay bằng từ mới
                start = f"{pos}+{len(repl)}c" #cập nhật vị trí
                self.textWidget.tag_add("found",pos,start) #thêm nhãn cho từ vừa sửa
                self.textWidget.tag_configure("found",background="blue") #có nhãn thì bôi đen
                count += 1
            else:
                showinfo("Replaced", f"Replaced {count} occurences.") #hiển thị số từ đã sửa
                break

if __name__=="__main__":
    root=Tk()             
    textEditor=TextEditor(root,width=800,height=600)
    textEditor.run()