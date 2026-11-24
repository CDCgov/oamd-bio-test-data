filename    input_parm
C-TEST1-20_filter_seqs_consensus.fasta  -1 ${fasta_inconsensus}
C-TEST1-20_filter_seqs_heuristics.fasta -2 ${fasta_heuristics}
C-TEST1-20_INCONSENSUS.txt  -3 ${blast_inconsensus}
C-TEST1-20_HEURISTICS.txt   -4 ${blast_heuristics}
fullRefs_junction.fasta -5 ${junction_sequences}
C-TEST1-20.fasta    -o ${prefix}.fasta
