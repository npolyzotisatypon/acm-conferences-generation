FROM python:2-alpine

RUN mkdir -p /generation/conf-acm
RUN mkdir -p /generation/template_do
RUN mkdir -p /generation/template_do 
RUN mkdir -p /generation/templates
COPY *.py conf-acm.csv requirements.txt /generation/
ADD conf-acm /generation/conf-acm 
ADD  template_do  /generation/template_do
ADD  templates  /generation/templates

RUN cd generation && pip install -r requirements.txt
WORKDIR /generation
CMD ["python","main.py"]