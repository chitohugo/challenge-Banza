class TestClients:
    def test_create_client(self, req):
        payload = {
            "first_name": "Kirby",
            "last_name": "Lucey",
            "email": "klucey7@theatlantic.com",
            "password": "eV6\"jv3Crtn{ukLg",
            "password_confirm": "eV6\"jv3Crtn{ukLg"
        }
        response = req.post("/api/clients/register", json=payload)

        assert response.status_code == 201
        assert response.json()['first_name'] == payload['first_name']
        assert response.json()['email'] == payload['email']

    def test_get_all_clients_(self, req, clients):
        response = req.get("/api/clients/")
        assert response.status_code == 200
        assert len(response.json()['clients']) == 2

    def test_retrieve_client(self, clients, req):
        id = clients[0].id
        response = req.get(f"/api/clients/{id}")

        assert response.status_code == 200
        assert response.json()['first_name'] == 'Kacie'
        assert response.json()['email'] == 'kkalewe0@nhs.uk'

    def test_delete_client(self, clients, req):
        id = clients[0].id
        response = req.delete(f"/api/clients/{id}")

        assert response.status_code == 204

    def test_added_client_to_category(self, clients, categories, req):
        id_client = str(clients[1].id)
        id_category = str(categories[2].id)
        payload = {
            "id_client": id_client,
            "id_category": id_category
        }
        response = req.post("/api/categories-clients/", json=payload)
        assert response.json()['id_client'] == str(clients[1].id)

        response = req.get(f"/api/clients/{id_client}")
        assert response.json()['categories'][0]['id'] == id_category

    def test_consult_client_with_accounts_categories(self, req, clients, categories_clients, accounts):
        response = req.get(f"/api/clients/{clients[1].id}")
        assert len(response.json()['accounts']) == 1
        assert len(response.json()['categories']) == 3

    def test_consult_balance_for_accounts(self, req, accounts):
        movements = [
            {
                "id_account": str(accounts[1].id),
                "amount": 2000000,
                "type": 2
            },
            {
                "id_account": str(accounts[1].id),
                "amount": 3000000,
                "type": 2
            },
            {
                "id_account": str(accounts[1].id),
                "amount": 1000000,
                "type": 1
            }
        ]
        for movement in movements:
            response = req.post("/api/movements/", json=movement)
            assert response.status_code == 201

        response = req.get("/api/accounts/balance/")
        assert response.json()[0]['balance'] == float(4000000)
