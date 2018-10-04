g++ -O3 -o sim sim.c
./sim 50 50
python gen.py data50_50.json 50
python gen.py data50_50.json 75
python gen.py data50_50.json 100
python gen.py data50_50.json 150
python gen.py data50_50.json 200
python gen.py data50_50.json 300
python gen.py data50_50.json 500
python gen.py data50_50.json 1000
python variance_envelope.py data50_50_50.json data75_50_50.json data100_50_50.json data150_50_50.json data200_50_50.json data300_50_50.json data500_50_50.json data1000_50_50.json
python EBB_envelope.py formatted_data50_50_50.json 50 formatted_data75_50_50.json 75 formatted_data100_50_50.json 100 formatted_data150_50_50.json 150 formatted_data200_50_50.json 200 formatted_data300_50_50.json 300 formatted_data500_50_50.json 500 formatted_data1000_50_50.json 1000
python graph.py
python graph2.py formatted_data50_50_50.json 50 formatted_data75_50_50.json 75 formatted_data100_50_50.json 100 formatted_data150_50_50.json 150 formatted_data200_50_50.json 200 formatted_data300_50_50.json 300 formatted_data500_50_50.json 500 formatted_data1000_50_50.json 1000
