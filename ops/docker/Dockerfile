FROM apache/airflow:2.9.3

USER root

# Copy and install Python requirements first (cache-friendly)
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Create working dirs
RUN mkdir -p /opt/airflow/dags /opt/airflow/plugins /opt/airflow/include /opt/airflow/dbt

# Copy project content
COPY dags /opt/airflow/dags
COPY plugins /opt/airflow/plugins
COPY include /opt/airflow/include
COPY dbt /opt/airflow/dbt

USER airflow