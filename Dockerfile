FROM python:3.9

WORKDIR /app

COPY . .

RUN pip install streamlit fpdf spacy && python -m spacy download en_core_web_sm

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]