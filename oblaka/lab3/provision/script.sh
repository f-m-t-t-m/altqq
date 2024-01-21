apt update
apt install nginx -y
sed -i '\/root \/var\/www\/html;/c root /vagrant/lab3/html;' /etc/nginx/sites-available/default
service nginx restart