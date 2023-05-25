from apiclient.discovery import build
# 下記リンクよりAPIキーを取得
#   https://cloud.google.com/console
# 参考リンク
#   https://hi3103.net/notes/web/1271
DEVELOPER_KEY = "AIzaSyDZ8Ac5sAKoYwi_P9PMtCHwiUPwaS7DZdA"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
#############################
########## 関数定義 ##########
#############################
from gensim.models import KeyedVectors

def reverse_recommend(q):
  model = KeyedVectors.load_word2vec_format('model.vec', binary=False)
  model.save("model.kv")
  ans = model.most_similar(negative=[q])
  return ans

def youtube_search(q):
  ### YoutubeAPIを使えるようにする
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
  ### search.listメソッドを呼び出して、指定された条件に合致する結果を取得
  # q：検索クエリ
  # type：リソースのタイプ。チャンネル・プレイリスト・動画
  # part：リソースのプロパティ。snippet→動画のIDだけでなく、タイトルや説明が含まれる
  # videoEmbeddable：true→埋め込み可能な動画だけ返す
  search_response = youtube.search().list(
    q=q,
    type = "video",
    part="id,snippet",
    maxResults=5,
    videoEmbeddable = "true"
  ).execute()

  ### 検索結果をvideosに格納
  titles=[]
  urls=[]
  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
      # 文字の置き換え
      # id→urlへ
      titles.append(search_result["snippet"]["title"].replace("\u3000", "").replace("\\u200d", "").replace("\xa0", ""))
      urls.append("https://www.youtube.com/embed/" + search_result["id"]["videoId"])

  return titles,urls

##########################
########## 実行 ##########
##########################
#print("\n".join(youtube_search(word)), "\n")
#print("\n".join(youtube_search(ans[0][0])), "\n")