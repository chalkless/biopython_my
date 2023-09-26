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

- NCBI_API_KEYを取得すると１秒間に3回までのリクエストが10回までに拡張される
  - 取得方法：https://github.com/chalkless/lifesciDB/blob/master/edirect/README.md
  - 参考までに、eutilsで作成するURLにapi_key=XXXをつける
  - 以下のように指定
```
Entrez.api_key = "MyAPIkey"
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
count = int(record["Count"])
print(record["IdList"])
（結果）
['19304878', '18606172', '16403221', '16377612', '14871861', '14630660', '12230038']
```
- まとめ
```
#!/usr/bin/env python

from Bio import Entrez

Entrez.email = "..."

handle = Entrez.esearch(db="pubmed", term="検索したい語")
record = Entrez.read(handle)
count  = int(record["Count"]
print(record["IdList"])
```
- 参考：esearch → efetch を連続でやる場合は別途 やり方があるので後ろで追記


### PMIDから書誌情報まで
- 概要；efetchで情報取得する。書き方が2パターンあるので使い分ける
  - XMLで取得するパターン
  - MEDLINE形式（テキストファイル）で取得し、Bio.Medlineで処理する
```
(XML版)
from Bio import Entrez

Entrez.email = "..."

handle = Entrez.efetch(db='pubmed', id=19304878, retmode='xml')
```

```
# PMIDを,で区切ってstrで渡してabstを取得することもできる
handle = Entrez.efetch(db='pubmed', id=pmid_query, retmode='xml')
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
- 参考つづき：Entrez.parse()とEntrez.read() もあるのだが、これはBio.Medlineとはちょっと挙動が違い、XMLがリストのようになっているときはparseを使うようなので、通常のXMLファイルであればread()を使っておけばよい。
- 処理する部分は後ろに追記

### esearch → efetch を連続でやる場合
- esearch の結果でPMIDリストを取得してそれをefetchに投げるのでなく、esearchをかけた際に得られるトークンをefetchに投げることで解析の続きとして結果が得られる。
- キモ：esearchでusehistoryをつけるとトークンが返ってくるようになるので、efetchでそれを指定する

```
# eserach部
...
handle = Entrez.esearch(db = "pubmed", term = term_search, usehistory="y")
records = Entrez.read(handle)

token   = records['WebEnv']
q_key   = records['QueryKey']
count = int(records['Count'])

# efetch部

retmax = 1000

for start in range(0, count, retmax):
    handle = Entrez.efetch(db='pubmed', retmode='xml', restart=start, retmax=retmax, webenv=token, query_key=q_key)
```
- handle を　read()とかしてファイルに書き込んだりする


## データ処理編
```
    records = Entrez.read(handle)
    # Entrez.read(handle)するとPythonのオブジェクトに変換される
    
```

- PubMedデータ（MEDLINE形式 or XML）を処理して必要な部分を抽出

```
records = Entrez.read(handle)
for record in records["PubmedArticle"]:
    title = record["MedlineCitation"]["Article"]["ArticleTitle"]
    pmid  = record["MedlineCitation"]["PMID"]
```
