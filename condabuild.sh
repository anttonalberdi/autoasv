######
# Build conda package
######

#It is essential to specify the channel, otherwise the r library dependencies will yield an error
cd /Users/anttonalberdi/github/
rm -rf autoasv_builds
mkdir autoasv_builds
conda-build autoasv -c conda-forge --output-folder /Users/anttonalberdi/github/autoasv_builds

#Convert build to different platforms
conda convert --platform all /Users/anttonalberdi/github/autoasv_builds/osx-64/autoasv-1.0-py37_0.tar.bz2 -o /Users/anttonalberdi/github/autoasv_builds

######
# Upload conda package
######

#Log-in to anaconda
anaconda login

#Upload package (all versions)
anaconda upload /Users/anttonalberdi/github/autoasv_builds/*/autoasv-1.0-py37_0.tar.bz2 --force

######
# Create conda environment
######

# Create environment yaml
cat > autoasv_environment.yaml <<EOL
name: autoasv_env_2
channels:
  - conda-forge
  - bioconda
  - anttonalberdi
dependencies:
  - bioconda::snakemake-minimal=6.3.0
  - conda-forge::biopython=1.78
  - conda-forge::ruamel.yaml=0.16.12
  - bioconda::cutadapt=2.10
  - anttonalberdi::autoasv=1.0
EOL

# Create environment
conda env create --file autoasv_environment.yaml python=3.8.10

######
# Test autoasv
######

source activate autoasv_env_2
#conda install autoasv -n autoasv_env_2 -c anttonalberdi

autoasv
autoasv -i hello -d world -f this -r is -a test -x .

######
# Deactivate and remove environment
######

conda remove autoasv
conda deactivate
conda env remove -n autoasv_env_1

######
# Local test
######
source activate autoasv_env_2
python3 /Users/anttonalberdi/github/autoasv/autoasv/autoasv.py
python3 /Users/anttonalberdi/github/autoasv/autoasv/autoasv.py -i hello -d /Users/anttonalberdi/ -f asd -r is -a test -x . --adaptorforward ad
