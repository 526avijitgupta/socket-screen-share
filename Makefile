runserver:
	python server/main.py &
	python server/filesend.py &
	python server/filerecv.py &
	python server/vcs.py &

runclient:
	google-chrome client/index.html

