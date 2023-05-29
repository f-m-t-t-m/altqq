set xyplane at 0
set size ratio -1
set view map
set xrange [0:1]
set yrange [0:1]
set palette model HSV
set palette rgb 3,2,2
set isosamples 80, 80
set pm3d
splot exp(10*x) w l pal notitle