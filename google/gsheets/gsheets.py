import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import gspread


class GSheet:

    """
    Class to convert the Google Sheets into Pandas.DataFrame
    """
    
    def __init__(self, credential_file):
        """
        @g_auth: google sheet authorization object
        """
        self.scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/spreadsheets.readonly']

        credentials = ServiceAccountCredentials.from_json_keyfile_name(credential_file,self.scope)
        self.g_auth = gspread.authorize(credentials)


    def convert_gsheets_to_dataframe(self, link: str,sheets_num: int) -> pd.DataFrame:
        """
        @link: link of the gsheets. Note: google sheets need to be public to access from google.auth
        @sheets_num: Sheets number of google sheets class
        return: DataFrame of google sheets
        """
        data = self.g_auth.open_by_url(link).get_worksheet(sheets_num).get_all_values()
        return pd.DataFrame.from_records(data[1:],columns=data[0])


    def upload_sheet(self, link: str, sheets_num: int, csv_path):
        """
        @link: link of the gsheets. Note: google sheets need to be public to access from google.auth
        @sheets_num: Sheets number of google sheets class
        """
        sheet_id = self.g_auth.open_by_url(link).id
        print(f'sheet id to which the csv file will uploaded is : {sheet_id}')
        with open(csv_path,'r') as content:
            self.g_auth.import_csv(sheet_id, content.read())