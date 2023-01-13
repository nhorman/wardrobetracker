WDVOL=$(shell podman volume ls | awk '/wardrobe/ {print $$2}')

.PHONY: all down cleanimage cleanvol clean

all:
	podman-compose build

down:
	podman-compose down
cleanimage: down
	podman rmi localhost/wardrobetracker_wardrobe-trakcer
cleanvol: down
	podman volume rm ${WDVOL}
	
clean: cleanimage cleanvol

