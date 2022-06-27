cd /workspace
echo "Download ..." | boxes
./task/humanpose_sample/download_model.sh
echo "Converting ..." | boxes
./converter/pose-converter \
-m ./task/humanpose_sample/resnet18_baseline_att_224x224_A.pth \
-j ./task/humanpose_sample/label.json \
-e ./task/humanpose_sample/resnet18_baseline_att_224x224_A.engine
echo "Run ..." | boxes
python3 demo.py -c task/humanpose_sample/task.json -s