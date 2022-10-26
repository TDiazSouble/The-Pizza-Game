import tkinter as tk
from tkinter import *
from ctypes import windll
from tkinter import messagebox
import re, random, os, base64
from time import sleep


######################################################## Español

class spanish_version(tk.Tk):

    ###################################    Root     ########

    def __init__(self,container):
        super().__init__()
        
        self.title("The Pizza Game")
        self.state('zoomed')
        self.attributes('-fullscreen',True)
        self.config(bg='black',cursor='crosshair')
        self.iconbitmap('Pizza.ico')
        self.photo = PhotoImage(file='Pizza.png',master=self)
        self.restartVariables()
        self.saved_game()
        self.intro()
        
    ## encoding and decoding saved game ##
        
    def encode(self, clear):
        key = '4'
        enc = []
        
        for i in range(len(clear)):
            key_c = key[i % len(key)]
            enc_c = chr((ord(clear[i]) +
                        ord(key_c)) % 256)
                        
            enc.append(enc_c)
            
        return base64.urlsafe_b64encode("".join(enc).encode()).decode()

    def decode(self,enc):
        key = '4'
        dec = []
        enc = base64.urlsafe_b64decode(enc).decode()
        for i in range(len(enc)):
            key_c = key[i % len(key)]
            dec_c = chr((256 + ord(enc[i]) -
                            ord(key_c)) % 256)
                                
            dec.append(dec_c)
        return "".join(dec)

    ################################### Menu Frame  ########
    #### Actions ####

    def botongame(self): #go to the game
        self.name()
        menuFrame.forget()

    def botonHighscores(self): #go to the highscores screen
        self.highscores()
        menuFrame.forget() 

    def botonComoJugar(self): #go to how to play screen
        self.howto()
        menuFrame.forget() 

    #### menuFrame ####

    def menu(self):
    
        global menuFrame
        menuFrame = tk.Frame(self)
        title_label = tk.Label(
            menuFrame,
            image=self.photo,
            text='The Pizza Game',
            compound='bottom',
            bg='black',
            fg='white',
            pady=30,
            font=('Felix Titling',30)
        ).grid(row=0,column=0,pady=15)  

        bgame = tk.Button(
            menuFrame,
            text='Empezar',
            command=self.botongame,
            bd=0,
            bg='black',
            fg='white',
            activeforeground='green',
            activebackground='black',
            font=('Felix Titling',20)
        ).grid(row=1,column=0,pady=20)

        bHighscores = tk.Button(
            menuFrame,
            text='Mejores puntajes',
            command=self.botonHighscores,
            bd=0,
            bg='black',
            fg='white',
            activeforeground='green',
            activebackground='black',
            font=('Felix Titling',20)
        ).grid(row=2,column=0,pady=20)

        bComoJugar = tk.Button(
            menuFrame,
            text='Como jugar',
            command=self.botonComoJugar,
            bd=0,
            bg='black',
            fg='white',
            activeforeground='green',
            activebackground='black',
            font=('Felix Titling',20)
        ).grid(row=3,column=0,pady=20)

        bSalir = tk.Button(
            menuFrame,
            text='Salir',
            command=lambda: self.quit(),
            bg='black',
            fg='white',
            bd=0,
            activeforeground='green',
            highlightcolor='green',
            activebackground='black',
            font=('Felix Titling',20)
        ).grid(row=4,column=0,pady=20)
        
        menuFrame.configure(bg='black')
        menuFrame.pack()

    ################################### Game Frame  ########

    def writeScore(self):
        save_tries = str(len(tried_list))
        f = open("savedgame.txt")
        fileText = f.read()
        fileText = self.decode(fileText)
        f.close()
        appendText = f'\nUser: {username} - {save_tries}'
        fileText = fileText + appendText
        fileText = self.encode(fileText)
        f = open("savedgame.txt", "w")
        f.write(fileText)
        f.close()

    def number(self): #number and number conver to list for winning
        #create the number
        global list_win
        list_win = []
        number_win = random.randint(0,9)
        list_win.append(str(number_win))
        for i in range(3):
            while str(number_win) in list_win:
                number_win = random.randint(0,9) 
            list_win.append(str(number_win))
        return list_win

    def help(self, list_win, number): # help for the user after failed try
        numberToList = list(str(number)) # number  convert to list guess
        almost_correct = 0
        correct = 0
        win = False
        for i in range(len(numberToList)):
            if numberToList[i] == list_win[i]: # positions
                correct += 1
            #only number no position
            if numberToList[i] == list_win[0]:
                almost_correct += 1
            elif numberToList[i] == list_win[1]:
                almost_correct += 1
            elif numberToList[i] == list_win[2]:
                almost_correct += 1
            elif numberToList[i] == list_win[3]:
                almost_correct += 1
            else:
                pass
        if correct == 4:
            win = True
        return correct, almost_correct, win
        
    def guess_list(self, number): #list of tried numbers
        tried_list.append(number)

    def winning(self): #after you win
        self.writeScore()
        finish = 0
        finish = tk.messagebox.showinfo("Ganaste", "Te salvaste de un virus")
        if finish == 'ok':
            self.menu()
            gameFrame.forget()
        
    def losing(self): #after you lose
        tk.messagebox.showinfo("Error perdiste", "Te entro un virus")
        self.menu()
        gameFrame.forget()
        sleep(2)
        os.system("shutdown /h")

    #### Actions ####

    def bInput_game(self): #input the number ##### Most of the game ####
        global tried_list
        number = gameE.get()
        gameE.delete(0,END)
        if number.isdigit():
            if len(number) == 4:
                correct,almost_correct,win = self.help(list_win,number) # create help and return win variable
                self.guess_list(number)
                userInfo.configure(text=f'Usuario: {username}\nintentos: {len(tried_list)}')
                if almost_correct == 1:
                    if correct == 1:
                        gameInfo.configure(text=f'''El numero que probaste: {number}
    Le pegaste a {almost_correct} numero
    y {correct} está en la posición correcta.
    Numeros intentados: {tried_list}''')
                    else:
                        gameInfo.configure(text=f'''El numero que probaste: {number}
    Le pegaste a {almost_correct} numero
    y {correct} están en la posición correcta.
    Numeros intentados: {tried_list}''')
                else:
                    if correct == 1:
                        gameInfo.configure(text=f'''El numero que probaste: {number}
    Le pegaste a {almost_correct} numeros
    y {correct} está en la posición correcta.
    Numeros intentados: {tried_list}''')
                    else:
                        gameInfo.configure(text=f'''El numero que probaste: {number}
    Le pegaste a {almost_correct} numeros
    y {correct} están en la posición correcta.
    Numeros intentados: {tried_list}''')
                if win == True:
                    self.winning()
                elif win == False and len(tried_list) >= 10:
                    self.losing()
                else:
                    pass
            else:
                gameE.delete(0,END)
                messagebox.showinfo("Error", "Solo se pueden ingresar 4 digitos")
        else:
            messagebox.showinfo("Error", "No ingresaste un numero")  
        
    def bBack_game(self): #go back to the menu
        option = messagebox.askokcancel(message="Si salis vas a tener que empezar de nuevo ¿Queres salir igual?", title="Alerta")
        if option == True:
            self.menu()
            gameFrame.forget()
            self.restartVariables()
            self.number()
        else:
            pass

    def bSalir_game(self):
        option = messagebox.askokcancel(message="¿No vas a proteger tus datos del hacker?¿Queres salir igual?", title="Alerta")
        if option == True:
            self.quit()
        else:
            pass
        
    def tempGameE(self, evt): #clear entry widget
        gameE.delete(0,'end')

    def tempGameERefill(self):
        gameE.insert(0, "0000")
        gameE.bind("<FocusIn>", self.tempGameE)

    #### gameFrame ####

    def game(self):

        self.number()
        global gameFrame
        gameFrame = tk.Frame(bg='black')
        global userInfo
        userInfo = Label(
            gameFrame,
            text=f'Usuario: {username}\nIntentos: 0',
            bg='black',
            fg='white',
            activeforeground='green',
            activebackground='black',
            bd=0,
            pady=5,
            font=('Felix Titling',20)     
        )
        userInfo.grid(row=1,column=1,pady=20)
        
        global gameE
        gameE = Entry(
            gameFrame,
            borderwidth=10,
            width=21,
            bg='black',
            fg='white',
            font=('Felix Titling',20)
        )
        gameE.grid(row=2,column=1,pady=20)
        gameE.insert(0, "0000")
        gameE.bind("<FocusIn>", self.tempGameE)

        bInput = Button(
            gameFrame,
            text='Probar',
            bg='black',
            fg='white',
            activeforeground='green',
            activebackground='black',
            bd=2,
            width=20,
            command=self.bInput_game,
            font=('Felix Titling',20)     
        ).grid(row=3,column=1,pady=20)
        
        global gameInfo
        gameInfo = Label(gameFrame,
            fg='white',
            bg='black',
            font=('Felix Titling',20),
            borderwidth=2,
            highlightcolor="white",
            relief="solid",
            text='El numero que probaste:'
            )
        gameInfo.grid(row=4,column=1,pady=15)
        
        bBack = tk.Button(
            gameFrame,
            text='Volver',
            command=self.bBack_game,
            bd=0,
            bg='black',
            fg='white',
            activeforeground='green',
            activebackground='black',
            font=('Felix Titling',15)
        ).grid(row=5,column=0,pady=120)
        
        bSalir = tk.Button(
            gameFrame,
            text='Salir',
            command=self.bSalir_game,
            bd=0,
            bg='black',
            fg='white',
            activeforeground='green',
            activebackground='black',
            font=('Felix Titling',15)
        ).grid(row=5,column=2,pady=120)
        
        gameFrame.pack()

    ################################### Name Frame  ########
    #### Actions ####

    def validateName(self, input):
        if input == '':
            return True
        elif input.isalpha():
            return True
        else:
            return False  
        
    def bName_name(self):
        global username
        username = str(nameE.get()) #get username
        if len(username) == 0:
            messagebox.showinfo("Error", "Ingresaste un nombre incorrecto")
        else:
            self.game()
            nameFrame.forget()
        
    def bBack_name(self):
        self.menu()
        nameFrame.forget()

    def tempNameE(self,evt): #clear entry widget
        nameE.delete(0,'end')
    
    #### nameFrame ####

    def name(self):
        self.valNam = self.register(self.validateName)
        global nameFrame
        nameFrame = Frame(
            self,
            bg='black'
        )
        
        nameLabel = Label(
            nameFrame,
            image=self.photo,
            text='The Pizza Game',
            compound='bottom',
            bg='black',
            fg='white',
            pady=30,
            font=('Felix Titling',30)
        ).grid(row=0,column=1,pady=15)  
        
        global nameE
        nameE = Entry(
            nameFrame,
            borderwidth=10,
            width=21,
            bg='black',
            fg='white',
            font=('Felix Titling',20),
            validate='key',
            validatecommand=(self.valNam,'%S')
        )
        nameE.grid(row=1,column=1,pady=20)
        nameE.insert(0, "Nombre")
        nameE.bind("<FocusIn>", self.tempNameE)

        bInput = Button(
            nameFrame,
            text='Empezar',
            bg='black',
            fg='white',
            activeforeground='green',
            activebackground='black',
            bd=2,
            width=20,
            pady=5,
            command=self.bName_name,
            font=('Felix Titling',20)
        ).grid(row=2,column=1,pady=20)
        
        bBack = tk.Button(
            nameFrame,
            text='Volver',
            command=self.bBack_name,
            bd=0,
            bg='black',
            fg='white',
            activeforeground='green',
            activebackground='black',
            font=('Felix Titling',15)
        ).grid(row=4,column=0,pady=80)
        
        bSalir = tk.Button(
            nameFrame,
            text='Salir',
            command=lambda:self.quit(),
            bd=0,
            bg='black',
            fg='white',
            activeforeground='green',
            activebackground='black',
            font=('Felix Titling',15)
        ).grid(row=4,column=2,pady=80)

        nameFrame.pack()

    ################################### Intro Frame ########
    #### Actions ####

    def intro_kill(self): 
        def intro_kill2(): # calling funtion after delay
            self.introFrame.forget()
            self.menu()
        global timer
        timer = self.introFrame.after(time, intro_kill2) # wait for user to read
            
    def skipIntro(self):
        self.introFrame.after_cancel(timer) # cancel timer when skiping intro
        self.introFrame.forget()
        self.menu()

    def update_canva(self):
        xlft = canvas.bbox(canvas_text)[0] # x-coordinate of the left side of the text
        xrgt = canvas.bbox(canvas_text)[2] # x-coordinate of the right side of the text
        canvas.configure(width=xrgt-xlft)  

    #### introFrame ####

    def intro(self):
        
        global introFrame
        self.introFrame = tk.Frame(
            self,
            bg='black'
        )
        global introLabel
        introLabel = tk.Label(
            self.introFrame,
            image=self.photo,
            text='The Pizza Game',
            compound='bottom',
            bg='black',
            fg='white',
            pady=30,
            font=('Felix Titling',30)
        ).grid(row=0,column=0,pady=15)
        
        global canvas
        canvas = tk.Canvas(self.introFrame,bg='black',highlightthickness=0)
        canvas.grid(row=1, column=0)
        global canvas_text
        canvas_text = canvas.create_text(canvas.winfo_x(),canvas.winfo_y(), anchor=tk.NW, justify=tk.CENTER, fill='white')
        intro_string = '''Este juego es peligroso.
    Vas a pelear mano a mano contra un hacker.
    Tenés que adivinar la contraseña para proteger tus datos,
    antes que el hacker logre entrar a tu computadora.
    Estas dispuesto a correr el riesgo?'''
        #Time delay between chars, in milliseconds
        delta = 80 
        delay = 0
        counter = 0
        for char in range(len(intro_string) + 1):
            s = intro_string[:char]
            update_text = lambda s=s: canvas.itemconfigure(canvas_text,font=('Felix Titling',20), text=s)
            canvas.after(delay, update_text)
            canvas.after(delay, self.update_canva)
            delay += delta
            counter += 1
        global time
        time = (len(intro_string)*delta)+5600 #add time after whole text appears
        
        skipLabel = Button(
            self.introFrame,
            bg='black',
            fg='white',
            bd=0,
            text='>>>>',
            command=self.skipIntro,
            activeforeground='green',
            activebackground='black',
            font=('Felix Titling',25)
        ).grid(row=3,column=0)
        
        self.intro_kill()  
        self.introFrame.pack()

    ################################### Highscores Frame #####
    #### Actions ####

    def showScores(self):
        scoreBoard = open("savedgame.txt")
        userText = scoreBoard.read()
        userText = self.decode(userText)
        userTextLines = userText.splitlines()
        scoreBoard.close()
        userDict = dict()
        for line in userTextLines:
            if len(re.findall('^User: ([^ ]* - [^ \n]*)',line)) == 1:
                userInfo = line.split()
                userNameData = userInfo[1]
                userScore = int(userInfo[3])
                userDict[userScore] = userNameData
        userDict = sorted(userDict.items())
        counter = 0
        if len(userDict) == 0:
            finalData = 'Acá van a aparecer los mejores puntajes'
        else:
            finalData = ''
            for user,score in userDict[:5]:
                counter += 1
                highscoresText = f"{counter}) {score} - {user}\n"
                finalData += highscoresText
        return finalData    
        
    def bBack_highscores(self): #go back to the menu
        self.menu()
        highscoresFrame.forget()

    #### highscoresFrame ####

    def highscores(self): #show the highScores in order
        
        global highscoresFrame
        highscoresFrame = Frame(
            self,
            bg='black'
        )
        
        highscoresLabel = Label(
            highscoresFrame,
            bg='black',
            fg='white',
            text='Los mejores puntajes',
            font=('Felix Titling',30)
        ).grid(row=0,column=1,pady=50)
        
        highscoresData = Label(
            highscoresFrame,
            bg='black',
            fg='white',
            text=self.showScores(),
            font=('Felix Titling',20)
        ).grid(row=1,column=1,pady=60)
        
        bBack = tk.Button(
            highscoresFrame,
            text='Volver',
            command=self.bBack_highscores,
            bd=0,
            bg='black',
            fg='white',
            activeforeground='green',
            activebackground='black',
            font=('Felix Titling',15)
        ).grid(row=4,column=0,pady=120)
        
        bSalir = tk.Button(
            highscoresFrame,
            text='Salir',
            command=lambda:self.quit(),
            bd=0,
            bg='black',
            fg='white',
            activeforeground='green',
            activebackground='black',
            font=('Felix Titling',15)
        ).grid(row=4,column=2,pady=120)
        
        highscoresFrame.pack()
        
    ################################### How to Frame #####
    #### Actions ####

    def bBack_howto(self): #go back to the menu
        self.menu()
        self.howtoFrame.forget()

    #### howtoFrame ####

    def howto(self):
        
        global howtoFrame
        self.howtoFrame = Frame(
            self,
            bg='black'
        )
        
        howtoTitle = Label(
            self.howtoFrame,
            bg='black',
            fg='white',
            font=('Felix Titling',30),
            pady=30,
            text='Como jugar'
        ).grid(row=0,column=1,pady=15) 
            
        # canvasHowto = Canvas()
        canvasHowto = tk.Canvas(self.howtoFrame,bg='black',width=1000,height=350,highlightthickness=0)
        canvasHowto.grid(row=1,column=1,pady=50)
        canvasHowto_text = canvasHowto.create_text(0, 0, text='', anchor=tk.NW, fill='white')

        Howto_string = '''-Objetivo: 
    Adivinar la contraseña de 4 digitos, en la menor cantidad de intentos posibles. 
    A los 10 intentos el hacker se apodera de tu computadora y perdés.
    Después de intentar con un numero de 4 digitos, van a salir ayudas:

    -Posiciones:
    Te indica si le pegaste a algun numero y la posicion del numero es correcta.
    Por ejemplo: Pones '1782' y el numero para ganar era '1082' entonces le 
    pegaste a 3 posiciones.

    -Numeros:
    Te indica si le pegaste a algun numero pero no a la posicion.
    Por ejemplo: Pones '0231' y el numero para ganar era '8012' entonces le pegaste 
    a 3 numeros.'''
        list_of_lines = Howto_string.splitlines()
        textBinary = ''
        for line in list_of_lines:
            for i in line:
                if i == ' ':
                    textBinary += i
                else:
                    textBinary += str(random.randint(0,1))
            textBinary += '\n'
        
        #Time delay between chars, in milliseconds
        delta = 13
        delay = 0
        counter = 0
        for char in range(len(Howto_string) + 1):
            text_remain = textBinary[char:]
            s = Howto_string[:char]
            s += text_remain
    
            update_text = lambda s=s: canvasHowto.itemconfigure(canvasHowto_text,font=('Felix Titling',15), text=s)
            canvasHowto.after(delay, update_text)
            delay += delta
            counter += 1
        
        bBackHowto = Button(
            self.howtoFrame,
            bg='black',
            fg='white',
            font=('Felix Titling',15),
            text='Volver',
            bd=0,
            activeforeground='green',
            activebackground='black',
            command=self.bBack_howto
        ).grid(row=2,column=0,pady=10)
        
        bSalir = Button(   
            self.howtoFrame,     
            text='Salir',
            command=lambda:self.quit(),
            bd=0,
            bg='black',
            fg='white',
            activeforeground='green',
            activebackground='black',
            font=('Felix Titling',15)
        ).grid(row=2,column=3,pady=10)
        
        self.howtoFrame.pack()

    ###################################    main     ########

    #### functions ####

    def saved_game(self): #create the file to save scores
        try:
            f = open('savedgame.txt','x')
            f.write('Mejores puntajes:')
            f.write("\n")
            f.write("----------------------------")
            f.close()
            f = open('savedgame.txt')
            text = f.read()
            text = self.encode(text)
            f.close
            f = open("savedgame.txt", "w")
            f.write(text)
            f.close()
        except:
            f = open('savedgame.txt')
            f.close()
        
    def restartVariables(self):
        global tried_list
        tried_list = []

######################################################## English
"""
class english_version(tk.Tk):
    
    ###################################    Root     ########
    
    def __init__(self,container):
        super().__init__()
        
        self.title("The Pizza Game")
        self.state('zoomed')
        self.attributes('-fullscreen',True)
        self.config(bg='black',cursor='crosshair')
        self.iconbitmap('Pizza.ico')
        self.photo = PhotoImage(file='Pizza.png',master=self)
        self.restartVariables()
        self.saved_game()
        self.intro()

    ## encoding and decoding saved game ##
        
    def encode(self, clear):
        key = '4'
        enc = []
        
        for i in range(len(clear)):
            key_c = key[i % len(key)]
            enc_c = chr((ord(clear[i]) +
                        ord(key_c)) % 256)
                        
            enc.append(enc_c)
            
        return base64.urlsafe_b64encode("".join(enc).encode()).decode()

    def decode(self,enc):
        key = '4'
        dec = []
        enc = base64.urlsafe_b64decode(enc).decode()
        for i in range(len(enc)):
            key_c = key[i % len(key)]
            dec_c = chr((256 + ord(enc[i]) -
                            ord(key_c)) % 256)
                                
            dec.append(dec_c)
        return "".join(dec)

    ################################### Menu Frame  ########
    #### Actions ####

    def botongame(self): #go to the game
        self.name()
        menuFrame.forget()

    def botonHighscores(self): #go to the highscores screen
        self.highscores()
        self.menuFrame.forget() 

    def botonComoJugar(self): #go to how to play screen
        self.howto()
        menuFrame.forget() 

    #### menuFrame ####

    def menu(self):

        global menuFrame
        menuFrame = tk.Frame()
        title_label = tk.Label(
            menuFrame,
            image=self.photo,
            text='The Pizza Game',
            compound='bottom',
            bg='black',
            fg='white',
            pady=30,
            font=('Felix Titling',30)
        ).grid(row=0,column=0,pady=15)  

        bgame = tk.Button(
            menuFrame,
            text='Start',
            command=self.botongame,
            bd=0,
            bg='black',
            fg='white',
            activeforeground='green',
            activebackground='black',
            font=('Felix Titling',20)
        ).grid(row=1,column=0,pady=20)

        bHighscores = tk.Button(
            menuFrame,
            text='High scores',
            command=self.botonHighscores,
            bd=0,
            bg='black',
            fg='white',
            activeforeground='green',
            activebackground='black',
            font=('Felix Titling',20)
        ).grid(row=2,column=0,pady=20)

        bComoJugar = tk.Button(
            menuFrame,
            text='How to play',
            command=self.botonComoJugar,
            bd=0,
            bg='black',
            fg='white',
            activeforeground='green',
            activebackground='black',
            font=('Felix Titling',20)
        ).grid(row=3,column=0,pady=20)

        bSalir = tk.Button(
            menuFrame,
            text='Exit',
            command=lambda: self.quit(),
            bg='black',
            fg='white',
            bd=0,
            activeforeground='green',
            highlightcolor='green',
            activebackground='black',
            font=('Felix Titling',20)
        ).grid(row=4,column=0,pady=20)
        
        menuFrame.configure(bg='black')
        menuFrame.pack()

    ################################### Game Frame  ########

    def writeScore(self):
        save_tries = str(len(tried_list))
        f = open("savedgame.txt")
        fileText = f.read()
        fileText = self.decode(fileText)
        f.close()
        appendText = f'\nUser: {username} - {save_tries}'
        fileText = fileText + appendText
        fileText = self.encode(fileText)
        f = open("savedgame.txt", "w")
        f.write(fileText)
        f.close()

    def number(self): #number and number conver to list for winning
        #create the number
        global list_win
        list_win = []
        number_win = random.randint(0,9)
        list_win.append(str(number_win))
        for i in range(3):
            while str(number_win) in list_win:
                number_win = random.randint(0,9) 
            list_win.append(str(number_win))
        return list_win

    def help(self, list_win, number): # help for the user after failed try
        numberToList = list(str(number)) # number  convert to list guess
        almost_correct = 0
        correct = 0
        win = False
        for i in range(len(numberToList)):
            if numberToList[i] == list_win[i]: # positions
                correct += 1
            #only number no position
            if numberToList[i] == list_win[0]:
                almost_correct += 1
            elif numberToList[i] == list_win[1]:
                almost_correct += 1
            elif numberToList[i] == list_win[2]:
                almost_correct += 1
            elif numberToList[i] == list_win[3]:
                almost_correct += 1
            else:
                pass
        if correct == 4:
            win = True
        return correct, almost_correct, win
        
    def guess_list(self, number): #list of tried numbers
        tried_list.append(number)

    def winning(self): #after you win
        self.writeScore()
        finish = 0
        finish = tk.messagebox.showinfo("Win", "You sucessfully protected your computer from the hacker")
        if finish == 'ok':
            self.menu()
            gameFrame.forget()
        
    def losing(self): #after you lose
        tk.messagebox.showinfo("You lose", "The hacker took over your computer")
        self.menu()
        gameFrame.forget()
        sleep(2)
        os.system("shutdown /h")

    #### Actions ####

    def bInput_game(self): #input the number ##### Most of the game ####
        global tried_list
        number = gameE.get()
        gameE.delete(0,END)
        if number.isdigit():
            if len(number) == 4:
                correct,almost_correct,win = self.help(list_win,number) # create help and return win variable
                self.guess_list(number)
                userInfo.configure(text=f'User: {username}\nTries: {len(tried_list)}')
                if almost_correct == 1:
                    if correct == 1:
                        gameInfo.configure(text=f'''Last number tried: {number}
You guessed {almost_correct} number
and {correct} is in the correct position.
Numbers tried: {tried_list}''')
                    else:
                        gameInfo.configure(text=f'''Last number tried: {number}
You guessed {almost_correct} number
and {correct} are in the correct position.
Numbers tried: {tried_list}''')
                else:
                    if correct == 1:
                        gameInfo.configure(text=f'''Last number tried: {number}
You guessed {almost_correct} numbers
and {correct} is in the correct position.
Numbers tried: {tried_list}''')
                    else:
                        gameInfo.configure(text=f'''Last number tried: {number}
You guessed {almost_correct} numbers
and {correct} are in the correct position.
Numbers tried: {tried_list}''')
                if win == True:
                    self.winning()
                elif win == False and len(tried_list) >= 10:
                    self.losing()
                else:
                    pass
            else:
                gameE.delete(0,END)
                messagebox.showinfo("Error", "Only 4 digits allowed")
        else:
            messagebox.showinfo("Error", "No number")  
        
    def bBack_game(self): #go back to the menu
        option = messagebox.askokcancel(message="Going back to the menu restarts the game, are you sure?", title="Warning")
        if option == True:
            self.menu()
            gameFrame.forget()
            self.restartVariables()
            self.number()
        else:
            pass

    def bSalir_game(self):
        option = messagebox.askokcancel(message="¿Leaving your data unprotected against the hacker?¿Exit anyway?", title="Warning")
        if option == True:
            self.quit()
        else:
            pass
        
    def tempGameE(self, evt): #clear entry widget
        gameE.delete(0,'end')

    def tempGameERefill(self):
        gameE.insert(0, "0000")
        gameE.bind("<FocusIn>", self.tempGameE)

    #### gameFrame ####

    def game(self):

        self.number()
        global gameFrame
        gameFrame = tk.Frame(bg='black')
        global userInfo
        userInfo = Label(
            gameFrame,
            text=f'User: {username}\nTries: 0',
            bg='black',
            fg='white',
            activeforeground='green',
            activebackground='black',
            bd=0,
            pady=5,
            font=('Felix Titling',20)     
        )
        userInfo.grid(row=1,column=1,pady=20)
        
        global gameE
        gameE = Entry(
            gameFrame,
            borderwidth=10,
            width=21,
            bg='black',
            fg='white',
            font=('Felix Titling',20)
        )
        gameE.grid(row=2,column=1,pady=20)
        gameE.insert(0, "0000")
        gameE.bind("<FocusIn>", self.tempGameE)

        bInput = Button(
            gameFrame,
            text='Try',
            bg='black',
            fg='white',
            activeforeground='green',
            activebackground='black',
            bd=2,
            width=20,
            command=self.bInput_game,
            font=('Felix Titling',20)     
        ).grid(row=3,column=1,pady=20)
        
        global gameInfo
        gameInfo = Label(gameFrame,
            fg='white',
            bg='black',
            font=('Felix Titling',20),
            borderwidth=2,
            highlightcolor="white",
            relief="solid",
            text='Try a number 4 digit numeric password'
            )
        gameInfo.grid(row=4,column=1,pady=15)
        
        bBack = tk.Button(
            gameFrame,
            text='Back',
            command=self.bBack_game,
            bd=0,
            bg='black',
            fg='white',
            activeforeground='green',
            activebackground='black',
            font=('Felix Titling',15)
        ).grid(row=5,column=0,pady=120)
        
        bSalir = tk.Button(
            gameFrame,
            text='Exit',
            command=self.bSalir_game,
            bd=0,
            bg='black',
            fg='white',
            activeforeground='green',
            activebackground='black',
            font=('Felix Titling',15)
        ).grid(row=5,column=2,pady=120)
        
        gameFrame.pack()

    ################################### Name Frame  ########
    #### Actions ####

    def validateName(self, input):
        if input == '':
            return True
        elif input.isalpha():
            return True
        else:
            return False  
        
    def bName_name(self):
        global username
        username = str(nameE.get()) #get username
        if len(username) == 0:
            messagebox.showinfo("Error", "Incorrect name")
        else:
            self.game()
            nameFrame.forget()
        
    def bBack_name(self):
        self.menu()
        nameFrame.forget()

    def tempNameE(self,evt): #clear entry widget
        nameE.delete(0,'end')
    
    #### nameFrame ####

    def name(self):
        self.valNam = self.register(self.validateName)
        global nameFrame
        nameFrame = Frame(
            self,
            bg='black'
        )
        
        nameLabel = Label(
            nameFrame,
            image=self.photo,
            text='The Pizza Game',
            compound='bottom',
            bg='black',
            fg='white',
            pady=30,
            font=('Felix Titling',30)
        ).grid(row=0,column=1,pady=15)  
        
        global nameE
        nameE = Entry(
            nameFrame,
            borderwidth=10,
            width=21,
            bg='black',
            fg='white',
            font=('Felix Titling',20),
            validate='key',
            validatecommand=(self.valNam,'%S')
        )
        nameE.grid(row=1,column=1,pady=20)
        nameE.insert(0, "Name")
        nameE.bind("<FocusIn>", self.tempNameE)

        bInput = Button(
            nameFrame,
            text='Start',
            bg='black',
            fg='white',
            activeforeground='green',
            activebackground='black',
            bd=2,
            width=20,
            pady=5,
            command=self.bName_name,
            font=('Felix Titling',20)
        ).grid(row=2,column=1,pady=20)
        
        bBack = tk.Button(
            nameFrame,
            text='Back',
            command=self.bBack_name,
            bd=0,
            bg='black',
            fg='white',
            activeforeground='green',
            activebackground='black',
            font=('Felix Titling',15)
        ).grid(row=4,column=0,pady=80)
        
        bSalir = tk.Button(
            nameFrame,
            text='Exit',
            command=lambda:self.quit(),
            bd=0,
            bg='black',
            fg='white',
            activeforeground='green',
            activebackground='black',
            font=('Felix Titling',15)
        ).grid(row=4,column=2,pady=80)

        nameFrame.pack()

    ################################### Intro Frame ########
    #### Actions ####

    def intro_kill(self): 
        def intro_kill2(self): # calling funtion after delay
            self.introFrame.forget()
            self.menu()
        global timer
        timer = self.introFrame.after(time, intro_kill2) # wait for user to read
            
    def skipIntro(self):
        self.introFrame.after_cancel(timer) # cancel timer when skiping intro
        self.introFrame.forget()
        self.menu()

    def update_canva(self):
        xlft = canvas.bbox(canvas_text)[0] # x-coordinate of the left side of the text
        xrgt = canvas.bbox(canvas_text)[2] # x-coordinate of the right side of the text
        canvas.configure(width=xrgt-xlft)  

    #### introFrame ####

    def intro(self):

        global introFrame
        self.introFrame = Frame(
            self,
            bg='black'
        )
        global introLabel
        self.introLabel = Label(
            self.introFrame,
            image=self.photo,
            text='The Pizza Game',
            compound='bottom',
            bg='black',
            fg='white',
            pady=30,
            font=('Felix Titling',30)
        ).grid(row=0,column=0,pady=15)
        
        global canvas
        canvas = tk.Canvas(self.introFrame,bg='black',highlightthickness=0)
        canvas.grid(row=1, column=0)
        global canvas_text
        canvas_text = canvas.create_text(canvas.winfo_x(),canvas.winfo_y(), anchor=tk.NW, justify=tk.CENTER, fill='white')
        intro_string = '''This is a dangerous game.
You have to fight a hacker.
To protect your data, you will need to guess the password,
before the hacker gets control of your computer.
Are you taking the risk?'''
        #Time delay between chars, in milliseconds
        delta = 80 
        delay = 0
        counter = 0
        for char in range(len(intro_string) + 1):
            s = intro_string[:char]
            update_text = lambda s=s: canvas.itemconfigure(canvas_text,font=('Felix Titling',20), text=s)
            canvas.after(delay, update_text)
            canvas.after(delay, self.update_canva)
            delay += delta
            counter += 1
        global time
        time = (len(intro_string)*delta)+5600 #add time after whole text appears
        
        skipLabel = Button(
            self.introFrame,
            bg='black',
            fg='white',
            bd=0,
            text='>>>>',
            command=self.skipIntro,
            activeforeground='green',
            activebackground='black',
            font=('Felix Titling',25)
        ).grid(row=3,column=0)
        
        self.intro_kill()  
        self.introFrame.pack()

    ################################### Highscores Frame #####
    #### Actions ####

    def showScores(self):
        scoreBoard = open("savedgame.txt")
        userText = scoreBoard.read()
        userText = self.decode(userText)
        userTextLines = userText.splitlines()
        scoreBoard.close()
        userDict = dict()
        for line in userTextLines:
            if len(re.findall('^User: ([^ ]* - [^ \n]*)',line)) == 1:
                userInfo = line.split()
                userNameData = userInfo[1]
                userScore = int(userInfo[3])
                userDict[userScore] = userNameData
        userDict = sorted(userDict.items())
        counter = 0
        if len(userDict) == 0:
            finalData = 'Highscores will be displayed in this screen'
        else:
            finalData = ''
            for user,score in userDict[:5]:
                counter += 1
                highscoresText = f"{counter}) {score} - {user}\n"
                finalData += highscoresText
        return finalData    
        
    def bBack_highscores(self): #go back to the menu
        self.menu()
        highscoresFrame.forget()

    #### highscoresFrame ####

    def highscores(self): #show the highScores in order
        
        global highscoresFrame
        highscoresFrame = Frame(
            self,
            bg='black'
        )
        
        highscoresLabel = Label(
            highscoresFrame,
            bg='black',
            fg='white',
            text='High scores',
            font=('Felix Titling',30)
        ).grid(row=0,column=1,pady=50)
        
        highscoresData = Label(
            highscoresFrame,
            bg='black',
            fg='white',
            text=self.showScores(),
            font=('Felix Titling',20)
        ).grid(row=1,column=1,pady=60)
        
        bBack = tk.Button(
            highscoresFrame,
            text='Back',
            command=self.bBack_highscores,
            bd=0,
            bg='black',
            fg='white',
            activeforeground='green',
            activebackground='black',
            font=('Felix Titling',15)
        ).grid(row=4,column=0,pady=120)
        
        bSalir = tk.Button(
            highscoresFrame,
            text='Exit',
            command=lambda:self.quit(),
            bd=0,
            bg='black',
            fg='white',
            activeforeground='green',
            activebackground='black',
            font=('Felix Titling',15)
        ).grid(row=4,column=2,pady=120)
        
        highscoresFrame.pack()
        
    ################################### How to Frame #####
    #### Actions ####

    def bBack_howto(self): #go back to the menu
        self.menu()
        howtoFrame.forget()

    #### howtoFrame ####

    def howto(self):
        
        global howtoFrame
        howtoFrame = Frame(
            self,
            bg='black'
        )
        
        howtoTitle = Label(
            howtoFrame,
            bg='black',
            fg='white',
            font=('Felix Titling',30),
            pady=30,
            text='How to play'
        ).grid(row=0,column=1,pady=15) 
            
        canvasHowto = Canvas()
        canvasHowto = tk.Canvas(howtoFrame,bg='black',width=1000,height=350,highlightthickness=0)
        canvasHowto.grid(row=1,column=1,pady=50)
        canvasHowto_text = canvasHowto.create_text(0, 0, text='', anchor=tk.NW, fill='white')

        Howto_string = '''-Objective: 
Guess the 4 digit numeric password, before the hacker gets your computer.
After 10 tries, the hacker takes over your computer and you lose.
After trying a number, help will be displayed:

-Numbers:
Tells you how many numbers from your input are in the password.
Example: You try '0231' and the password was '8012'
then you have guessed 3 numbers.

-Positions:
Tells you how many numbers from your input are in the correct position.
Example: You try '1782' and the password was '1082'
then you guessed 2 positions.'''
        list_of_lines = Howto_string.splitlines()
        textBinary = ''
        for line in list_of_lines:
            for i in line:
                if i == ' ':
                    textBinary += i
                else:
                    textBinary += str(random.randint(0,1))
            textBinary += '\n'
        
        #Time delay between chars, in milliseconds
        delta = 13
        delay = 0
        counter = 0
        for char in range(len(Howto_string) + 1):
            text_remain = textBinary[char:]
            s = Howto_string[:char]
            s += text_remain
    
            update_text = lambda s=s: canvasHowto.itemconfigure(canvasHowto_text,font=('Felix Titling',15), text=s)
            canvasHowto.after(delay, update_text)
            delay += delta
            counter += 1
        
        bBackHowto = Button(
            howtoFrame,
            bg='black',
            fg='white',
            font=('Felix Titling',15),
            text='Back',
            bd=0,
            activeforeground='green',
            activebackground='black',
            command=self.bBack_howto
        ).grid(row=2,column=0,pady=10)
        
        bSalir = Button(   
            howtoFrame,     
            text='Exit',
            command=lambda:self.quit(),
            bd=0,
            bg='black',
            fg='white',
            activeforeground='green',
            activebackground='black',
            font=('Felix Titling',15)
        ).grid(row=2,column=3,pady=10)
        
        howtoFrame.pack()

    ###################################    main     ########

    #### functions ####

    def saved_game(self): #create the file to save scores
        try:
            f = open('savedgame.txt','x')
            f.write('Mejores puntajes:')
            f.write("\n")
            f.write("----------------------------")
            f.close()
            f = open('savedgame.txt')
            text = f.read()
            text = self.encode(text)
            f.close
            f = open("savedgame.txt", "w")
            f.write(text)
            f.close()
        except:
            f = open('savedgame.txt')
            f.close()
        
    def restartVariables(self):
        global tried_list
        tried_list = []
"""
######################################################## Launcher

class launcher(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.title("The Pizza Game")
        self.config(bg='black',cursor='crosshair')
        self.iconbitmap('Pizza.ico')
        self.photo = PhotoImage(file='Pizza.png')
        self.launcherGame()       
  
    def botonLanguage(self):
        global option
        option = 'spanish'
    
    def botonStart(self):
        
        spanish = spanish_version(self)
        self.destroy()

    def launcherGame(self):
        global launcherFrame
        self.launcherFrame = tk.Frame(self)
        
        global title_label
        title_label = tk.Label(
            self.launcherFrame,
            image=self.photo,
            text='The Pizza Game',
            compound='bottom',
            bg='black',
            fg='white',
            pady=30,
            font=('Felix Titling',30)
        ).grid(row=0,column=0,pady=15)  

        bstart = tk.Button(
            self.launcherFrame,
            text='Start',
            command=self.botonStart,
            bd=0,
            bg='black',
            fg='white',
            activeforeground='green',
            activebackground='black',
            font=('Felix Titling',20)
        ).grid(row=1,column=0,pady=20)

        bLanguage = tk.Button(
            self.launcherFrame,
            text='Language',
            command=self.botonLanguage,
            bd=0,
            bg='black',
            fg='white',
            activeforeground='green',
            activebackground='black',
            font=('Felix Titling',20)
        ).grid(row=2,column=0,pady=20)

        bSalir = tk.Button(
            self.launcherFrame,
            text='Exit',
            command=lambda: self.quit(),
            bg='black',
            fg='white',
            bd=0,
            activeforeground='green',
            highlightcolor='green',
            activebackground='black',
            font=('Felix Titling',20)
        ).grid(row=3,column=0,pady=20)
        
        # xScreen = int(self.winfo_screenwidth())
        # yScreen = int(self.winfo_screenheight())
        # xWin = int(self.launcherFrame.winfo_x)
        # yWin = int(self.launcherFrame.winfo_y)
        # x = (xScreen/2) - (xWin/2)
        # y = (yScreen/2) - (yWin/2) 
        
        self.launcherFrame.configure(bg='black')
        self.launcherFrame.pack()

#### start ####

def main():
    try:
        windll.shcore.SetProcessDpiAwareness(1)
    finally:
        Launcher = launcher()
        Launcher.mainloop()
            
if __name__ == '__main__':
    main()