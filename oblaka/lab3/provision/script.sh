sed -i '\/root \/var\/www\/html;/c root /vagrant/Lab3/html;' /etc/nginx/sites-available/default
service nginx restart