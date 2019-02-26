from mailbox import Mailbox
import time
import subprocess
import threading
import json
import os

class Logger:
    delayIntervals = {"ten_seconds":10, "one_min":60, "five_minutes":300, "ten_minutes":600}
    stateLabels = ["unread_emails"]

    def main(self):
        """ Executes main functionality of logger app
        """
        self.startSamplingForEmails()

    def notify(self, notifyData):  
        """ Executes pop up notify with given data 
            notifyData: (string) data to show for user
        """ 
        subprocess.run(["notify", notifyData])

    def startSamplingForEmails(self):
        """ Starts polling for data 
        """
        for thread in self.threads:
            thread.start()

    def __init__(self, statsFilename="loggerStats.json"):
        """ Initializes object
            resultsFilename:    name of file that will be used as internal container for current results
        """
        self.mailbox = Mailbox()
        self.unreadEmailsNumber = 0
        self.threads = [threading.Thread(target=self.__samplingThread)]
        self.statsFilename = statsFilename
        self.__getPreviousStateFromFile()

    def __samplingThread(self):
        """ Thread polling for data from mailbox 
        """
        while True:
            time.sleep(Logger.delayIntervals["ten_seconds"])
            currentUnreadEmailsNr = self.mailbox.getUnreadMessagesNumber()

            if self.unreadEmailsNumber != currentUnreadEmailsNr:
                self.unreadEmailsNumber = currentUnreadEmailsNr
                self.__saveCurrentStateToFile()
                self.notify("new e-mail has benn received!")
                
    
    def __getPreviousStateFromFile(self):
        """ Gets current stats associated with unread data etc. from file 
        """
        readState = None

        if os.path.exists(self.statsFilename):
            with open(self.statsFilename,mode='r') as statsFile:
                readState = json.load(statsFile)

        if None != readState:
            self.unreadEmailsNumber = readState["unread_emails"]
    
    def __saveCurrentStateToFile(self):
        """ Saves current stats associated with unread data etc. into file 
        """
        currentState = {"unread_emails":self.unreadEmailsNumber}

        with open(self.statsFilename,mode='w') as statsFile:
            json.dump(currentState, statsFile)
