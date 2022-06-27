cd /workspace
echo "Download ..." | boxes
python3 /workspace/task/classification_sample/download_resnext50.py

echo "Run ..." | boxes
python3 demo.py -c ./task/classification_sample/task.json -s