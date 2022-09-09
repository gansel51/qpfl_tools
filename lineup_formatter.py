"""
Class to format lineups in Google Drive
"""
import os
import pickle

from read_lineups import LineupGenerator

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# TODO: Check scopes in Google Cloud project
SCOPES = ["https://www.googleapis.com/auth/drive"]


class FormatLineups:
    def __init__(self):
        self.lineups = LineupGenerator().controller()
        self.creds = None
        self.service = self._authenticate()
        self.spreadsheet_id = "1wSSo2Tbjha7bXI_jtVTMisbJXfWGBQbFF8hDB5JLngg"

    def _authenticate(self):
        # the file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first time
        if os.path.exists("credentials/token.pickle"):
            with open("credentials/token.pickle", "rb") as token:
                self.creds = pickle.load(token)
        # if there are no (valid) credentials availablle, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials/credentials.json", SCOPES)
                self.creds = flow.run_local_server(port=0)
            # save the credentials for the next run
            with open("credentials/token.pickle", "wb") as token:
                pickle.dump(self.creds, token)
        return build("sheets", "v4", credentials=self.creds)

    def _bold_lineups(self):
        pass

    def _read_lineup(self):
        # The A1 notation of the values to retrieve.
        range_ = "A:T"

        request = (
            self.service.spreadsheets()
            .values()
            .get(
                spreadsheetId=self.spreadsheet_id,
                range=range_,
            )
        )
        response = request.execute()
        return response

    def _conditional_formatting(spreadsheet_id):
        """
        Creates the batch_update the user has access to.
        Load pre-authorized user credentials from the environment.
        for guides on implementing OAuth2 for the application.
        """
        try:
            my_range = {
                "sheetId": 0,
                "startRowIndex": 1,
                "endRowIndex": 11,
                "startColumnIndex": 0,
                "endColumnIndex": 4,
            }
            requests = [
                {
                    "addConditionalFormatRule": {
                        "rule": {
                            "ranges": [my_range],
                            "booleanRule": {
                                "condition": {
                                    "type": "CUSTOM_FORMULA",
                                    "values": [{"userEnteredValue": "=GT($D2,median($D$2:$D$11))"}],
                                },
                                "format": {"textFormat": {"foregroundColor": {"red": 0.8}}},
                            },
                        },
                        "index": 0,
                    }
                },
                {
                    "addConditionalFormatRule": {
                        "rule": {
                            "ranges": [my_range],
                            "booleanRule": {
                                "condition": {
                                    "type": "CUSTOM_FORMULA",
                                    "values": [{"userEnteredValue": "=LT($D2,median($D$2:$D$11))"}],
                                },
                                "format": {"backgroundColor": {"red": 1, "green": 0.4, "blue": 0.4}},
                            },
                        },
                        "index": 0,
                    }
                },
            ]
            body = {"requests": requests}
            response = self.service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
            print(f"{(len(response.get('replies')))} cells updated.")
            return response

        except HttpError as error:
            print(f"An error occurred: {error}")
            return error


if __name__ == "__main__":
    FL = FormatLineups()
    lineups = FL._read_lineup()
    # FL.conditional_formatting("1CM29gwKIzeXsAppeNwrc8lbYaVMmUclprLuLYuHog4k")
