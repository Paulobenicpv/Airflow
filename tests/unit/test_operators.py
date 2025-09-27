from plugins.operators.dbt_operator import DbtRunOperator

def test_dbt_operator_init():
    op = DbtRunOperator(task_id="dbt", project_dir="/tmp/project")
    assert op.project_dir == "/tmp/project"