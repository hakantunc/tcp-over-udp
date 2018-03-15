all: html pdf

html:
	pandoc -s -f gfm --metadata pagetitle='Reliable UDP' --css github-pandoc.css -o reliable-udp.html ../README.md
pdf:
	pandoc -o reliable-udp.pdf ../README.md
