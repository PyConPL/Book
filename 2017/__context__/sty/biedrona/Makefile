all: biedrona.pdf

biedrona.pdf: biedrona.mp Makefile
	echo input biedrona > tmp.mp
	mpost tmp.mp
	gs -sDEVICE=png16m -sOutputFile=tmp.png -r200 -dEPSFitPage -dNOPAUSE tmp.ps -c quit
	autotrace --background-color FFFFFF tmp.png  | perl -pe 's/setcmykcolor/setcmykcolor 0.7 .setopacityalpha/' > tmp.ps
	gs -sDEVICE=pdfwrite -sOutputFile=tmp.pdf -dEPSFitPage -dNOPAUSE tmp.ps -c quit
	mv tmp.pdf $@
	rm tmp.*

biedrona.ps: biedrona.mp Makefile
	mpost $<


clean:
	rm *~ biedrona.pdf tmp*
