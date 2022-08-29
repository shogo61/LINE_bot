# LINE_bot
インターンで制作したLINEbotです。

料理名と体重からその料理のカロリーを消費するのにかかる運動量を返すプログラムです。


実行手順

１、ユーザーからメッセージで料理名のキーワードを受け取る。

２、BeautifulSoupでWebスクレイピングを実行し、カロリーSlismというサイトから検索結果とそのカロリーを取得する。

３、取得した料理名とカロリーの上位４件をPyMySQLでDBに格納する。

４、料理名４つをユーザーに候補として返し、その中から料理を確定してもらう（その中に候補がなければ１に戻る）。

５、料理が確定したらその料理名とカロリーをユーザーにメッセージとして返し、userテーブルにカロリーを格納する。

６、ユーザーから体重をメッセージとして受け取って、そのカロリーを消費するのに必要な運動時間を計算する。

７、各運動時間をユーザーにメッセージとして返す（１に戻る）。


データベースの設計

foodsテーブル

上記３で格納するテーブル

・id:連番。このカラムでユーザーが候補の中からどれを選んだかを特定する

・料理名

・カロリー


userテーブル

各ユーザーに正しく返信する（混線が起きないようにする）ためのテーブル

カロリーが格納されているかどうかでユーザーからのメッセージが料理名か体重かの判別をする

⇨カロリーに値が格納されていなかったらメッセージは料理のキーワード

⇨カロリーに値が格納されていたらメッセージは体重

  ⇨運動時間を計算して返したら、カラムを削除する
  
・userId:ラインアカウントごとに割り振られている一意のID

・カロリー
