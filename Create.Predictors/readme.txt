This is set of the programs to generate databases and predictors to perform local (by Protein Blocks) 
protein structure prediction without reliancy to the evolutionary information (i.e. sequence alignments).
(C) Yuri V. Milchevskiy, Yuri V. Kravatsky under the terms of the Creative Commons CC BY-NC-SA 4.0 license
email: milch@eimb.ru

1. Unpack Gen.Dbs.Preds.NN.tar.gz:
   tar -xf Gen.Dbs.Preds.NN.tar.gz

2. Download databases:
   wget https://ftp.eimb.ru/Milch/Generate.DB.Predictors/Store_20231020.tgz 
   or
   wget ftp://ftp.eimb.ru/Milch/Generate.DB.Predictors/Store_20231020.tgz 

3. Put Store_20231020.tgz to the same directory where you have unpacked
   previously Gen.Dbs.Preds.NN.tar.gz, and unpack it:
   tar -xf Store_20231020.tgz

4. If you want to use Linux static precompiled binaries, copy 4 files 
   1_MakeChainBinary
   2_MakeFrequencyDatabases
   3_MakeRegressStepwiseModel
   4_PredictorListToNN  
   from bin directory to the main directory of the project (to the same 
   directory where _config file is located). 
   If you want to recompile binaries, read manual in the file
   Generate.Databases.and.Predictors.pdf carefully.

5. Get PDB databank by command
   rsync -rlpt -v -z --delete --port=33444 \
   rsync.rcsb.org::ftp_data/structures/divided/pdb/ /home/username/PDB
   where '/home/username/PDB' is the directory where you want to put it.

6. Unpack PDB databank by command
   gunzip -r *
   in the PDB directory

7. Edit _config file to set the correct path to PDB

8. Read manual in the file Generate.Databases.and.Predictors.pdf carefully
