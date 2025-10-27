import pandas as pd

data = pd.DataFrame([
    ['Young','High','Electronics','Yes'],
    ['Young','Medium','Clothing','Yes'],
    ['Middle','High','Electronics','Yes'],
    ['Old','Low','Groceries','No'],
    ['Old','Medium','Electronics','No']
], columns=['Age','Income','Product','Buys'])

def find_s(df):
    h = ['ϕ']*(len(df.columns)-1)
    for i,row in df.iterrows():
        if row['Buys']=='Yes':
            for j in range(len(h)):
                if h[j]=='ϕ': h[j]=row[j]
                elif h[j]!=row[j]: h[j]='?'
    return h

def candidate_elimination(df):
    attrs, S, G = df.columns[:-1], [['ϕ']*3], [['?']*3]
    for _,row in df.iterrows():
        x,y=row[:-1],row[-1]
        if y=='Yes':
            S=[[x[i] if s[i] in ['ϕ',x[i]] else '?' for i in range(3)] for s in S]
            G=[g for g in G if all(g[k] in ['?',S[0][k]] for k in range(3))]
        else: S=[s for s in S if not all(s[k] in ['?',x[k]] for k in range(3))]
    return S,G

finds=find_s(data); S,G=candidate_elimination(data)
print("Find-S:", finds)
print("Candidate Elimination -> S:", S)
print("Candidate Elimination -> G:", G)
