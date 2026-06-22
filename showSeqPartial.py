from Bio import SeqIO
import sys

# 配列のFASTAファイル、どの塩基からどの塩基までを表示するかを指定してFASTAファイルの部分配列を表示するスクリプト

def extract_subsequence(fasta_file, start, end):
    for record in SeqIO.parse(fasta_file, "fasta"):
        # Pythonのインデックスは0始まりなので調整
        subseq = record.seq[start-1:end]

        print(f">{record.id} ({start}-{end})")
        print(subseq)
        print()

if __name__ == "__main__":
    # 引数チェック
    if len(sys.argv) != 4:
        print("Usage: python script.py <fasta_file> <start> <end>")
        sys.exit(1)

    fasta_file = sys.argv[1]
    start = int(sys.argv[2])
    end = int(sys.argv[3])

    extract_subsequence(fasta_file, start, end)
