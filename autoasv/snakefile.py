######
# Snakemake workflow
######

rule get_paths:
    input:
        paramsfile=expand("{paramsfile}", paramsfile=config['paramsfile']),
        logfile=expand("{logfile}", logfile=config['logfile'])

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
# Find optimal trimming scores
##
