import subprocess
import re
import os
import sys
from datetime import datetime
import shutil


def extract_audio(video_filepath: str):
    """
    对给定的视频文件提取音频。 (This function is unchanged)
    """
    if not video_filepath or not os.path.isfile(video_filepath):
        print(f"  [!] 错误: 文件路径无效或文件不存在 -> '{video_filepath}'")
        return False

    print(f"  [+] 正在处理视频: {os.path.basename(video_filepath)}")

    basename, _ = os.path.splitext(video_filepath)
    audio_filepath = basename + ".mp3"

    if os.path.exists(audio_filepath):
        print(f"  [✓] 音频 '{os.path.basename(audio_filepath)}' 已存在，跳过转换。")
        return True

    try:
        print(f"  [>] 正在提取音频 -> {os.path.basename(audio_filepath)} ...")
        ffmpeg_command = ['ffmpeg', '-i', video_filepath, '-vn', '-y', '-loglevel', 'error', audio_filepath]
        result = subprocess.run(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)

        if result.returncode == 0:
            print(f"  [✓] 音频提取成功。")
            return True
        else:
            print(f"  [!] 错误: ffmpeg 转换失败 (返回码: {result.returncode})。")
            print(f"      ffmpeg 输出: {result.stderr.decode('utf-8', 'replace')}")
            return False
    except FileNotFoundError:
        print("  [!] 错误: 'ffmpeg' 命令未找到。请确保已安装并配置好环境变量。")
        return False
    except Exception as e:
        print(f"  [!] 提取音频时发生未知错误: {e}")
        return False


def download_and_process(url: str, is_playlist: bool):
    """
    新策略：
    1. 创建一个临时目录。
    2. 使用 you-get 将所有视频下载到该目录。
    3. 下载完成后，遍历目录中的文件，重命名并提取音频。
    """
    # --- Phase 1: Download all videos ---

    # Create a temporary directory for this download session
    temp_dir = f"temp_downloads_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(temp_dir, exist_ok=True)

    print("\n--------------------------------------------------")
    print(f"阶段 1: 开始下载视频到临时目录: '{temp_dir}'")
    print("请耐心等待所有下载任务完成...")
    print("--------------------------------------------------")

    command = ['you-get', '--no-caption']  # --no-caption avoids downloading .xml files
    if is_playlist:
        command.append('--playlist')

    # Use -o to force the output directory
    command.extend(['-o', temp_dir, url])

    try:
        # We run the process and wait for it to complete. We no longer need to parse its output in real-time.
        # We use 'utf-8' and 'replace' to ensure the log prints as cleanly as possible to the console.
        subprocess.run(command, check=True, encoding='utf-8', errors='replace')

    except FileNotFoundError:
        print("\n[!] 严重错误: 'you-get' 命令未找到。请确保已正确安装并配置环境变量。")
        shutil.rmtree(temp_dir)  # Clean up
        return
    except subprocess.CalledProcessError as e:
        print(f"\n[!] 严重错误: you-get 执行失败 (返回码: {e.returncode})。请检查链接是否有效以及网络连接。")
        shutil.rmtree(temp_dir)  # Clean up
        return
    except Exception as e:
        print(f"\n[!] 运行时发生严重错误: {e}")
        shutil.rmtree(temp_dir)  # Clean up
        return

    print("\n--------------------------------------------------")
    print("阶段 1: 所有下载任务已完成。")
    print("阶段 2: 开始处理已下载的文件。")
    print("--------------------------------------------------\n")

    # --- Phase 2: Process downloaded files ---

    file_counter = 1
    processed_count = 0
    try:
        # Get a list of all files downloaded into our temp directory
        downloaded_files = os.listdir(temp_dir)
        video_files = [f for f in downloaded_files if f.lower().endswith(('.mp4', '.flv', '.mkv', '.webm'))]

        if not video_files:
            print("[!] 警告: 在临时目录中未找到任何视频文件。")
            return

        for filename in video_files:
            original_filepath = os.path.join(temp_dir, filename)

            # Generate new safe filename and move it to the current directory
            _, extension = os.path.splitext(original_filepath)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            new_filename = f"video_{timestamp}_{file_counter}{extension}"

            try:
                # Move and rename the file out of the temp dir into the script's dir
                shutil.move(original_filepath, new_filename)
                print(f"[*] 已移动并重命名: '{filename}' -> '{new_filename}'")

                # Now, extract audio from the safely-named file
                if extract_audio(new_filename):
                    processed_count += 1

                file_counter += 1
            except Exception as e:
                print(f"[!] 处理文件 '{filename}' 时出错: {e}")

            print("-" * 20)

    finally:
        # Clean up the temporary directory
        if os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
                print(f"\n[✓] 已清理临时目录: '{temp_dir}'")
            except OSError as e:
                print(f"\n[!] 无法清理临时目录 '{temp_dir}': {e}")
                print(f"    您可以手动删除它。")

    print(f"\n[✓] 阶段 2: 文件处理完成。共成功处理 {processed_count} 个文件。")


# --- 主程序入口 ---
if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_url = sys.argv[1]
    else:
        input_url = input("请输入Bilibili视频链接: ")

    if not input_url.strip():
        print("错误: 输入的链接为空。")
        sys.exit(1)

    input_url = input_url.strip()

    is_bili_playlist = "bilibili.com/video/BV" in input_url and ("&p=" in input_url or "?p=" in input_url)

    if is_bili_playlist:
        choice = input(
            "\n检测到这是一个Bilibili播放列表链接。\n  (1) 只处理当前这一个视频\n  (2) 处理整个播放列表的所有视频\n请输入选项 (1 或 2，默认为 2): ").strip()
        if choice == '1':
            download_and_process(input_url, is_playlist=False)
        else:
            download_and_process(input_url, is_playlist=True)
    else:
        download_and_process(input_url, is_playlist=False)

    print("\n🎉 全部任务已结束。")