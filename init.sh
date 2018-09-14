ln -s /root/DataMS/config/supervisor.conf /etc/supervisor/conf.d/DataMS.conf
ln -s /root/DataMS/config/nginx.conf /etc/nginx/sites-enabled/DataMS.conf

pip3 install -r requirements.txt
