from datetime import datetime

from fastapi.testclient import TestClient
from starlette import status

from app.db.models import Record
from app.tests.integration.conftest import reverse


class TestLicenseUseCase:

    def test_get_all_records(self, client: TestClient, db_session):
        record1 = Record(date=datetime.now().date(),
                        country="Argentina",
                        deaths=1,
                        recoveries=10,
                        cases=100)

        record2 = Record(date=datetime.now().date(),
                         country="Brasil",
                         deaths=10,
                         recoveries=100,
                         cases=1000)

        db_session.add_all([record1, record2])
        db_session.commit()

        url = reverse("record-get-all")
        response = client.get(url)
        result = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert len(result) == 2
        for element in result:
            assert element['id'] is not None
            assert element['country'] is not None
            assert element['deaths'] is not None
            assert element['recoveries'] is not None
            assert element['cases'] is not None
