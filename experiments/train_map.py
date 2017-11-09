from myutils import utils
from myutils.vgg16 import Vgg16 
from option import Options

import torch
from torch.autograd import Variable
from torch.optim import Adam
import torchvision.datasets as dset
import torchvision.transforms as transforms

def main():
	"""
	For extending the package:
		1. Extending a new network type:
			1). define your own file under the folder 'net/' 
			2). implement your own nn.Module in mynn.py if need
			3). implement train and evaluate functions base on your need
			4). set up the import in the follows
		2. Extending a new experiment (changing the options)
			1). define the subcommand of the options
			2). implement the experiment function like optimize()
			3). set up the experiment as follows
	"""
	# figure out the experiments type
	args = Options().parse()
	if args.subcommand is None:
		raise ValueError("ERROR: specify the experiment type")
	if args.cuda and not torch.cuda.is_available():
		raise ValueError("ERROR: cuda is not available, try running on CPU")	
	

	# Gatys et al. using optimization-based approach
	extract_feats(args)

def extract_feats(args):
	vgg = Vgg16()
	utils.init_vgg16(args.vgg_model_dir)

	cap = dset.CocoCaptions(root = '/Pulsar1/Datasets/coco/train2014/train2014',annFile='/Neutron9/sahil.c/datasets/annotations/captions_train2014.json',transform=transforms.ToTensor())

	print('Number of samples: ', len(cap))
	for i, t in cap:
		image = i.unsqueeze(0)	
		image = Variable(utils.preprocess_batch(image), requires_grad=False)
		image = utils.subtract_imagenet_mean_batch(image)
		features_content = vgg(image)

	# img, target = cap[3] # load 4th sample
	# print(cap[3])
	# print("Image Size: ", img.size())
	# print(target)

if __name__ == '__main__':
	main()