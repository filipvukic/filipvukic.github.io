# create python script to save all captions by going through all "caption.txt" files in all folders of  the machinelerning/data_powdervibe directory and saving all the captions to a file called powdervibe_captions.txt

import os
import shutil

account = "powdervibe"

def save_all_captions(directory):
    print(f"Saving all captions in {directory}")
    print(f"Current directory: {os.getcwd()}")
    captions = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == 'caption.txt':
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        caption = f.read()
                        captions.append(caption)
                except Exception as e:
                    print(f"Failed to read {file}: {e}")
    with open(account + '_captions.txt', 'w', encoding='utf-8') as f:
        print(f"Writing captions to " + account + "_captions.txt")
        for caption in captions:
            f.write(caption + '\n')


def main():
    directory = './machine_learning/data_' + account
    save_all_captions(directory)
    print("Captions saved successfully!")

if __name__ == "__main__":
    main()