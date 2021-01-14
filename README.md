# shorten_url

#### maintainer:


-----


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
