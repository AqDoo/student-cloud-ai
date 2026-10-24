from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    concat,
    lit,
    lpad,
    pmod,
    when,
)

spark = (
    SparkSession.builder
    .master("local[*]")
    .appName("StudentStreamingAnalytics")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

# Spark создаёт по одной новой записи каждые 3 секунды
stream = (
    spark.readStream
    .format("rate")
    .option("rowsPerSecond", 1)
    .load()
)

students = (
    stream
    .withColumn(
        "student_id",
        concat(
            lit("ST"),
            lpad((col("value") + 1000).cast("string"), 4, "0")
        )
    )
    .withColumn(
        "attendance",
        (pmod(col("value") * 7, lit(56)) + 45).cast("double")
    )
    .withColumn(
        "practice_score",
        (pmod(col("value") * 11, lit(61)) + 40).cast("double")
    )
    .withColumn(
        "activity",
        (pmod(col("value") * 13, lit(71)) + 30).cast("double")
    )
    .withColumn(
        "missed_tasks",
        pmod(col("value"), lit(11)).cast("integer")
    )
)

predictions = (
    students
    .withColumn(
        "risk_score",
        (
            (100 - col("attendance")) * 0.35
            + (100 - col("practice_score")) * 0.35
            + (100 - col("activity")) * 0.15
            + col("missed_tasks") * 3
        ).cast("double")
    )
    .withColumn(
        "predicted_risk",
        when(col("risk_score") >= 40, "Жоғары")
        .when(col("risk_score") >= 22, "Орташа")
        .otherwise("Төмен")
    )
    .select(
        col("timestamp").alias("processed_at"),
        "student_id",
        "attendance",
        "practice_score",
        "activity",
        "missed_tasks",
        "risk_score",
        "predicted_risk",
    )
)

query = (
    predictions.writeStream
    .format("console")
    .outputMode("append")
    .option("truncate", False)
    .option("numRows", 20)
    .trigger(processingTime="3 seconds")
    .start()
)

print("Потоковая обработка запущена")
print("Каждые 3 секунды поступают новые данные студентов")
print("Для остановки нажмите Ctrl+C")

try:
    query.awaitTermination()
except KeyboardInterrupt:
    print("\nПотоковая обработка остановлена")
    query.stop()
    spark.stop()