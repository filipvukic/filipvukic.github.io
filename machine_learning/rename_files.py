import os
import shutil

account = "skiingviral"

def rename_files(directory):
    print(f"Renaming files in {directory}")
    print(f"Current directory: {os.getcwd()}")
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                try:
                    shutil.move(os.path.join(root, file), os.path.join(root, 'caption.txt'))
                except Exception as e:
                    print(f"Failed to rename {file}: {e}")
            elif file.endswith('.mp4'):
                try:
                    shutil.move(os.path.join(root, file), os.path.join(root, 'video.mp4'))
                except Exception as e:
                    print(f"Failed to rename {file}: {e}")

def main():
    directory = './machine_learning/data_' + account
    rename_files(directory)
    print("Files renamed successfully!")

if __name__ == "__main__":
    main()