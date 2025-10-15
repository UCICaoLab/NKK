# NKK
Neural network kinetics - NNK


Vacancy diffusion barrier dataset for NNK model: https://doi.org/10.5281/zenodo.17069342

This data repository contains the data for training the neural network model in the following paper.

Xing, B., Rupert, T. J., Pan, X., & Cao, P. (2024). Neural network kinetics for exploring diffusion multiplicity and chemical ordering in compositionally complex materials. Nature Communications, 15(1), 3879.

The repository has the following directories:

 

material_models:
This directory consists 46 DUMP format files representing 46 distinct atomistic models. The compositions are listed in the text file "dirnames.txt". These compositions are used for preparing dataset for training ml models including on-lattice representation of local atomistic configuration and corresponding diffusion barrier from NEB calculation. The "data" folder contains on-lattice representations and the "labels" folder contains the diffusion barriers.

data:
This directory consists of 46 NPY format files, each of which corresponds to the on-lattice representations of local atomistic configurations from one composition. Each NPY file contains a four-dimensional matrix which serves as the input to ml models. The matrix dimension is 16000x9x9x9, containing 16000 on-lattice representations of distinct local atomistic configurations, each of which has the dimension of 9x9x9. The file name takes the format as *.npy, where the asterisk denotes the index of composition. The compositions are listed in the text file named as "dirnames.txt".

labels:
This directory consists of 46 NPY format files, each of which corresponds to the diffusion barriers from one composition. The 46 compositions are listed in the text file named as "dirnames.txt". Each NPY file contains a vector with 16,000 barriers corresponding to 16,000 on-lattice representations from the "data" folder. For example, "0.npy" in the "labels" folder consists the labels (diffusion barriers) corresponding to on-lattice representations from "0.npy" in the "data" folder.

scripts:
This directory consists of scripts for generating on-lattice representations of local atomistic configurations. 
