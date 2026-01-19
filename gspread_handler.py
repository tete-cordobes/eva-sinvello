import os
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# Configuración de gspread
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# Usa variable de entorno para la ruta del service account
service_account_path = os.getenv('GOOGLE_SERVICE_ACCOUNT_PATH', 'proyecto-eva-service-account.json')
creds = Credentials.from_service_account_file(service_account_path, scopes=scope)
client = gspread.authorize(creds)

# ID del spreadsheet - considera moverlo a variable de entorno también
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID', '1qWlfX_inOnDdK5GtJzX3n_0dutbnEYssEjuR9yudN-o')
sheet = client.open_by_key(SPREADSHEET_ID).sheet1

def save_to_sheet(thread_id, question, response):
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([thread_id, question, response, date_time])
