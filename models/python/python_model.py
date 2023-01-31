#def is_holiday(date_col):
#    french_holidays = holidays.France()
#    is_holiday = (date_col in french_holidays)
#    return is_holiday

def model(dbt, session):
    dbt.config(
        submission_method="serverless",
        gcs_bucket="dbt_python_tdunlap",
        dataproc_region="us-west1",
        location="us-west1b",
        materialized = "table"
    )

    orders_df = dbt.ref("stg_tpch_orders")

    # df = orders_df.to_pandas_on_spark()  # Spark 3.2+
    df = orders_df.toPandas()    # in earlier versions
    # df = df.columns.str.lower()

    # apply our function
    #df["is_holiday"] = df["order_date"].apply(is_holiday)

    # convert back to PySpark
    # df = df.to_spark()               # Spark 3.2+
    df = session.createDataFrame(df)   # in earlier versions

    # return final dataset (PySpark DataFrame)
    return df