#!/bin/sh
# Grid Engine options (lines prefixed with #$)              
#$ -cwd                  
#$ -N run_model
#$ -l h_rt=00:02:00 
#$ -l h_vmem=3G
#  These options are:
#  job name: -N
#  use the current working directory: -cwd
#  runtime limit of 60 minutes: -l h_rt
#  memory limit of 2 Gbyte: -l h_vmem

# Initialise the environment modules
. /etc/profile.d/modules.sh
module load anaconda
conda activate camkii-project-env

# Tell eddie where mcell is saved
export CELLBLENDER_BASE_PATH=/exports/cmvm/eddie/sbms/groups/stefanlab/Blender-2.93-CellBlender/2.93/
export MCELL_PATH=$CELLBLENDER_BASE_PATH/scripts/addons/cellblender/extensions/mcell/
export PATH=$PATH:$CELLBLENDER_BASE_PATH/python/bin/

echo "start run"
# Run the program
python prepare_run_files.py
echo "finish run"
