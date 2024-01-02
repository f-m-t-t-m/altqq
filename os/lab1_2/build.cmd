git pull
mkdir _build

cd _build
g++ -c ../hello_world.cpp
g++ -o  hello_world.exe hello_world.o
cd ..