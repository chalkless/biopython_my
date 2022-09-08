# BioPython でPubMedデータを処理する
## データ取得編
- 基本事項：NCBIからプログラムでデータを取得する仕組みのeutilsを用いる。具体的にはesearchでキーワード検索してPMIDリストを取得し、efetchでPMIDを投げて書誌情報を取得する
- BioPythonでは：Bio.Entrezを用いる
```
from Bio import Entrez
```
- 今はeutilsを使うときにはこちらのメールアドレスを伝えるものらしい（何かあったら連絡をくれるらしい。が、何もないにこしたことない）
```
Entrez.email = "A.N.Other@example.com"
```
    - このアドレスはとりあえず例示で示すときに使われるものである
    - GitHubで自分のアドレスを晒したら、それはある意味インシデントである
### キーワード検索からPMIDリストまで
- 実際にNCBIに検索するところ
```
handle = Entrez.esearch(db="pubmed", term="biopython")
```
- データを取得してその後
    - 件数を確認したり、PMIDリストを取得したり
```
record = Entrez.read(handle)
record["IdList"]
（結果）
['19304878', '18606172', '16403221', '16377612', '14871861', '14630660', '12230038']
```
