def model(dbt, session):
    dbt.config(
        submission_method="serverless",
        gcs_bucket="dbt_python_tdunlap",
        location="us-west1b",
        materialized = "table"
    )

    orders_df = dbt.ref("stg_tpch_orders")

    df = orders_df.toPandas()    # in earlier versions

    df = session.createDataFrame(df)   # in earlier versions

    # return final dataset (PySpark DataFrame)
    return df