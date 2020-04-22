## About

This is a Snakemake profile for use with slurm on the UCD farm cluster. I've removed the attempts to
use `sacct` in `slurm-status.py`, as Farm isn't configured properly and it always fails. I've also
removed the extremely verbose failure output, and have modified the script to output specific job
statuses to stderr when a failure occurs (not on every status check).

## Installation

    mkdir -p ~/.config/snakemake
    cd ~/.config/snakemake
    git clone https://github.com/camillescott/ucd-farm-slurm-profile.git

An example cluster config is given as well. You'll want to edit the paths for your account and
project (sorry, I was too lazy to make it a cookiecutter =P). Namely, you'll want to edit
the `logdir`, `chdir`, and `mail-user` entries, and remove / edit the per-rule resources for your
workflow.

## Usage

    snakemake -p -j 16 --rerun-incomplete --keep-going --profile ucd-farm-slurm-profile --cluster-config cluster_config.yml

Note that I still provide `--cluster-config` in the `snakemake` invocation: without this, you won't
have access to `wildcards` expansions in your config variables.

The most important resource specifications are `mem` and `time`. `time` is specified in minutes.,
`mem` in megabytes.
I've included a function in `common.snakefile` to easily use hours (or days, or whatever other
keywords python's `timedelta` accepts). An example resources block would look like:

    resources:
        mem = 8000,
        time = lambda _: as_minutes(hours=3)

Naturally, you can make use of `attempts` (and other parameters) to your lambda functions:

    resources:
        mem = lambda wildcards, attempts: attempts * 4000,
        time = lambda wildcards, attempts: as_minutes(hours=(2**(attempts-1)))

Or, other time type combos:

    resources:
        time = lambda _: as_minutes(days=1, hours=4)

See the `timedelta`
[documentation](https://docs.python.org/3/library/datetime.html#datetime.timedelta) for other
keywords.

## Other

The `cluster_config.yml` can include any parameter that can be passed to `sbatch`; these are
described in the slurm [documentation](https://slurm.schedmd.com/sbatch.html). Make sure they match
exactly, as they're expanded and placed directly in the command invocation.
