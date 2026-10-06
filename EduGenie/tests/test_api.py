from fastapi.testclient import TestClient
from app.main import app, service
client=TestClient(app)
def test_health():
    r=client.get('/api/health'); assert r.status_code==200; assert r.json()['status']=='ok'
def test_qna(monkeypatch):
    monkeypatch.setattr(service,'qna',lambda question:'Mock answer'); r=client.post('/api/qna',json={'question':'What is AI?'}); assert r.status_code==200; assert r.json()['result']=='Mock answer'
def test_explain(monkeypatch):
    monkeypatch.setattr(service,'explain',lambda topic:'Mock explanation'); assert client.post('/api/explain',json={'topic':'Photosynthesis'}).status_code==200
def test_summary(monkeypatch):
    monkeypatch.setattr(service,'summarize',lambda text:'Mock summary'); r=client.post('/api/summarize',json={'text':'Long text'}); assert r.status_code==200
def test_quiz(monkeypatch):
    q=[{'question':'2+2?','options':['1','2','3','4'],'correct_answer':'4','explanation':'Arithmetic.'},{'question':'Capital of France?','options':['Paris','Rome','Delhi','Berlin'],'correct_answer':'Paris','explanation':'Paris.'},{'question':'Water formula?','options':['CO2','H2O','O2','NaCl'],'correct_answer':'H2O','explanation':'Water.'}]
    monkeypatch.setattr(service,'quiz',lambda text:{'questions':q}); r=client.post('/api/quiz',json={'text':'science'}); assert r.status_code==200; assert len(r.json()['questions'])==3
def test_learning(monkeypatch):
    monkeypatch.setattr(service,'learning_path',lambda topic:'Beginner -> Advanced'); r=client.post('/api/learn/recommendations',json={'topic':'SQL'}); assert r.status_code==200
def test_validation(): assert client.post('/api/qna',json={'question':''}).status_code==422
