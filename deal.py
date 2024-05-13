import pandas as pd
import os
import csv


def main():
    root_path = r"E:\\"
    csv_file_path = r"./佛山BC病理.csv"

    deal_path(root_path, csv_file_path)


def deal_path(root_path = "./乳腺病理多模态", csv_file_path = "乳腺病理多模态.csv"):
    endwith = ['.kfb', '.tif', '.svs']

    files_with_extension = get_files_with_extension(root_path, endwith)

    # Save the information to a CSV file
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['filename', 'filepath']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        writer.writeheader()
        for file_name, file_path in files_with_extension:
            writer.writerow({'filename': file_name, 'filepath': file_path})

    replace_symbol = ['_', '(', '（', '=', '-',' ','.']
    df = pd.read_csv(csv_file_path)
    df['clear_filename'] = df['filename'].apply(lambda x: os.path.basename(x))
    for symbol in replace_symbol:
        df['clear_filename'] = df['clear_filename'].apply(lambda x: x.split(symbol)[0].strip() if symbol in x else x)
    df.to_csv(csv_file_path, index=False)
    print(f"File information has been saved to {csv_file_path}.")

def deal_ct():
    pass

def get_files_with_extension(directory, extensions):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(tuple(extensions)):
                file_path = os.path.join(root, file)
                file_list.append((file, file_path))
    return file_list

def merge_csv():
    # 指定目录路径
    directory = 'D:\数据处理\乳腺癌新辅助病理整理'
    output_file_path = 'D:\数据处理\乳腺癌新辅助病理整理.csv'  

    # 获取目录下所有子目录中的.csv文件
    csv_files = [os.path.join(root, file) for root, dirs, files in os.walk(directory) for file in files if file.endswith('.csv')]

    # 如果没有找到任何.csv文件，给出提示并退出
    if not csv_files:
        print("No .csv files found in the specified directory or its subdirectories.")
        exit()

    # 创建一个空的DataFrame用于存储所有.csv文件数据
    concatenated_df = pd.DataFrame()

    # 循环读取每个.csv文件并将它们concat到DataFrame中
    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        print(csv_file, df.columns)
        # 统一 df 的 列名 为 ['filename', 'filepath']
        # df.columns = ['file_name', 'file_path']
        concatenated_df = pd.concat([concatenated_df, df], ignore_index=True)

    # 处理 df_csv 中的 filename 列，提取病理号
    concatenated_df = deal_with_csv(concatenated_df)
    # 将concatenated_df保存为一个新的.csv文件
    concatenated_df.to_csv(output_file_path, index=False)

    print(f"All .csv files concatenated and saved to {output_file_path}.")

def deal_with_csv(df_csv):
    df_csv.dropna(inplace=True)
    # 从 df_csv 的 filename 中提取病理号, 去掉其中的 '-', '_'
    df_csv['病理号'] = df_csv['filename'].apply(lambda x: x.split('-')[0] if '-' in x else x)
    df_csv['病理号'] = df_csv['病理号'].apply(lambda x: x.split('_')[0] if '_' in x else x)
    df_csv['病理号'] = df_csv['病理号'].apply(lambda x: x.split('.')[0] if '.' in x else x)

    return df_csv




if __name__ == "__main__":
    main()
    # merge_csv()



