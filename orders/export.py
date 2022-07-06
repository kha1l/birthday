import requests
import fake_useragent
from datetime import date
from postgres.psql import Database
from bs4 import BeautifulSoup


class DataExportDay:

    def __init__(self, date_end: date, name: str):
        db = Database()
        data = db.get_data(name)
        self.name = name
        self.rest = data[0]
        self.uuid = data[2]
        self.date_end = date_end
        self.login = data[3]
        self.password = data[4]
        self.code = data[5]
        self.session = None
        self.user = None
        self.header = None
        self.auth()

    def auth(self):
        self.session = requests.Session()
        self.user = fake_useragent.UserAgent().random
        log_data = {
            'CountryCode': self.code,
            'login': self.login,
            'password': self.password
        }
        self.header = {
            'user-agent': self.user
        }
        log_link = f'https://auth.dodopizza.{self.code}/Authenticate/LogOn'
        self.session.post(log_link, data=log_data, headers=self.header)

    def birthday(self):
        data_link = f'https://officemanager.dodopizza.{self.code}/OfficeManager/EmployeeList/EmployeeBirthdaysPartial?unitId=' \
                    + str(self.rest) + '&employeeName=&'
        response_data = self.session.get(data_link, headers=self.header)
        soup = BeautifulSoup(response_data.text, 'html.parser')
        finds = soup.find_all("tr", class_="b-table__row")
        worker = []
        person = []
        if len(finds) == 1:
            pass
        else:
            for i in range(1, len(finds)):
                finds_1 = finds[i].find_all("td", class_="b-table__col")
                for find_1 in finds_1:
                    person.append(find_1.text)
                    if len(person) == 3:
                        worker.append(person.copy())
                        person.clear()
        self.session.close()
        return worker
