cd /workspace

echo "Download ..." | boxes
./task/people_seg_sample/download_model.sh

echo "Converting ..." | boxes
./converter/tao-converter -k nvidia_tlt \
-d 3,576,960 \
-o mask_fcn_logits/Conv2D,mask_fcn_logits/BiasAdd \
-e /workspace/task/people_seg_sample/peoplesegnet.engine \
-t fp32 \
-i nchw \
-m 1 \
/workspace/task/people_seg_sample/peoplesegnet_resnet50.etlt

echo "Run ..." | boxes
python3 demo.py -c task/people_seg_sample/task.json -s