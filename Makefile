runserver:
	python server/vcs.py &
	python server/main.py &

runclient:
	google-chrome client/index.html

