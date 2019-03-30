FROM nginx:alpine

ADD proxy/nginx.conf /etc/nginx/nginx.conf

ADD application/CodeRx/static /www/static

RUN chown -R nginx:nginx /www