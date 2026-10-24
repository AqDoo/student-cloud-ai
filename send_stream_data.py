import csv
import random
import time
from datetime import datetime
from pathlib import Path

INPUT_DIR = Path(__file__).parent / "stream" / "input"
INPUT_DIR.mkdir(parents=True, exist_ok=True)

student_number = random.randint(1000, 9999)
attendance = random.randint(45, 100)
practice_score = random.randint(40, 100)
activity = random.randint(30, 100)
missed_tasks = random.randint(0, 10)

filename = f"student_{student_number}_{int(time.time())}.csv"
temporary_file = INPUT_DIR / f"{filename}.tmp"
final_file = INPUT_DIR / filename

with temporary_file.open("w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(
        [
            "student_id",
            "attendance",
            "practice_score",
            "activity",
            "missed_tasks",
        ]
    )
    writer.writerow(
        [
            f"ST{student_number}",
            attendance,
            practice_score,
            activity,
            missed_tasks,
        ]
    )

temporary_file.rename(final_file)

print("Новые данные отправлены в поток:")
print(f"Файл: {final_file}")
print(f"Время: {datetime.now():%H:%M:%S}")