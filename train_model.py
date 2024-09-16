'''
https://github.com/CompVis/taming-transformers
Training on your own dataset can be beneficial to get better tokens and hence better images for your domain. Those are the steps to follow to make this work:

install the repo with conda env create -f environment.yaml, conda activate taming and pip install -e .
put your .jpg files in a folder your_folder
create 2 text files a xx_train.txt and xx_test.txt that point to the files in your training and test set respectively (for example find $(pwd)/your_folder -name "*.jpg" > train.txt)
adapt configs/custom_vqgan.yaml to point to these 2 files
run python main.py --base configs/custom_vqgan.yaml -t True --gpus 0,1 to train on two GPUs. Use --gpus 0, (with a trailing comma) to train on a single GPU.
'''