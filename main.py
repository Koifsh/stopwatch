from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys,time
from threading import Thread

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(300,300,500,400)
        self.setStyleSheet("background: #161219;")
        self.setWindowTitle("stopwatch")
        self.seconds = 0
        self.widgets = {"title": Text(self,"Timer",(215,10),15),
                        "colons": Text(self,":                 :",(215,50),15),
                        "hours": LineEdit(self,"00",(165,60),(50,50)),
                        "minutes": LineEdit(self,"00",(250,60),(50,50)),
                        "seconds": LineEdit(self,"00",(335,60),(50,50)),
                        "start": Button(self,"Start",(20,140),size=(100,50),func=self.startTimer,colour="green"),
                        "stop": Button(self,"Stop",(200,140),size=(100,50),func=self.stopTimer,colour="red"),
                        "reset": Button(self,"Reset",(380,140),size=(100,50),func=self.resetTimer,colour="orange"),
                        
                        }
        self.widgets["minutes"].setMaxLength(2)
        self.widgets["seconds"].setMaxLength(2)
        self.update()
    
    def resetTimer(self):
        self.timer.stop()
        for i in ("hours","minutes","seconds"):
            self.widgets[i].setEnabled(True)
        for i in ("hours","minutes","seconds"):
            self.widgets[i].setText("")
    
    def startTimer(self):
        if all(True if self.widgets[i].text().zfill(2) == "00" else False for i in ("hours","minutes","seconds")):
            self.widgets["title"].notice(0.5,"Enter Values","Timer")
            return
        if not all(True if self.widgets[i].text().zfill(2).isnumeric() else False for i in ("hours","minutes","seconds")):
            self.widgets["title"].notice(0.5,"Enter Numeric","Timer")
            return
        for i in ("hours","minutes","seconds"):
            self.widgets[i].setEnabled(False)
        hours,minutes,seconds = (self.widgets[i] for i in ("hours","minutes","seconds"))
        hours.setText(f"{'00' if hours.text() == '' else hours.text()}")
        minutes.setText(f"{minutes.text().zfill(2)}")
        seconds.setText(f"{seconds.text().zfill(2)}")
        self.totalseconds = (int(hours.text())*3600) + (int(minutes.text())*60) + int(seconds.text())
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.counter)
        self.timer.start()
    
    def counter(self):
        self.totalseconds -= 1
        if self.totalseconds < 1:
            self.timer.stop()
            self.widgets["title"].notice(0.5,"Finished","Timer")
            for i in ("hours", "minutes", "seconds"):
                self.widgets[i].setText("")
                self.widgets[i].setEnabled(True)
                self.update()
            return
        
        
        hours = self.totalseconds//3600
        minutes = (self.totalseconds//60) - (hours*60)
        seconds = (self.totalseconds % 60)
        self.widgets["hours"].setText(f"{str(hours).zfill(2)}")
        self.widgets["minutes"].setText(f"{str(minutes).zfill(2)}")
        self.widgets["seconds"].setText(f"{str(seconds).zfill(2)}")
        self.update()
    
    def stopTimer(self):
        for i in ("hours","minutes","seconds"):
            self.widgets[i].setEnabled(True)
        self.timer.stop()
    
    def update(self):#This updates the different frames so that each widget can be seen
        for widget in self.widgets.values():
            widget.show()


class Progressbar(QProgressBar):
    def __init__(self,window, pos,text= "", backgroundcolor = "orange", barcolor = "red", min = 0, max = 100):
        super().__init__(window)
        self.win = window
        self.setMinimum(min)
        self.setMaximum(max)
        self.move(*pos)
        self.setFixedSize(200,30)
        self.setFormat(text)
        self.setStyleSheet("QProgressBar {"
                           f"background-color: {backgroundcolor};"
                           "color: white;"
                           "border-color: orange;"
                           "border-radius: 2px;"
                           "text-align: center; }"

                           "QProgressBar::chunk {"
                           "border-radius: 2px;"
                           f"background-color: {barcolor};"+"}")
        
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.counter)
        
    def counter(self):
        self.win.warmth -= 2
        self.setValue(self.win.warmth)
        self.update()
        if self.win.warmth == 0:
            self.win.close()

class Button(QPushButton):
    #Here I have taken window as an argument to stop cyclical imports
    def __init__(self,window,text,pos=None,size = (200,70),func="notentered",text_size=15,colour="white"):
        super().__init__(text, window)
        self.win = window  # setting the window as a class variable
        self.cooldownstate = False
        self.func = func
        if pos is not None: #Move the button if the position argument is specified
            self.move(*pos)
        self.setFixedSize(*size)
        self.setStyleSheet(
        #Setting the style of the button
        '''
        QPushButton {
        border: 4px solid #737373;
        color: white;
        font-family: shanti;'''+
        f"font-size: {text_size}px;" +'''
        border-radius: 4px;
        margin-top: 0px}
        
        QPushButton::hover{
            background: '''+f"{colour}"+''';
        }
        ''')
         #Matching buttons to the screens it should take the user to.
        self.clicked.connect(self.func)
        # Functions that are not transition buttons are managed in the main script 
            # to avoid back and forth between different files

    def notice(self, sleeptime, message, orgmessage): # Gives the user a brief idea of what the button has just done
        def noticefunc():
            self.setEnabled(False)#This variable makes sure that the button wont do anything while the message is displayed
            self.setText(message)
            time.sleep(sleeptime)
            self.setText(orgmessage)
            self.setEnabled(True)
         #daemon thread allows the rest of the screen to function while the message is being displayed
        self.noticethread = Thread(target=noticefunc, daemon = True)
        self.noticethread.start()

class LineEdit(QLineEdit):
    def __init__(self,window,text,pos,size=(200,50)):
        super().__init__(window)
        self.move(*pos)
        self.setPlaceholderText(text) # Gives the edit box a prompt
        self.setFixedSize(*size)
        self.setStyleSheet(
            #Sets the style of the edit boxes
            '''
            QLineEdit {
            border: 4px solid #161219;
            color: white;
            font-family: shanti;
            font-size: 15px;
            border-radius: 4px;
            margin-top: 0px}
            '''
        )

class Text(QLabel):
    def __init__(self,window,text,pos,size):
        super().__init__(text,window)
        self.move(*pos)
        self.setAlignment(Qt.AlignCenter) # changes the alignment to the center of the widget
        self.setStyleSheet( # sets the style of the text
            "*{"+
            f'''color: white;
            font-family: 'shanti';
            font-size: {size}px;

            margin-top: 20px'''
            +"}")
        self.setFixedHeight(size*3) # adjusts the size of the widget based on text size.
    
    def notice(self, sleeptime, message, orgmessage): # Gives the user a brief idea of what the button has just done
        def noticefunc():
            self.setText(message)
            time.sleep(sleeptime)
            self.setText(orgmessage)
         #daemon thread allows the rest of the screen to function while the message is being displayed
        self.noticethread = Thread(target=noticefunc, daemon = True)
        self.noticethread.start()

        
if __name__ == "__main__": # So that the script can't be executed indirectly
    app = QApplication(sys.argv) # Initializes the application
    window = MainWindow() # initializes the window by instantiating the screen class
    window.show()
    sys.exit(app.exec_()) # destroys the program to stop it running after the program has been closed.