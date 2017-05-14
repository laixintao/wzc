FROM ubuntu
RUN sudo apt-get install phantomjs
RUN sudo apt-get install python
RUN pip install -r requirements.txt

