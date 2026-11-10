import csv
import json
import os
import time
from collections import Counter
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "employees.csv"
OUTPUT_DIR = BASE_DIR / "output"
LOG_FILE = OUTPUT_DIR / "log.txt"

def setup_and_check():
    """1.1 Create output dir and check that the input file exists."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    if not DATA_FILE.exists():
        print(f"ERROR: input file not found: {DATA_FILE}")
        print("Put employees.csv into the 'data' folder next to hr_report.py.")
        return False
    print("Input file:", DATA_FILE.resolve())
    return True

def backup_file(src, dst):
    """1.2 Copy src to dst line by line, return number of lines copied."""
    count = 0
    with open(src, "r", encoding="utf-8", newline="") as fin, \
         open(dst, "w", encoding="utf-8", newline="") as fout:
        for line in fin:
            fout.write(line)
            count += 1
    return count

def log(message):
    """1.3 Append a timestamped line to output/log.txt."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().isoformat()} {message}\n")

def create_lock():
    """1.4 Create lock.txt in mode 'x'; do not stop if it already exists."""
    lock_path = OUTPUT_DIR / "lock.txt"
    try:
        with open(lock_path, "x", encoding="utf-8") as f:
            f.write(datetime.now().isoformat())
        print("Lock file created.")
    except FileExistsError:
        print("Report already created")

def part1():
    count = backup_file(DATA_FILE, OUTPUT_DIR / "employees_backup.csv")
    print("Backup lines:", count)
    log(f"backup created, {count} lines")
    create_lock()

def print_basic_info():
    """2.1 csv.reader: header, first 3 employees, record count."""
    with open(DATA_FILE, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)
    print("Header:", header)
    for row in rows[:3]:
        print(row)
    print("Records:", len(rows))

def analyze_csv():
    """2.2 csv.DictReader statistics. Returns data for later tasks."""
    dept_count = Counter()
    dept_total = Counter()
    active_employees = []
    active = 0
    inactive = 0

    with open(DATA_FILE, "r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            salary = int(row["salary"])
            dept = row["department"]
            dept_count[dept] += 1
            dept_total[dept] += salary
            if row["is_active"] == "True":
                active += 1
                active_employees.append(row)
            else:
                inactive += 1

    dept_stats = []
    for dept in dept_count:
        avg = round(dept_total[dept] / dept_count[dept], 2)
        dept_stats.append(
            {"department": dept, "employee_count": dept_count[dept], "avg_salary": avg}
        )
    dept_stats.sort(key=lambda d: d["avg_salary"], reverse=True)

    print("Employees per department:")
    for d in dept_stats:
        print(f"  {d['department']}: {d['employee_count']}")
    print("Average salary per department:")
    for d in dept_stats:
        print(f"  {d['department']}: {d['avg_salary']:.2f}")

    top3 = sorted(active_employees, key=lambda r: int(r["salary"]), reverse=True)[:3]
    print("Top 3 active by salary:")
    for r in top3:
        print(f"  {r['first_name']} {r['last_name']} {r['salary']}")

    print(f"Active: {active}, inactive: {inactive}")
    return dept_stats

def write_department_stats(dept_stats):
    """2.3 csv.DictWriter -> department_stats.csv (sorted by avg desc)."""
    path = OUTPUT_DIR / "department_stats.csv"
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["department", "employee_count", "avg_salary"]
        )
        writer.writeheader()
        writer.writerows(dept_stats)
    print("Written:", path.name)

def write_high_earners():
    """2.4 csv.writer + writerows -> high_earners.csv."""
    path = OUTPUT_DIR / "high_earners.csv"
    rows = []
    with open(DATA_FILE, "r", encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            salary = int(r["salary"])
            if r["is_active"] == "True" and salary >= 5000:
                full_name = f"{r['first_name']} {r['last_name']}"
                rows.append([r["id"], full_name, r["department"], salary])
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "full_name", "department", "salary"])
        writer.writerows(rows)
    print("High earners:", len(rows))

def part2():
    print_basic_info()
    dept_stats = analyze_csv()
    write_department_stats(dept_stats)
    write_high_earners()
    return dept_stats

def safe_read(path):
    """3.1 Read a text file, handling the two typical errors."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        log(f"safe_read: file not found: {path}")
        return ""
    except UnicodeDecodeError:
        log(f"safe_read: decode error, retrying with errors='replace': {path}")
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()

def test_safe_read():
    missing = OUTPUT_DIR / "missing.txt"
    broken = OUTPUT_DIR / "broken.txt"
    with open(broken, "wb") as f:
        f.write(bytes([99, 97, 102, 233, 32, 255]))
    print("missing.txt ->", repr(safe_read(missing)))
    print("broken.txt  ->", repr(safe_read(broken)))

def count_cities():
    """3.2 Counter over cities, top 3 printed and written to cities.txt."""
    cities = Counter()
    with open(DATA_FILE, "r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            cities[row["city"]] += 1
    top3 = cities.most_common(3)
    print("Top 3 cities:", ", ".join(f"{c} {n}" for c, n in top3))
    with open(OUTPUT_DIR / "cities.txt", "w", encoding="utf-8") as f:
        print("Top 3 cities:", file=f)
        for city, n in top3:
            print(f"{city} {n}", file=f)

def save_json_safe(data, path):
    """3.3 Write to a temp file first, then atomically replace the target."""
    path = Path(path)
    tmp_path = Path(str(path) + ".tmp")
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp_path, path)

def part3(dept_stats):
    test_safe_read()
    count_cities()
    save_json_safe(dept_stats, OUTPUT_DIR / "summary.json")
    print("Written: summary.json")

class Timer:
    """4.1 Context manager that measures elapsed time."""

    def __init__(self, name):
        self.name = name
        self.start = 0.0

    def __enter__(self):
        print(f"START {self.name}")
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        elapsed = time.perf_counter() - self.start
        if exc_type is not None:
            print(f"FAILED {self.name}: {exc_type.__name__}")
            return False
        print(f"FINISH {self.name} {elapsed:.4f} s")
        return False

def demo_timer_error():
    """4.2 Error inside the with-block must propagate."""
    try:
        with Timer("test"):
            1 / 0
    except ZeroDivisionError:
        print("ZeroDivisionError caught outside the with-block")

def main():
    if not setup_and_check():
        return
    log("program started")

    part1()
    log("part 1 finished")

    with Timer("CSV analysis"):
        dept_stats = part2()
    log("part 2 finished")

    part3(dept_stats)
    log("part 3 finished")

    demo_timer_error()
    log("program finished")

if __name__ == "__main__":
    main()


