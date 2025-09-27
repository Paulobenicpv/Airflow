FROM apache/airflow:2.9.3
USER root
RUN pip install --no-cache-dir -r /requirements.txt
USER airflow
COPY dags /opt/airflow/dags
COPY plugins /opt/airflow/plugins
COPY include /opt/airflow/include