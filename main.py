from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from tools import *
import sys

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

if __name__ == "__main__": # So that the script can't be executed indirectly
    app = QApplication(sys.argv) # Initializes the application
    window = MainWindow() # initializes the window by instantiating the screen class
    window.show()
    sys.exit(app.exec_()) # destroys the program to stop it running after the program has been closed.