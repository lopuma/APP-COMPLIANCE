# Slim version of Python
FROM python:3.8.12-slim

RUN yum update

# Install Tkinter
RUN yum install tk

# Commands to run Tkinter application
CMD ["/Alvaro/Desarrollo/APPCompliance/Compliance.py"]
ENTRYPOINT ["python3"]
