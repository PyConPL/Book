all:
	scons
	echo Running twice is required to make good table of contents.
test:
	./test_pl.py
compare:
	../../tools/gen_cmp.sh
diffs:
	../../tools/gen_diff.sh
clean:
	rm -rf build .tmp pyconbook-????.log pyconbook-????.pdf *.pyc .sconsign.dblite genart.txt
