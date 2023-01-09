#!/bin/sh


check_init_db() {
	local is_init

	is_init=$(echo "connect wardrobedb; Select * from inittable;" | mysql -u root --password=secret -h mysql)
	echo "$is_init"
	echo "$is_init" | grep -q ERROR
	if [ $? -eq 0 ]
	then
		echo "First run, we need to initalize the db"
		mysql -u root --password=secret -h mysql < /app/createdb.sql
		echo "connect wardrobedb; create table inittable (INIT BOOL NOT NULL);"  | mysql -u root --password=secret -h mysql
	fi
}

check_init_db

streamlit run --server.port=8501 --server.address=0.0.0.0 /app/index.py

