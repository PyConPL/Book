prologues:=3;
beginfig(-1)

vardef Sym(expr p) =
  p reflectedabout ((0,0),(0,1))
enddef;

def F(expr color, p) =
  fill p withcolor color;
  fill Sym(p) withcolor color;
enddef;

def D(expr p) =
  draw p withcolor black;
  draw Sym(p) withcolor black;
enddef;


W := 30pt;
H := 1.2W;
path tulw, glowa, oczko,nosek, lapka;
pickup pencircle scaled 0.03W;
tulw  = fullcircle xscaled 2W yscaled 2H;
glowa = fullcircle xscaled W yscaled 0.9W shifted (0,H);
oczko = (fullcircle xscaled 1.3 rotated 45) scaled 0.2W
        shifted (-.25W,1.1H);
nosek = fullcircle scaled 0.1W shifted (-0.1W,(H+0.35W));
% czulek	
D(((0,0) .. (-0.1W,0.05W) .. (-0.3W,0.1W))
  shifted (point 0 of nosek));
lapka = (0,0) .. (-.1W,.1W) .. (-.3W,.2W);
D(lapka rotated 20 shifted (-.5W,H));
D(lapka rotated 40 shifted (-.6W,0.8H));
D(lapka rotated 70 shifted (-.6W,-0.8H));

fill glowa withcolor black;
fill tulw  withcolor red;
fill fullcircle scaled 0.6W shifted (0,(H-0.3W-0.1W)) withcolor black;
draw (0,-H)--(0,H);

F(white, oczko);
F(white, nosek);
F(black, fullcircle scaled 0.4W yscaled 1.2 shifted (-0.3W,-.1W));
F(black, fullcircle scaled 0.2W yscaled 1.2 rotated -45 shifted (-0.5W,0.5H));
F(black, fullcircle scaled 0.3W yscaled 1.2 rotated 45 shifted (-0.5W,-0.5H));




endfig;
end.
