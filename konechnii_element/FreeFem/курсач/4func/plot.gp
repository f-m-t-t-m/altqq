set xyplane at 0
set size ratio -1
set view map
set xrange [0:1]
set yrange [0:1]
set dgrid3d 20,20
set palette model HSV
set palette rgb 3,2,2
splot "plot6.dat" w l pal notitle