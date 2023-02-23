```
echo "Pgadmin command!!!"
sudo docker run -p 5050:80  -e "PGADMIN_DEFAULT_EMAIL=admin@admin.com" -e "PGADMIN_DEFAULT_PASSWORD=root"  -d dpage/pgadmin4

```
