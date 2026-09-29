def test_health_is_public(api_client):
    r = api_client.get("/health")
    assert r.status_code == 200 and r.json()["documents"] >= 40


def test_ask_requires_api_key(api_client):
    assert api_client.post("/ask", json={"question": "What is AP-08?"}).status_code == 401


def test_ask_and_feedback(api_client):
    h = {"X-API-Key": "test-key"}
    r = api_client.post("/ask", json={"question": "Which API gateway product is the standard?"}, headers=h)
    body = r.json()
    assert r.status_code == 200 and body["found"] and body["citations"] and body["query_id"]
    f = api_client.post("/feedback", json={"query_id": body["query_id"], "correct": True}, headers=h)
    assert f.status_code == 200


def test_documents_endpoint(api_client):
    h = {"X-API-Key": "test-key"}
    adrs = api_client.get("/documents", params={"doc_type": "adr"}, headers=h).json()
    assert len(adrs) == 12 and all(d["doc_type"] == "adr" for d in adrs)
    assert api_client.get("/documents/STD-DB-006", headers=h).json()["owner"].startswith("Lena Vogel")
    assert api_client.get("/documents/NOPE", headers=h).status_code == 404


def test_rate_limit(api_client, monkeypatch):
    monkeypatch.setenv("EAKA_RATE_LIMIT_PER_MINUTE", "2")
    h = {"X-API-Key": "test-key"}
    codes = [api_client.get("/documents/AP-CATALOG", headers=h).status_code for _ in range(3)]
    assert codes == [200, 200, 429]
