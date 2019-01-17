g++ -o sim sim.c
./sim 50 50 50
./sim 75 50 50
./sim 100 50 50
./sim 150 50 50
./sim 200 50 50
./sim 300 50 50
./sim 500 50 50
./sim 1000 50 50
python gen.py z1data50_50_50.json z1data75_50_50.json z1data100_50_50.json z1data150_50_50.json z1data200_50_50.json z1data300_50_50.json z1data500_50_50.json z1data1000_50_50.json
python graph.py
python graph2.py 50 75 100 150 200 300 500 1000
python bandit.py 20 30 40 50 60 70 80 90 100 110 120 130 140 150 160 170 180 190 200 210 220 230 240 250 260 270 280 290 300 310 320 330 340 350 360 370 380 390
python rearrange.py
