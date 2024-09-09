# Imports
import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

def create_dataframe(filepath, format, spark):
    """
    Create a spark df given a filepath and format.

    :param filepath: <str>, the filepath
    :param format: <str>, the file format (e.g. "csv" or "json")
    :param spark: <str> the spark session

    :return: the spark df uploaded
    """
    
    #Load data into dataframe
    spark_df = spark.read.load(filepath, format = format, \
    header = 'true', inferSchema = 'true')

    return spark_df
    
def transform_nhis_data(nhis_df):
    """   
    Transform df elements

    :param nhis_df: spark df
    
    :return: spark df, transformed df
    """   

    #Transform by: (1) dropping null values,
    #(2) grouping by age (note: min age found in nhis data was 18), 
    #(3) flattening hispanic ethnicity into race column, 
    #(4) modifying race indexes, (5) renaming columns
    transformed_df = nhis_df.dropna(how = 'any')\
    .withColumn('AGE_P', floor(abs(nhis_df.AGE_P-20)/5 + 1))\
    .withColumn('MRACBPI2', when(nhis_df.HISPAN_I < 12, 5)\
    .when((nhis_df.MRACBPI2 == 6) | (nhis_df.MRACBPI2 == 7) | (nhis_df.MRACBPI2 == 12), 3)\
    .when(nhis_df.MRACBPI2 == 3, 4)\
    .when((nhis_df.MRACBPI2 == 16) | (nhis_df.MRACBPI2 == 17), 6)\
    .otherwise(nhis_df.MRACBPI2)).drop('HISPAN_I')\
    .withColumnRenamed('AGE_P', '_AGEG5YR').withColumnRenamed('MRACBPI2', '_IMPRACE')

    return transformed_df

def join_dfs(nhis_df, brfss_df):
     """
     Join two dataframes with respect to common columns

     :param nhis_df: processed spark df of nhis data
     :param brfss_df: spark df of brfss data

     :return: joined_df, the joined df
     """

     brfss_df.dropna(how = 'any')
     joined_df = brfss_df.join(nhis_df, ['SEX', '_AGEG5YR', '_IMPRACE'])

     return(joined_df)

def report_summary_stats(joined_df):
    """
    Calculate prevalence statistics

    :param joined_df: the joined df

    :return: None
    """   
    summary_df1 = joined_df.crosstab("SEX", "DIBEV1")\
    .write.format('csv').option('header', True).mode('overwrite')\
    .save("Sex_Diabetes")
    
    summary_df2 = joined_df.crosstab("_AGEG5YR", "DIBEV1")\
    .write.format('csv').option('header', True).mode('overwrite')\
    .save("Age_Diabetes")
    
    summary_df3 = joined_df.crosstab("_IMPRACE", "DIBEV1")\
    .write.format('csv').option('header', True).mode('overwrite')\
    .save("Race_Diabetes")

def main():
     """
     Main function
     
     :param brfss_file_arg: brfss file path
     :param nhis_file_arg: nhis file path
     :param save_output_arg: T/F save output file
     :param output_filename_arg: output (joined_df) file path
     
     :return: None
     """

     #Send both files to create dataframes
     format_brfss = brfss_file_arg.split(".")[1]
     format_nhis = nhis_file_arg.split(".")[1]
     brfss_df = create_dataframe(brfss_file_arg, format_brfss, spark)
     nhis_df = create_dataframe(nhis_file_arg, format_nhis, spark)

     #Transform nhis data
     nhis_df = transform_nhis_data(nhis_df) 

     #Use nhis data to predict diabetes diagnoses in brfss population
     joined_df = join_dfs(nhis_df, brfss_df)

     #Calculate statistics
     report_summary_stats(joined_df)  

     #Save joined_df
     if save_output_arg == "True":
         joined_df = joined_df.coalesce(1)\
         .write.format('csv').option('header', True).mode('overwrite')\
         .save(output_filename_arg)

if __name__ == '__main__':

    brfss_file_arg = sys.argv[1]
    nhis_file_arg = sys.argv[2]
    save_output_arg = sys.argv[3]
    if save_output_arg == "True":
        output_filename_arg = sys.argv[4]
    else:
        output_filename_arg = None



    # Start spark session
    spark = SparkSession.builder.getOrCreate()
    main()
    # Stop spark session 
    spark.stop()
