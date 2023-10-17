This is the program to fit regression multi-output neural network for protein secondary structure 
prediction by DSSP 8 without reliancy to the evolutionary information (i.e. sequence alignments).
(C) Yuri V. Milchevskiy, Yuri V. Kravatsky under the terms of the Creative Commons CC BY-NC-SA 4.0 license
email: milch@eimb.ru

1. Download datasets for learning:
   wget https://ftp.eimb.ru/Milch/Learn.Q8/learn_Q8.dbs.tar.gz
   or
   wget ftp://ftp.eimb.ru/Milch/Learn.Q8/learn_Q8.dbs.tar.gz

2. Put learn_Q8.dbs.tar.gz to the same directory as Learn_Q8.py script and unpack it:
   tar -xf learn_Q8.dbs.tar.gz

3. Install python3 and all proper dependencies:
   1. python 3 (tested with v. 3.8.10)
   2. numpy (tested with v. 1.22.3)
   3. PyTorch (tested with v. 1.12.1)

3. If you want to learn from the scratch, delete following files:
   Q8_DATA_MODEL
   Q8_DATA_MODEL_FOR_CPU
   and set lr_start to 0.01 in Learn_Q8.py.
   If you don't have GPU with 16GB RAM (or more) you should disable test dataset loading
   by setting test_enabled = 0 in the string 28 of the script.
   
4. Run learning neural network:
   python3 Learn_Q8.py
   At any moment you can stop learning process, tune up lr_start and re-run learning
   process by the same command. The previous results will be saved and the learning
   will continue from the same place as it stopped.
