all:
	scons
test:
	./test_pl.py
compare:
	(cd build; tar cf - `find . -name \*.tex`) | (cd expected; tar -xvf -)
diffs:
	./gen_diff.sh
clean:
	rm -rf build .tmp pyconbook-2014.log pyconbook-2014.pdf *.pyc .sconsign.dblite
