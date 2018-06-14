# HugProtocol
Hug and get contact info by using Rasberrypi and RC522

###　書き下し
なにができる：ハッグするだけで、連絡先を交換する。

#### いいところ：
0.スマホ出さずに交換できる

1.ハッグ（日本ではあまりしないが、海外では普通）、握手など、人同士として、自然、面白い体験できる

2.大人数でも気軽いに交換できる。

3.GPSや日時を指定して、交換する属性が自分で決められる

#### シナリオ：
AとBが互いにタッチすると、DBに

src des
A   B
B   A  
みたいな書き込んで、AB,BAがある限りAにBのINFOを送信、BにAのINFOを送信。

もし
src des
A   B
だけであれば、送信しない。

2つTableがある：ユーザの属性を保存するテーブル；Authenticationテーブル（受送信）
