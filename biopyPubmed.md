# BioPython でPubMedデータを処理する
## データ取得編
- 基本事項：NCBIからプログラムでデータを取得する仕組みのeutilsを用いる。具体的にはesearchでキーワード検索してPMIDリストを取得し、efetchでPMIDを投げて書誌情報を取得する
- BioPythonでは：Bio.Entrezを用いる
```
from Bio import Entrez
```
- 参考：http://biopython.org/DIST/docs/tutorial/Tutorial.html (BioPython Tutorial)

- 今はeutilsを使うときにはこちらのメールアドレスを伝えるものらしい（何かあったら連絡をくれるらしい。が、何もないにこしたことない）
  - このアドレスはとりあえず例示で示すときに使われるものである
  - GitHubで自分のアドレスを晒したら、それはある意味インシデントである
```
Entrez.email = "A.N.Other@example.com"
```

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

### PMIDから書誌情報まで
- 概要；efetchで情報取得する。書き方が2パターンあるので使い分ける
  - XMLで取得するパターン
  - MEDLINE形式（テキストファイル）で取得し、Bio.Medlineで処理する
```
(XML版)
from Bio import Entrez

Entrez.email = "..."

handle = Entrez.efetch(db='pubmed', id=19304878, retmode='xml')
records = Entrez.read(handle)
for record in records["PubmedArticle"]:
    title = record["MedlineCitation"]["Article"]["ArticleTitle"]
    pmid  = record["MedlineCitation"]["PMID"]
```
```
(MEDLINE形式版)
from Bio import Entrez
from Bio import Medline

Entrez.email = "..."

handle = Entrez.efetch(db='pubmed', id=19304878, rettype='medline', retmode='text')
records = Medline.parse(handle)
for record in records:
    title = record['TI']
    pmid  = record['PMID']
```
- 参考：Medline.parse() の他に Medline.read() というのがあるが、parseは複数の論文を扱うもの、readはひとつひとつ扱うもの、という違い

