######
# Snakemake workflow
######

rule get_paths:
    input:
        parampath=expand("{parampath}", parampath=config['parampath']),
        logpath=expand("{logpath}", logpath=config['logpath'])

##
# Primer clipping
##

rule primerclip:
    input:
        read1="{projectpath}/0-Rawdata/{run}/{sample}_1.fq.gz",
        read2="{projectpath}/0-Rawdata/{run}/{sample}_2.fq.gz"
    threads: 1
    output:
        read1="{projectpath}/1-Primersclipped/{run}/{sample}_1.tmp.fq.gz",
        read2="{projectpath}/1-Primersclipped/{run}/{sample}_2.tmp.fq.gz",
        read1_rev="{projectpath}/1-Primersclipped/{run}/{sample}_1rev.tmp.fq.gz",
        read2_rev="{projectpath}/1-Primersclipped/{run}/{sample}_2rev.tmp.fq.gz"
    params:
        primer1=expand("{primer1}", primer1=config['primer1']),
        primer2=expand("{primer2}", primer2=config['primer2'])
    shell:
        """
        mkdir -p {wildcards.projectpath}/1-Primersclipped
        cutadapt --pair-adapters -e 0.2 -g ^{params.primer1} -G ^{params.primer2} --discard-untrimmed -o {output.read1} -p ${output.read2} {input.read1} {input.read2} 2>> /dev/null
        cutadapt --pair-adapters -e 0.2 -g ^{params.primer2} -G ^{params.primer1} --discard-untrimmed -o {output.read1_rev} -p ${output.read2_rev} {input.read1} {input.read2} 2>> /dev/null
        """

rule reverseflip:
    input:
        read1="{projectpath}/1-Primersclipped/{run}/{sample}_1.tmp.fq.gz",
        read2="{projectpath}/1-Primersclipped/{run}/{sample}_2.tmp.fq.gz",
        read1_rev="{projectpath}/1-Primersclipped/{run}/{sample}_1rev.tmp.fq.gz",
        read2_rev="{projectpath}/1-Primersclipped/{run}/{sample}_2rev.tmp.fq.gz"
    threads: 1
    output:
        read1="{projectpath}/1-Primersclipped/{run}/{sample}_1.tmp.fq.gz",
        read2="{projectpath}/1-Primersclipped/{run}/{sample}_2.tmp.fq.gz",
        read1_rev="{projectpath}/1-Primersclipped/{run}/{sample}_1rev.tmp.fq.gz",
        read2_rev="{projectpath}/1-Primersclipped/{run}/{sample}_2rev.tmp.fq.gz"
    params:
        primer1=expand("{primer1}", primer1=config['primer1']),
        primer2=expand("{primer2}", primer2=config['primer2'])
    shell:
        """
        mkdir -p {wildcards.projectpath}/1-Primersclipped
        cutadapt --pair-adapters -e 0.2 -g ^{params.primer1} -G ^{params.primer2} --discard-untrimmed -o {output.read1} -p ${output.read2} {input.read1} {input.read2} 2>> /dev/null
        cutadapt --pair-adapters -e 0.2 -g ^{params.primer2} -G ^{params.primer1} --discard-untrimmed -o {output.read1_rev} -p ${output.read2_rev} {input.read1} {input.read2} 2>> /dev/null
        """
