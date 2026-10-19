from fastapi.testclient import TestClient
from resilitwin.api import app

client = TestClient(app)

def test_health_and_dashboard():
    assert client.get('/api/health').json()['status'] == 'ok'
    page = client.get('/')
    assert page.status_code == 200
    assert 'ResiliTwin' in page.text

def test_catalog_and_forecasts():
    overview = client.get('/api/overview')
    assert overview.status_code == 200
    assert overview.json()['history_rows'] > 1000
    fc = client.get('/api/forecasts', params={'sku': 'SOLAR'}).json()['forecasts']
    assert len(fc) == 21
    assert client.get('/api/forecasts',params={'sku':'UNKNOWN'}).status_code == 404

def test_invalid_scenario_rejected():
    response = client.post('/api/scenarios', json={'demand_shock_pct': 9999})
    assert response.status_code == 422

def test_unknown_supplier_is_error_not_server_exception():
    # Unknown suppliers currently require explicit domain validation.
    assert client.post('/api/scenarios', json={'outages':['BAD']}).status_code == 422

def test_evidence_endpoint():
    r = client.get('/api/evidence', params={'query':'carbon emissions'})
    assert r.status_code == 200
    assert len(r.json()['documents']) >= 1
