#!/bin/bash

# crawl.py 실행 명령어
python3 ./crawl.py >> ./log/log_python/crawl_error.log 2>&1

# crawl.py 실행 후 로그 기록
echo "Crawl completed at $(date)" >> ./log/log_exec/crawl_exec.log
