.PHONY:

# Project
build:
	docker build -t app .
run:
	docker run -it -p 5173:5173 -v $$(pwd)/src:/app/src app:latest

