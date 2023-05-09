# import packages first 
import random
import pandas

# all python models need to be defined at the start with this specific syntax
# dbt: A class compiled by dbt Core, unique to each model, enables you to run your Python code in the context of your dbt project and DAG.
# session: A class representing your data platform’s connection to the Python backend. The session is needed to read in tables as DataFrames, and to write DataFrames back to tables.
def model(dbt, session):

    # setting configuration - can also configure in dbt_project.yml or in models.yml file
    # be sure to materialize python models as tables, and to specify the packages that were imported above
    dbt.config(
        submission_method="serverless",
        gcs_bucket="dbt_python_tdunlap",
        dataproc_region="us-west1",
        location="us-west1b",
        materialized = "table", 
        packages=['pandas', 'random']
    )

    # python models don't use Jinja. Here we are using dbt.ref to create model references and pushing it to a pandas df 
    my_sql_model = dbt.ref("my_first_dbt_model")

    my_sql_model_df = my_sql_model.toPandas() 
    
    # creating a basic list to use for random colum rand
    num_list = [1, 2, 3, 4, 5]

    # adding a new column which will have a rand number picked from the list
    my_sql_model_df['new_column_rand'] = [random.choice(num_list) for row in my_sql_model_df.index]

    # renaming my model and ordering by the random added column
    final_df = my_sql_model_df.sort_values(by=['new_column_rand'])

    # in dbt, you always need to return your data frame at the end of your models
    return final_df