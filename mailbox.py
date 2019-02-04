from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class Mailbox:
    gmailLabels = ['CATEGORY_PERSONAL', 'CATEGORY_SOCIAL', 'IMPORTANT', 'CATEGORY_UPDATES','INBOX','UNREAD','TRASH','SPAM']
    
    def __init__(self):
        """ Authenitaces the mailbox, checks for credentials and requests for login if required \
            Also starts the service if credentials are satisfied \
        """
        self.credentials = None
        self.service = None
        self.__getCredentials()
        self.__getService()


    def __getCredentials(self):
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.credentials = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.credentials = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.credentials, token)
        
    
    def __getService(self):
        """ Gets service associated with credentails file """
        self.service =  build('gmail', 'v1', credentials=self.credentials)

    def test(self):
        """ Simple test of class. Used for purpose of debugging 
        """
        # Call the Gmail API
        # results = self.service.users().labels().list(userId='me', q="").execute()
        labels_info = self.service.users().labels().get(userId='me', id='UNREAD').execute()
        # labels_unread = labels_info.get('messagesUnread', [])
        print(str(labels_info["messagesUnread"]))
        # if not labels_unread:
        #     print("there's no labels")
        # else:
        #     for label in labels_unread:
        #         print(label)
        # Turning on notifications about new e-mails
        # results = self.service.users().messages().list(userId='me', q="category:primary is:unread").execute()
        # messages = results.get('messages', [])

        # if not messages:
        #     print('No messages found.')
        # else:
        #     print('Number of unread messages in mailbox:', len(messages))
            # for message in messages:
                # for key in message.values():
                    # print(key)

    def getUnreadMessagesNumber(self):
        """ Returns the number of unread messages

            return:         The number of unread messages       
        """
        unreadLabelInfo = self.service.users().labels().get(userId='me', id='UNREAD').execute()   
        return unreadLabelInfo["messagesUnread"]

    def getMessageSender(self, id):
        """ Obtains the sender of message's id

            id: id of the message

            return: string containing sender's name
        """
        