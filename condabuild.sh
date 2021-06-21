######
# Build conda package
######

#It is essential to specify the channel, otherwise the r library dependencies will yield an error
cd /Users/anttonalberdi/github/
mkdir autoasv_builds
conda-build autoasv -c conda-forge --output-folder /Users/anttonalberdi/github/autoasv_builds

#Convert build to different platforms
conda convert --platform all /Users/anttonalberdi/github/autoasv_builds/osx-64/autoasv-1.0-py38_0.tar.bz2 -o /Users/anttonalberdi/github/autoasv_builds

######
# Upload conda package
######

#Log-in to anaconda
anaconda login

#Upload package (all versions)
anaconda upload /Users/anttonalberdi/github/autoasv_builds/*/autoasv-1.0-py38_0.tar.bz2 --force

######
# Create conda environment
######

# Create environment yaml
cat > autoasv_environment.yaml <<EOL
name: autoasv_env_1
channels:
  - conda-forge
  - bioconda
  - anttonalberdi
dependencies:
  - anttonalberdi::autoasv=1.0
EOL

# Create environment
conda env create --file autoasv_environment.yaml python=3.8.10
conda install autoasv -n autoasv_env_1 -c anttonalberdi

source activate autoasv_env_1

autoasv
python3 -m autoasv

echo $PATH

conda deactivate
conda env remove -n autoasv_env_1
