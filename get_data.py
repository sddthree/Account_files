    # 问题描述
    path = r'H:\课题\论文-甲状腺癌四分型\数据集\'
    save_name = "h5_files.csv"
    split_symbols = ['_', '-', '(', '（', '.']
    # 现在我想找到path路径下的所有.h5文件目录, 并且将这些文件的路径保存到一个list中
    h5_paths = [os.path.join(root, file) for root, dirs, files in os.walk(path) for file in files if file.endswith('.h5')]
    # 提取这些文件的文件名, 并且将这些文件名保存到一个list中
    h5_filenames = [os.path.basename(path) for path in h5_paths]
    # 进一步筛选这些文件名, 提取其中的病理号, 删去其余不需要的内容, 如N104453-1.2.jpg, 只需要N104453, 并且将这些病理号保存到一个list中
    df = pd.DataFrame(h5_filenames, columns=['filename'])
    df['filepath'] = h5_paths
    df['clear_filename'] = df['filename']
    for symbol in split_symbols:
        df['clear_filename'] = df['clear_filename'].apply(lambda x: x.split(symbol)[0] if symbol in x else x)
    # 最后将这些病理号保存到一个csv文件中, 这三列分别命名为"filepath", 'filename', 'clear_filename'
    df.to_csv(path + save_name, index=False)