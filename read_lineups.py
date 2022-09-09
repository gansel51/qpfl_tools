import os
import pickle

# Gmail API utils
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# for encoding/decoding messages in base64
from base64 import urlsafe_b64decode, urlsafe_b64encode

# for dealing with attachement MIME types
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import guess_type as guess_mime_type

# Request all access (permission to read/send/receive emails, manage the inbox, and more)
SCOPES = ["https://mail.google.com/"]


class LineupGenerator:
    def __init__(self):
        self.service = self._authenticate_gmail()

    def _authenticate_gmail(self):
        creds = None
        # the file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first time
        if os.path.exists("credentials/token.pickle"):
            with open("credentials/token.pickle", "rb") as token:
                creds = pickle.load(token)
        # if there are no (valid) credentials availablle, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials/credentials.json", SCOPES)
                creds = flow.run_local_server(port=0)
            # save the credentials for the next run
            with open("credentials/token.pickle", "wb") as token:
                pickle.dump(creds, token)
        return build("gmail", "v1", credentials=creds)

    def search_messages(self, query: str) -> list:
        result = self.service.users().messages().list(userId="me", q=query).execute()
        messages = []
        if "messages" in result:
            messages.extend(result["messages"])
        while "nextPageToken" in result:
            page_token = result["nextPageToken"]
            result = self.service.users().messages().list(userId="me", q=query, pageToken=page_token).execute()
            if "messages" in result:
                messages.extend(result["messages"])
        return messages

    def get_size_format(self, b, factor=1024, suffix="B"):
        """
        Scale bytes to its proper byte format
        e.g:
            1253656 => '1.20MB'
            1253656678 => '1.17GB'
        """
        for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
            if b < factor:
                return f"{b:.2f}{unit}{suffix}"
            b /= factor
        return f"{b:.2f}Y{suffix}"

    def clean(self, text):
        # clean text for creating a folder
        return "".join(c if c.isalnum() else "_" for c in text)

    def parse_parts(self, parts, folder_name, message):
        """
        Utility function that parses the content of an email partition
        """
        if parts:
            for part in parts:
                filename = part.get("filename")
                mimeType = part.get("mimeType")
                body = part.get("body")
                data = body.get("data")
                file_size = body.get("size")
                part_headers = part.get("headers")
                if part.get("parts"):
                    # recursively call this function when we see that a part
                    # has parts inside
                    text = parse_parts(part.get("parts"), folder_name, message)
                if mimeType == "text/plain":
                    # if the email part is text plain
                    if data:
                        text = urlsafe_b64decode(data).decode()
                        return text

    def read_message(self, message):
        """
        This function takes Gmail API `service` and the given `message_id` and does the following:
            - Downloads the content of the email
            - Prints email basic information (To, From, Subject & Date) and plain/text parts
            - Creates a folder for each email based on the subject
            - Downloads text/html content (if available) and saves it under the folder created as index.html
            - Downloads any file that is attached to the email and saves it in the folder created
        """
        msg = self.service.users().messages().get(userId="me", id=message["id"], format="full").execute()
        # parts can be the message body, or attachments
        payload = msg["payload"]
        headers = payload.get("headers")
        parts = payload.get("parts")
        folder_name = "email"
        has_subject = False
        if headers:
            # this section prints email basic info & creates a folder for the email
            for header in headers:
                name = header.get("name")
                value = header.get("value")
                if name.lower() == "from":
                    # we print the From address
                    print("From:", value)
                if name.lower() == "to":
                    # we print the To address
                    print("To:", value)
                if name.lower() == "subject":
                    # make our boolean True, the email has "subject"
                    has_subject = True
                    # make a directory with the name of the subject
                    folder_name = self.clean(value)
                    # we will also handle emails with the same subject name
                    folder_counter = 0
                    while os.path.isdir(folder_name):
                        folder_counter += 1
                        # we have the same folder name, add a number next to it
                        if folder_name[-1].isdigit() and folder_name[-2] == "_":
                            folder_name = f"{folder_name[:-2]}_{folder_counter}"
                        elif folder_name[-2:].isdigit() and folder_name[-3] == "_":
                            folder_name = f"{folder_name[:-3]}_{folder_counter}"
                        else:
                            folder_name = f"{folder_name}_{folder_counter}"
                    os.mkdir(folder_name)
                    print("Subject:", value)
                if name.lower() == "date":
                    # we print the date when the message was sent
                    print("Date:", value)
        if not has_subject:
            # if the email does not have a subject, then make a folder with "email" name
            # since folders are created based on subjects
            if not os.path.isdir(folder_name):
                os.mkdir(folder_name)
        text = self.parse_parts(parts, folder_name, message)
        return text

    def _format_lineup(self, lineup):
        formatted_lineup = list(lineup.split("\r\n"))
        return formatted_lineup

    def controller(self):
        # get emails that match the query you specify
        results = self.search_messages(query="Lineup Week 1")
        print(f"Found {len(results)} results.")
        # for each email matched, read it (output plain/text to console & save HTML and attachments)
        lineups = []
        for msg in results:
            lineup = self.read_message(msg)
            formatted_lineup = self._format_lineup(lineup)
            lineups.append(formatted_lineup)
        return lineups


if __name__ == "__main__":
    LG = LineupGenerator()
    lineups = LG.controller()
