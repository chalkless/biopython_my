from Bio import SeqIO
import sys

# マルチFASTAファイルを引数として指定すると、各配列の長さを配列名とともにタブ区切り表示する

for record in SeqIO.parse(sys.argv[1], "fasta"):
    print(f"{record.id}\t{len(record.seq)}")
