from collections import defaultdict
import numpy as np

######
# Snakemake workflow
######

rule get_paths:
    input:
        autoasvpath=expand("{autoasvpath}", autoasvpath=config['autoasvpath']),
        projectdir=expand("{projectdir}", projectdir=config['projectdir']),
        inputfile=expand("{inputfile}", inputfile=config['inputfile']),
        paramsfile=expand("{paramsfile}", paramsfile=config['paramsfile']),
        logfile=expand("{logfile}", logfile=config['logfile'])

######
# Create group structure
######

inputfile=str(rules.get_paths.input.inputfile)
inputtable=np.loadtxt(open(inputfile, "rb"), dtype='str', delimiter=",")
inputtable2=inputtable[:,0:2]
my_list  = inputtable2.tolist()
GROUPS = defaultdict(list)
for value, key in my_list:
	GROUPS[key].append(value)

##
# Primer clipping
##

rule primerclip_for:
    input:
        read1="{projectpath}/0-Rawdata/{run}/{sample}_1.fq.gz",
        read2="{projectpath}/0-Rawdata/{run}/{sample}_2.fq.gz"
    threads: 1
    output:
        read1="{projectpath}/1-Primersclipped/{run}/{sample}_1.fq.gz",
        read2="{projectpath}/1-Primersclipped/{run}/{sample}_2.fq.gz"
    params:
        primer_for=expand("{primer_for}", primer_for=config['primer_for']),
        primer_rev=expand("{primer_rev}", primer_rev=config['primer_rev'])
    shell:
        """
        mkdir -p {wildcards.projectpath}/1-Primersclipped
        cutadapt --pair-adapters -e 0.2 -g ^{params.primer_for} -G ^{params.primer_rev} --discard-untrimmed -o {output.read1} -p {output.read2} {input.read1} {input.read2}
        """

rule primerclip_rev:
    input:
        read1="{projectpath}/0-Rawdata/{run}/{sample}_1.fq.gz",
        read2="{projectpath}/0-Rawdata/{run}/{sample}_2.fq.gz"
    threads: 1
    output:
        read1="{projectpath}/1-Primersclipped_rev/{run}/{sample}_1.tmp.fq.gz",
        read2="{projectpath}/1-Primersclipped_rev/{run}/{sample}_2.tmp.fq.gz"
    params:
        primer_for=expand("{primer_for}", primer_for=config['primer_for']),
        primer_rev=expand("{primer_rev}", primer_rev=config['primer_rev'])
    shell:
        """
        mkdir -p {wildcards.projectpath}/1-Primersclipped_rev
        cutadapt --pair-adapters -e 0.2 -g ^{params.primer_rev} -G ^{params.primer_for} --discard-untrimmed -o {output.read1} -p {output.read2} {input.read1} {input.read2}
        """

rule reverseflip:
    input:
        read1="{projectpath}/1-Primersclipped_rev/{run}/{sample}_1.tmp.fq.gz",
        read2="{projectpath}/1-Primersclipped_rev/{run}/{sample}_2.tmp.fq.gz"
    threads: 1
    output:
        read1="{projectpath}/1-Primersclipped_rev/{run}/{sample}_1.fq.gz",
        read2="{projectpath}/1-Primersclipped_rev/{run}/{sample}_2.fq.gz"
    shell:
        """
        gunzip -c {input.read2} | sed 's/2:N:0:/1:N:0:/g' | gzip -c - > {output.read1}
        gunzip -c {input.read1} | sed 's/1:N:0:/2:N:0:/g' | gzip -c - > {output.read2}
        rm {input.read2}
        rm {input.read1}
        """

##
# Compute scores
##

rule optimaltrim:
    input:
        read1="{projectpath}/1-Primersclipped/{run}/{sample}_1.fq.gz",
        read2="{projectpath}/1-Primersclipped/{run}/{sample}_2.fq.gz"
    threads: 1
    output:
        "{projectpath}/1-Primersclipped/{run}/{sample}.csv"
    shell:
        """
        python {rules.get_paths.input.autoasvpath}/trimlengths.py -f {input.read1} -r {input.read2} -l 420 -e 2 -v 20 -m 1000 -o {output}
        """

rule optimaltrim_rev:
    input:
        read1="{projectpath}/1-Primersclipped_rev/{run}/{sample}_1.fq.gz",
        read2="{projectpath}/1-Primersclipped_rev/{run}/{sample}_2.fq.gz"
    threads: 1
    output:
        "{projectpath}/1-Primersclipped_rev/{run}/{sample}.csv"
    shell:
        """
        python {rules.get_paths.input.autoasvpath}/trimlengths.py -f {input.read1} -r {input.read2} -l 420 -e 2 -v 20 -m 1000 -o {output}
        """

##
# Find optimal trimming scores
##

rule all:
    input:
        expand("/Users/anttonalberdi/autoasvtest/2-Trimmed/{run}/trim.csv", run=list(GROUPS.keys()))

rule optimalfinal:
    input:
        lambda wildcards: expand("/Users/anttonalberdi/autoasvtest/1-Primersclipped/{run}/{sample}.csv", run= wildcards.run, sample=GROUPS[wildcards.run])
    output:
        "/Users/anttonalberdi/autoasvtest/2-Trimmed/{run}/trim.csv"
    shell:
        """
        cat {input} > {output}
        """
