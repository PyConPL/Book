all:
	scons
	echo Running twice is required to make good table of contents.
test:
	./test_pl.py
compare:
	(cd build; tar cf - `find . -name \*.tex`) | (cd expected; tar -xvf -)
diffs:
	./gen_diff.sh
clean:
	rm -rf build .tmp pyconbook-2016.log pyconbook-2016.pdf *.pyc .sconsign.dblite
