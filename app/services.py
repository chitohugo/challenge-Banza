import requests


class CustomRequest:
    @classmethod
    def get(cls):
        url = "https://www.dolarsi.com/api/api.php?type=valoresprincipales"
        try:
            response = requests.get(url)
        except requests.exceptions.RequestException as error:
            print(error)
            raise

        return response


class APIDollar:
    def __init__(self, response):
        self.response = response

    def get_price(self):
        if self.response.status_code == 200:
            for item in self.response.json():
                if item['casa']['nombre'] == 'Dolar Bolsa':
                    return float(item['casa']['compra'].replace(",", "."))