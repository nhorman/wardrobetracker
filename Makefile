WDVOL=$(shell podman volume ls | awk '/wardrobe/ {print $$2}')

all:
	podman-compose build

clean:
	podman-compose down
	podman rmi localhost/wardrobetracker_wardrobe-trakcer
	podman volume rm ${WDVOL}
