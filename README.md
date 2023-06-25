# 커뮤니티 총학공지 인스타그램 크롤러
커뮤니티 총학공지 인스타그램 로컬 서버의 크롤링 코드입니다.

* 파이썬 버전
  * 3.10.9
* required library
  * boto3
  * instaloader

## 사용법
```bash
chmod +x run_crawl.sh
$ mkdir -p ./log/log_python
$ mkdir -p ./log/log_exec
```
```bash
crontab -e
```
최하단에 다음 내용 추가
```bash
0 * * * * ./run_instagram_crawl.sh
```
