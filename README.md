# shorten_url

#### maintainer: chenpohsun1@gmail.com

-----

## Design

- 把每個短網址在剛建立的時候就會先放到 Redis cache, 減少 DB connections
- 希望避免在高流量時的 concurrency 問題所以除了基本的 db transaction 還有加上 redis-lock,使用 redis-lock 的好處是萬一真的需要加開機器也可以有效地避免 A 機器有上鎖 B 機器卻沒有鎖到的問題
- DB 使用 MySQL, 原因是 1. Django 本身對 MySQL 就比較友善 2.因為需要快速根據短網址的 code 找到原本的網址然後重導向過去,所以在 code 上面加上 index 可以快速搜尋 3. 因為每組短網址只能對應到一組正確的網址 所以這個欄位是 unique
- 縮短網址產生出來的代碼最大數量是每一位 26+26+10 長度為 5 所以 62^5 = 916132832


## Local dev setup steps

### Prerequisite
- `$ echo '127.0.0.1 dev-shorten_url.work.tw' >> /etc/hosts`

- Make sure native Docker is installed, and the following ports are available (change port-foward setting if your local port is occupied.)
    - 6379  (Redis)
    - 6606  (MySQL)
    - 80 (Nginx/OpenResty)

### Run!

- Start the world by `docker-compose up -d` and after the initial build everything should just run, and the environment is now ready
- DB can be accessed from within host machine terminal with `mysql -h 0.0.0.0 -P 6606 -u app -p app app`
- Execute `docker-compose exec app bash` to go into the container environment
- `cd /var/www/shorten_url.work.tw/django_www && python manage.py makemigrations && python manage.py migrate` to migrate DB (if you are happy with the current model XDD (or else skip this step)
- `cd /var/www/shorten_url.work.tw/django_www && python manage.py runserver` to run debug Django server
- Inside your favorite browser, go to `dev-shorten_url.work.tw` to see the page
