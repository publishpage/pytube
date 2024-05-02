from pytube import YouTube
from moviepy.editor import VideoFileClip
import os

def download_and_convert_video(url, output_file):
    # YouTubeの動画をダウンロード
    yt = YouTube(url)
    stream = yt.streams.filter(file_extension='mp4', resolution='360p').first()
    if stream is None:
        print(f"360pのMP4動画が見つかりませんでした: {url}")
        return

    # 動画をダウンロード（一時ディレクトリに保存）
    temp_path = "temp/"
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)
    downloaded_file = stream.download(output_path=temp_path)

    # 出力ディレクトリを確認し、存在しない場合は作成
    output_dir = "output/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # ダウンロードした動画を開いて変換
    clip = VideoFileClip(downloaded_file)
    final_output_path = os.path.join(output_dir, output_file)
    try:
        clip.write_videofile(final_output_path, codec='mpeg4', fps=24, bitrate='3000k')
    except Exception as e:
        print(f"エラーが発生しました: {e}")
    finally:
        # 一時ファイルを削除
        clip.close()
        os.remove(downloaded_file)

# ファイルからURLと出力ファイル名を読み込む
with open('videos.txt', 'r', encoding='utf-8') as file:
    for line in file:
        url, output_file = line.strip().split(',')
        download_and_convert_video(url, output_file)
