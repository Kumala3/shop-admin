### 🔧 Instalation:

1. Rename `.env.dist` to `.env` and fill in required data.
2. **Docker:**

    1. You can start a project with Docker right away, and if you don't have it, you can [Download](https://docs.docker.com/get-docker/) it.
    2. Run project with next command: `docker-compose up --build`
    3. Run migrations with next command:

        `docker compose exec api alembic upgrade head`

3. **Without Docker:**
    1. Create [venv](https://docs.python.org/3/library/venv.html)
    2. Install all requirements:
        - Go to **tgbot** and install requirements
          `pip install -r requirements.txt`
        - Go to **infrastructure** and install requirements:
          `pip install -r requirements.txt`
    4. To start DataBase run next command in the terminal:
        ```
        postgres -c max_connections=150
                -c shared_buffers=512MB -c effective_cache_size=1536MB
                -c maintenance_work_mem=128MB -c checkpoint_completion_target=0.9 -c wal_buffers=16MB
                -c default_statistics_target=100 -c random_page_cost=1.1 -c effective_io_concurrency=200
                -c work_mem=3495kB -c min_wal_size=1GB -c max_wal_size=4GB -c max_worker_processes=2
                -c max_parallel_workers_per_gather=1 -c max_parallel_workers=2 -c max_parallel_maintenance_workers=1
        ```
    5. Go to `infrastructure` and run all migrations with next command in the terminal: 
    
        `alembic upgrade head`
    4. To start bot run next command in the terminal: `python3 bot.py`
