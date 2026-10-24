# Student Cloud AI Analytics

**Жоба тақырыбы:** «Бұлттық ортада жасанды интеллект көмегімен студенттердің үлгерімін талдау және болжау жүйесі».

Бұл — №13 «Үлкен мәліметтерді автоматты талдау қызметі» тақырыбына арналған оқу жобасы. Қолданба CSV деректерін пакетпен өңдейді, аналитика мен визуализация жасайды, машиналық оқыту арқылы студенттің тәуекел деңгейін болжайды және API арқылы нәтиже береді.

## PyCharm арқылы іске қосу

1. `student-cloud-ai` бумасын PyCharm-да ашыңыз.
2. Python 3.11 немесе 3.12 виртуалды ортасын жасаңыз.
3. PyCharm Terminal ішінде орындаңыз:

```bash
pip install -r requirements.txt
python generate_data.py
streamlit run app.py
```

Браузерде `http://localhost:8501` ашылады.

## API іске қосу

```bash
uvicorn api:app --reload
```

API құжаттамасы: `http://127.0.0.1:8000/docs`.

## Docker арқылы іске қосу

```bash
docker build -t student-cloud-ai .
docker run --rm -p 8501:8501 student-cloud-ai
```

## CSV форматы

Міндетті бағандар:

- `student_id`
- `attendance`
- `practice_score`
- `activity`
- `missed_tasks`
- `final_score`
- `risk_level`

## Келесі кезеңдер

- PySpark Structured Streaming арқылы ағынды өңдеу;
- BigQuery Sandbox-пен бұлттық сақтау және сұраныстар;
- Streamlit Community Cloud-та жариялау;
- архитектуралық схема, презентация және қорғау мәтіні.
