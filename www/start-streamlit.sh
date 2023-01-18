#!/bin/sh


check_init_db() {
	local is_init
	echo "CHECKING DB"
	while true
	do
		is_init=$(echo "connect wardrobedb; Select * from inittable;" | mysql -u root --password=secret -h wardrobe-mysql 2>&1)
		echo "$is_init"
		echo "$is_init" | grep -q "ERROR 2002.*Can't connect to MySQL server"
		if [ $? -eq 0 ]
		then
			echo "Waiting on db startup"
			sleep 5 
			continue
		fi
		break
	done

	echo "$is_init" | grep -q ERROR
	if [ $? -eq 0 ]
	then
		echo "First run, we need to initalize the db"
		mysql -u root --password=secret -h wardrobe-mysql < /app/createdb.sql
		echo "connect wardrobedb; create table inittable (INIT BOOL NOT NULL);"  | mysql -u root --password=secret -h wardrobe-mysql
	fi
}

echo "STARTING WARDROBE CONTAINER!!!!"

check_init_db

streamlit run --server.port=8501 --server.address=0.0.0.0 /app/index.py

