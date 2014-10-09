all:
	scons
test:
	./test_pl.py
compare:
	echo; (cd build; tar cf - `find . -name \*.tex`) | (cd expected; tar -xvf -)
clean:
	rm -rf build .tmp pyconbook-2014.log pyconbook-2014.pdf *.pyc .sconsign.dblite
