import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer


def fea_cases_sbert(
    fea_cases_path: str,
    output_path: str,
    sheet_name: str,
    column_name: str,
    model_name_or_path = 'all-MiniLM-L6-v2',
):
    # 加载数据
    print(f'loading data from {fea_cases_path} ...')
    df = pd.read_excel(fea_cases_path, sheet_name=sheet_name, engine='openpyxl')
    sentences = df[column_name].tolist()

    # 建立 Sentence-BERT 模型
    print('loading model...')
    sbert = SentenceTransformer(model_name_or_path)

    # 编码
    print('encoding...')
    embeddings = sbert.encode(sentences)
    print(f'shape: {embeddings.shape}')

    # 保存到文件
    print(f'saving vectors to {output_path} ...')
    np.save(output_path, embeddings)


if __name__ == '__main__':
    # 英文
    fea_cases_sbert(
        'G:\pythonProject\FEASimPaper\Excel2Json\FEA案例数据_英文400.xlsx',
        'FEA案例数据_英文400_sbert.npy',
        sheet_name='Sheet1',
        column_name='FEAcases',
        model_name_or_path='all-distilroberta-v1'
    )  # shape = (n, 768)

    # 中文
    fea_cases_sbert(
        'G:\pythonProject\FEASimPaper\Excel2Json\FEA案例数据_中文400.xlsx',
        'FEA案例数据_中文400_sbert.npy',
        sheet_name='Sheet1',
        column_name='FEAcases',
        model_name_or_path='paraphrase-multilingual-mpnet-base-v2'
    )  # shape = (n, 768)