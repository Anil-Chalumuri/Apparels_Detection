FROM continuumio/anaconda3:4.4.0
#COPY . /usr/app/
#COPY . /todo
ADD . /todo
#EXPOSE 8000
#WORKDIR /usr/app/
WORKDIR /todo
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
#CMD python main.py
#CMD uvicorn main:app
EXPOSE 5000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
#uvicorn main:app --reload
#COPY . .

#ENV FLASK_APP=clientApp.py

#CMD flask run  --host=0.0.0.0



