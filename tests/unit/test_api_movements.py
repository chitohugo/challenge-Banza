class TestMovements:
    def test_create_movements(self, req, accounts):
        id_account = str(accounts[1].id)

        payload = [
            {
                "id_account": id_account,
                "amount": 2000000,
                "type": 2
            },
            {
                "id_account": id_account,
                "amount": 3000000,
                "type": 2
            },
            {
                "id_account": id_account,
                "amount": 1000000,
                "type": 1
            }
        ]
        for data in payload:
            response = req.post("/api/movements/", json=data)
            assert response.status_code == 201

    def test_create_movement_egress_fail(self, req, accounts):
        id_account = str(accounts[1].id)

        payload = {
            "id_account": id_account,
            "amount": 2000000,
            "type": 1
        }
        response = req.post("/api/movements/", json=payload)

        assert response.status_code == 400
        assert response.json()['detail'] == "You don't have enough balance"

    def test_delete_movement(self, req, accounts):
        id_account = str(accounts[1].id)

        payload = {
            "id_account": id_account,
            "amount": 2000000,
            "type": 2
        }
        # Create a movement
        response = req.post("/api/movements/", json=payload)
        assert response.status_code == 201

        # Delete a movement
        id = response.json()['id']
        response = req.delete(f"/api/movements/{id}")
        assert response.status_code == 204

    def test_consult_movement(self, req, accounts):
        id_account = str(accounts[1].id)

        payload = {
            "id_account": id_account,
            "amount": 2000000,
            "type": 2
        }
        # Create a movement
        response = req.post("/api/movements/", json=payload)
        assert response.status_code == 201

        # Get a movement
        id = response.json()['id']
        response = req.get(f"/api/movements/{id}")
        assert response.status_code == 200
        assert response.json()['id_account'] == payload['id_account']
