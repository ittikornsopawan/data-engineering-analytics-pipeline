# World Cup Data Lab

**AI Engineer Learning Series — Part 1: Data Analysis Foundation**:

Project สำหรับฝึก Python, NumPy, Pandas, Matplotlib, PostgreSQL และ Docker โดยใช้ข้อมูล FIFA World Cup เป็น dataset หลัก

Download Data: [File](https://www.kaggle.com/datasets/piterfm/fifa-football-world-cup/data)

## Project Structure

```text
├── README.md
├── data
│   ├── fifa_ranking_2022-10-06.csv
│   ├── fifa_ranking_2026-06-08.csv
│   ├── matches_1930_2022.csv
│   ├── schedule_2026.csv
│   └── world_cup.csv
├── docker-compose.yml
├── main.py
├── notebook
│   ├── 01_explore_matches.ipynb
│   ├── 02_matches_statics.ipynb
│   ├── 03_matches_all_time.ipynb
│   ├── 04_matches_year_summary.ipynb
│   ├── 05_matches_goals_summary.ipynb
│   └── 06_team_rank_vs_winner.ipynb
├── output
├── requirements.txt
└── src
    ├── __init__.py
    ├── config.py
    ├── database.py
    ├── extract.py
    ├── load.py
    └── transform.py
```

## Step 1: Create Virtual Environment

สร้าง virtual environment สำหรับ project นี้

```bash
python3 -m venv .venv
```

Activate environment

```bash
source .venv/bin/activate
```

ตรวจสอบ Python version

```bash
python --version
```

## Step 2: Create requirements.txt

สร้างไฟล์ `requirements.txt` ที่ root project

```txt
numpy>=2.3
pandas>=2.3.3
matplotlib
jupyterlab
ipykernel
sqlalchemy
psycopg[binary]
python-dotenv
```

สร้างไฟล์ `.env.example` ที่ root project เพื่อเก็บตัวอย่าง database connection string

```env
DATABASE_URL=postgresql+psycopg://worldcup:worldcup@localhost:5432/worldcup_db
```

## Step 3: Install Dependencies

ติดตั้ง package ทั้งหมดจาก `requirements.txt`

```bash
python -m pip install -r requirements.txt
```

ตรวจสอบว่า package หลักใช้งานได้

```bash
python -c "import pandas as pd; import numpy as np; import matplotlib.pyplot as plt; print('OK')"
```

ถ้าขึ้น `OK` แปลว่า setup สำเร็จ

## Step 4: Setup PostgreSQL with Docker

Project นี้ใช้ PostgreSQL เพื่อฝึก workflow แบบใกล้เคียงงานจริงมากขึ้น จากเดิมที่อ่านข้อมูลจาก CSV อย่างเดียว จะต่อยอดเป็นการ load CSV เข้า database แล้วใช้ Pandas อ่านข้อมูลจาก PostgreSQL

สร้างไฟล์ `docker-compose.yml` ที่ root project

```yaml
services:
  postgres:
    image: postgres:16
    container_name: world-cup-postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: worldcup
      POSTGRES_PASSWORD: worldcup
      POSTGRES_DB: worldcup_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

เริ่ม PostgreSQL container

```bash
docker compose up -d
```

ตรวจสอบ container

```bash
docker compose ps
```

ทดสอบเข้า PostgreSQL container

```bash
docker exec -it world-cup-postgres psql -U worldcup -d worldcup_db
```

ถ้าเข้าได้จะเห็น prompt ประมาณนี้

```text
worldcup_db=#
```

ออกจาก `psql`

```sql
\q
```

หยุด container

```bash
docker compose down
```

ถ้าต้องการลบ database volume ด้วย

```bash
docker compose down -v
```

Database connection string ที่จะใช้ใน Python

```text
postgresql+psycopg://worldcup:worldcup@localhost:5432/worldcup_db
```

## Step 5: Register Jupyter Kernel

สร้าง kernel สำหรับ project นี้ เพื่อให้ Jupyter Notebook ใช้ Python จาก `.venv`

```bash
python -m ipykernel install --user --name world-cup-data-lab --display-name "Python (World Cup Data Lab)"
```

เวลาเปิด notebook ให้เลือก kernel:

```text
Python (World Cup Data Lab)
```

## Step 6: Start JupyterLab

เปิด JupyterLab

```bash
jupyter lab
```

จากนั้นสร้าง notebook แรกใน folder `notebook`

```text
notebook/01_explore_matches.ipynb
```

## Step 7: First Notebook Setup

ใน Part แรกจะเริ่มจากอ่าน CSV ก่อน เพื่อฝึก Pandas พื้นฐาน จากนั้นค่อยเพิ่ม step สำหรับ load CSV เข้า PostgreSQL

ใน notebook แรก ให้เริ่มจาก import library

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
```

อ่านไฟล์ match dataset

```python
matches_path = "../data/matches_1930_2022.csv"

df = pd.read_csv(matches_path)
```

ดูข้อมูลเบื้องต้น

```python
df.head()
```

```python
df.shape
```

```python
df.columns.tolist()
```

```python
df.info()
```

```python
df.isna().sum()
```

## Step 8: Source Code Structure

Project นี้แยก logic หลักออกจาก notebook เพื่อให้สามารถนำ code ไปใช้ซ้ำใน pipeline ได้

```text
src
├── __init__.py
├── config.py
├── database.py
├── extract.py
├── load.py
└── transform.py
```

ความหมายของแต่ละไฟล์

```text
config.py    เก็บ path และ environment configuration
database.py  สร้าง database engine สำหรับเชื่อมต่อ PostgreSQL
extract.py   อ่านข้อมูลจาก CSV
transform.py แปลงข้อมูลและสร้าง analytical tables
load.py      load DataFrame เข้า PostgreSQL
```

ตัวอย่างการ run pipeline

```bash
python main.py
```

## Current Learning Goal

เป้าหมายของ project นี้คือฝึก workflow พื้นฐานของ Data Engineering และ AI Engineer Foundation ผ่านข้อมูล FIFA World Cup ตั้งแต่การอ่าน raw CSV, วิเคราะห์ข้อมูลด้วย notebook, แปลงข้อมูลด้วย Pandas, load เข้า PostgreSQL และสร้าง visualization เบื้องต้น

สิ่งที่ project นี้ทำได้แล้ว:

1. อ่านข้อมูลจาก `matches_1930_2022.csv` และ `world_cup.csv`
2. สำรวจข้อมูลเบื้องต้นด้วย Jupyter Notebook
3. แปลงข้อมูลจาก match-level เป็น team-level
4. สร้าง summary table รายทีม รายปี และ all-time
5. สร้าง match goals summary
6. วิเคราะห์ ranking ของทีมเทียบกับทีมที่ได้แชมป์จริง
7. จัดการ edge case ของ World Cup 1950 ที่ไม่มี Final match แบบปกติ
8. สร้าง visualization สำหรับจำนวนแชมป์ของแต่ละประเทศ
9. Load raw และ transformed tables เข้า PostgreSQL

## Notebooks

```text
01_explore_matches.ipynb        สำรวจ dataset เบื้องต้น
02_matches_statics.ipynb        วิเคราะห์ match statistics พื้นฐาน
03_matches_all_time.ipynb       สร้าง team summary แบบ all-time
04_matches_year_summary.ipynb   สร้าง summary รายปีของ World Cup
05_matches_goals_summary.ipynb  สร้าง match goals summary
06_team_performance.ipynb       วิเคราะห์ team champion
```

## Generated Tables

ตารางหลักที่สร้างจาก pipeline / notebook:

```text
raw_matches
team_matches
team_summary_by_year
team_summary_all_time
world_cup_year_summary
match_goals_summary
team_ranking_by_year
champion_count
```

## Project Scope

Project นี้เป็น portfolio project สำหรับฝึกพื้นฐาน Data Engineering และ AI Engineer Foundation โดยเน้น:

- Python data processing
- Pandas transformation
- PostgreSQL loading
- Docker-based local database
- Jupyter Notebook analysis
- Matplotlib visualization
- Data quality thinking and edge-case handling
