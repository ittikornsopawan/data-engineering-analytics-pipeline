# World Cup Data Lab

**AI Engineer Learning Series — Part 1: Data Analysis Foundation**:

Project สำหรับฝึก Python, NumPy, Pandas, Matplotlib, PostgreSQL และ Docker โดยใช้ข้อมูล FIFA World Cup เป็น dataset หลัก

Download Data: [File](https://www.kaggle.com/datasets/piterfm/fifa-football-world-cup/data)

## Project Structure

```text
├── README.md
├── requirements.txt
├── docker-compose.yml
├── .env.example
├── data
│   ├── fifa_ranking_2022-10-06.csv
│   ├── fifa_ranking_2026-06-08.csv
│   ├── matches_1930_2022.csv
│   ├── schedule_2026.csv
│   └── world_cup.csv
├── notebook
├── output
└── src
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

## Step 8: Optional Source Code Structure

ถ้าต้องการแยก code ที่ใช้ซ้ำออกจาก notebook ให้สร้างไฟล์ใน `src`

```text
src
├── __init__.py
├── config.py
├── data_loader.py
└── display.py
```

ตัวอย่างการใช้ใน notebook

```python
import sys
from pathlib import Path

PROJECT_ROOT = Path.cwd().parent
sys.path.append(str(PROJECT_ROOT))
```

```python
from src.data_loader import load_matches
from src.display import setup_display

setup_display()
df = load_matches()
df.head()
```

## Current Learning Goal

เป้าหมายแรกของ project นี้คือทำความเข้าใจข้อมูลจากไฟล์ `matches_1930_2022.csv` ก่อน จากนั้นค่อยต่อยอดเป็นการนำข้อมูลเข้า PostgreSQL และอ่านข้อมูลจาก database ด้วย Pandas

คำถามที่ต้องตอบให้ได้ในรอบแรก:

1. Dataset นี้มีกี่ rows และ columns
2. มี column อะไรบ้าง
3. มีข้อมูลตั้งแต่ปีไหนถึงปีไหน
4. มีทีมทั้งหมดกี่ทีม
5. column ไหนมี missing values บ้าง
6. สามารถ start PostgreSQL ด้วย Docker ได้
7. สามารถเชื่อมต่อ PostgreSQL จาก Python ได้
8. สามารถ load CSV เข้า PostgreSQL ได้
