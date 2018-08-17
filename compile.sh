g++ -o sim sim.c
./sim 25 50 50
./sim 50 50 50
./sim 75 50 50
./sim 100 50 50
./sim 150 50 50
./sim 200 50 50
./sim 300 50 50
./sim 500 50 50
./sim 1000 50 50
python gen.py data25_50_50.json
python gen.py data50_50_50.json
python gen.py data75_50_50.json
python gen.py data100_50_50.json
python gen.py data150_50_50.json
python gen.py data200_50_50.json
python gen.py data300_50_50.json
python gen.py data500_50_50.json
python gen.py data1000_50_50.json
python variance_envelope.py data50_50_50.json data75_50_50.json data100_50_50.json data150_50_50.json data200_50_50.json data300_50_50.json data500_50_50.json data1000_50_50.json
python EBB_envelope.py formatted_data50_50_50.json 50 formatted_data75_50_50.json 75 formatted_data100_50_50.json 100 formatted_data150_50_50.json 150 formatted_data200_50_50.json 200 formatted_data300_50_50.json 300 formatted_data500_50_50.json 500 formatted_data1000_50_50.json 1000
python graph.py
