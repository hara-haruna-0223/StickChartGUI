#ライブラリのインポート
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.pyplot import axes
import pandas as pd
import datetime as dt
import pandas_datareader.data as web
import mplfinance as mpf
import requests
from matplotlib.figure import Figure

def stock2graph():
    global canvas
    s_code = (en_code.get()+".JP")
    fy = int(f_year.get())
    fm = int(f_month.get())
    fd = int(f_day.get())
    ty = int(t_year.get())
    tm = int(t_month.get())
    td = int(t_day.get())
    start = dt.date(fy,fm,fd)
    end = dt.date(ty,tm,td)
    df = web.DataReader(s_code,'stooq',start, end)
    d_ohlcv = {'Open': 'first',
               'High': 'max',
               'Low': 'min',
               'Close': 'last',
               'Volume': 'sum'}
    df_w = df.resample('W-MON', closed='left', label='left').agg(d_ohlcv)
    df = df.sort_index()
    #print(df)
    df_w = df_w.sort_index()
    clear()
    fig ,axes= mpf.plot(df, title="\n"+s_code, type='candle', mav=(5, 25),volume=True, 
	style='mike', returnfig=True, figsize=(10, 5))
    canvas = FigureCanvasTkAgg(fig, frame_graph)
    canvas.draw()
    canvas.get_tk_widget().pack()


def clear():
    canvas.get_tk_widget().destroy()
  
def load_data():
    global df_c
    url = "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls"
    r = requests.get(url)
    with open('data_j.xls', 'wb') as output:
        output.write(r.content)
    df_c = pd.read_excel("./data_j.xls", index_col=1)

def code2name():
    en_name.delete('0','end')
    code = en_code.get()
    if (int(code) in df_c.index.values) == True:
        s_name = df_c.at[int(code), '銘柄名']
        en_name.insert(0, str(s_name))
    else:
        en_name.insert(0, '銘柄はありません')
        
#ウインドウの作成
root = tk.Tk()
#ウインドウのタイトル
root.title("日本株価チャートを表示するGUIアプリ")
#ウインドウサイズと位置指定 幅,高さ,x座標,y座標 
root.geometry("1000x700+30+20")

#フレームの作成
frame = tk.Frame(root, width=1000, height=700, bg="#4c6473")
frame.place(x=0, y=0)

frame_code = tk.Frame(frame,relief=tk.FLAT,bg="#4c6473")
frame_code.place(x=5,y=5,width=990,height=50)

frame_menu = tk.Frame(frame, relief=tk.FLAT, bg="#4c6473", bd=2)
frame_menu.place(x=5, y=55, width=990, height=125)

frame_stocks = tk.Frame(frame,relief=tk.FLAT,bg="#4c6473")
frame_stocks.place(x=5,y=130,width=990,height=155)

frame_graph = tk.Frame(frame, relief=tk.FLAT, bg="#4c6473", bd=2)
frame_graph.place(x=5, y=160, width=990, height=695)

#ラベル作成
l_code = tk.Label(frame_code,text="証券コード", relief="flat", fg="white", bg="#4c6473")
l_code.grid(row=0, column=0, sticky = tk.W)
#証券コード入力ボックス
en_code = tk.Entry(frame_code, width = 6, relief="solid")
en_code.grid(row=0, column=1, sticky = tk.W, padx=5,pady=10)

#日付
l_from = tk.Label(frame_menu,text="期間を入力", relief="flat", fg="white", bg="#4c6473")
l_from.grid(row=0, column=0, sticky = tk.W)
#from_year
f_year = tk.Entry(frame_menu, width = 6 ,relief="solid")
f_year.grid(row=1, column=1, sticky = tk.W)
l_fy = tk.Label(frame_menu,text="年", relief="flat", fg="white", bg="#4c6473")
l_fy.grid(row=1,column=2 , sticky = tk.W)
#from_month
f_month = tk.Entry(frame_menu, width = 6,relief="solid")
f_month.grid(row=1, column=3, sticky=tk.W)
l_fm = tk.Label(frame_menu,text="月", relief="flat", fg="white", bg="#4c6473")
l_fm.grid(row=1, column=4,sticky=tk.W) 
#from_day
f_day = tk.Entry(frame_menu, width = 6, relief="solid")
f_day.grid(row=1,column=5,sticky=tk.W)
l_fd = tk.Label(frame_menu,text="日", relief="flat", fg="white", bg="#4c6473")
l_fd.grid(row=1,column=6,sticky=tk.W)
#～
l_ft = tk.Label(frame_menu,text="～",relief="flat",fg="white",bg="#4c6473")
l_ft.grid(row=1,column=7,sticky=tk.W)
#to_year
t_year = tk.Entry(frame_menu, width = 6, relief="solid")
t_year.grid(row=1,column=8, sticky = tk.W)
l_ty = tk.Label(frame_menu,text="年", relief="flat", fg="white", bg="#4c6473")
l_ty.grid(row=1,column=9,sticky = tk.W)
#to_month
t_month = tk.Entry(frame_menu, width = 6, relief="solid")
t_month.grid(row=1, column=10,sticky = tk.W)
l_tm = tk.Label(frame_menu,text="月", relief="flat", fg="white", bg="#4c6473")
l_tm.grid(row=1,column=11, sticky = tk.W)
#to_day
t_day = tk.Entry(frame_menu, width = 6, relief="solid")
t_day.grid(row=1,column=12, sticky = tk.W)
l_td = tk.Label(frame_menu,text="日", relief="flat", fg="white", bg="#4c6473")
l_td.grid(row=1,column=13, sticky = tk.W)

#ボタン作成
button = tk.Button(frame_menu, text="検索", command=lambda:[code2name(), stock2graph()])
button.grid(row=1, column=14, sticky = tk.E, padx=5, pady=5)

#銘柄名コメント
en_com = tk.Label(frame_stocks,text="銘柄名",fg="white",bg="#4c6473")
en_com.grid(row=1,column=0,sticky=tk.W,pady=5)
#銘柄名出力用
en_name = tk.Entry(frame_stocks, width =100, relief="solid")
en_name.grid(row=1,column=1,sticky=tk.W,padx=5,pady=5)

#データフレーム読み込み
load_data()
    

#グラフ用キャンバス
fig = Figure(figsize=(10, 5))
canvas = FigureCanvasTkAgg(fig, frame_graph)
canvas.get_tk_widget().pack()

#イベントループ
root.mainloop()