#!/bin/bash

ANALYSIS_SCRIPT=$1
NUM_JOBS=$2

for(( job=1; job <= $NUM_JOBS; job++))
do
    sge "~/anaconda3/bin/ipython $ANALYSIS_SCRIPT $job $NUM_JOBS" "analysis_$job"
done
