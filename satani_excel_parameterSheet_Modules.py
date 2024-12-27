
from satani_excel_search_word import search_entire_sheet
from satani_excel_search_word import search_rectangle


def get_nowtime() -> str:
    '''
    現在年月日時分秒を取得する
    ex-output: 2024-09-02-18-39-10
    '''
    dt_now        = datetime.datetime.now()
    current_time  = dt_now.strftime('%Y-%m-%d-%H-%M-%S')
    return current_time


def get_cell_address(ws, keyword, cordinate="tuple") -> list:
    '''
    キーワードに一致するセル番地を返す
    複数合致した場合は複数のtupleを返す
    ex-config: [(4,6)]
    cordinate引数に"address"を渡した場合はセルアドレス形式で返す
    ex-config: ['F6']
    '''
    cell_address = search_entire_sheet(ws, keyword, cordinate)
    return cell_address


def copy_sheet_row(ws, origin, is_last_element, distance) -> None:
    '''
    シートの一部行をコピーし、コピーした行の直下へ挿入する
    VLAN表やLAG表など動的に項目の行数を増やしたい場合に利用
    source_row <= 原点から見て何行目をコピーしたいのか指定する
    '''
    target_row = origin[0] + distance

    #最後の要素でなければ表に空行を追加
    if is_last_element == False:
        ws.insert_rows(target_row+1)

        #マージしたセルは上に行を挿入しても同じアドレスで動かない
        #shiftメソッドを用いて、挿入した行より下に存在するマージセルを
        #全て一行下へシフトする 
        merged_cells_range = ws.merged_cells.ranges
        for merged_cell in merged_cells_range:
            merged_address = range_boundaries(str(merged_cell))
            merged_row_address = merged_address[1]
            if merged_row_address > target_row:
                merged_cell.shift(0,1)

        #source_rowの内容を追加した空行へコピーする
        for column,cell in enumerate(ws[target_row]):
            target_cell               = ws.cell(row=target_row+1, column=column+1)
            target_cell.value         = copy(cell.value)
            target_cell.font          = copy(cell.font)
            target_cell.border        = copy(cell.border)
            target_cell.fill          = copy(cell.fill)
            target_cell.number_format = copy(cell.number_format)
            target_cell.protection    = copy(cell.protection)
            target_cell.alignment     = copy(cell.alignment)

        #行を追加する度に印刷範囲を一行下へ移動する
        try:
            print_area_before = openpyxl.utils.range_to_tuple(ws.print_area)
            last_column = openpyxl.utils.get_column_letter(print_area_before[1][2])
            last_row    = print_area_before[1][3] + 1
            print_area_after = f"A1:{last_column}{last_row}"
            ws.print_area = print_area_after
        except ValueError:
            None


def copy_template_book(common_template_book_name, common_automate_book_name) -> None:
    '''
    テンプレシートを含むExcelブックをコピーし、自動化用の新規Excelブックを作成する
    '''
    template_bookname = common_template_book_name
    new_bookname = common_automate_book_name
    shutil.copy(template_bookname, new_bookname)


def set_default_sheetview(ws) -> None:
    '''
    シートに対し以下処理を実行する
        - シートのアクティブセルをA1に移動
        - シートのスクロール状態を初期化
        - 拡大倍率を80%に変更
    '''
    cell_no    = 'A1'
    zoom_scale = 80
    ws_view    = ws.sheet_view

    # アクティブセルを'A1'に設定
    ws_view.selection[0].activeCell   = cell_no
    ws_view.selection[0].sqref        = cell_no
    ws_view.selection[0].activeCellId = None

    #シートのスクロールを初期化する
    ws_view.topLeftCell     = cell_no

    # 表示倍率を80％に設定
    ws_view.zoomScale       = zoom_scale
    ws_view.zoomScaleNormal = zoom_scale


def set_default_bookview(common_automate_book_name) -> None:
    '''
    ブック対し以下処理を実行する
        - Excelシートを昇順にソート
        - 表紙、変更履歴シートは先頭となるよう移動
        - アクティブシートを表紙に変更
    '''
    automate_book_name = common_automate_book_name
    automate_book = openpyxl.load_workbook(automate_book_name)

    # Excelシート一覧（昇順）
    ws_title_list = sorted([ws.title for ws in automate_book.worksheets])
    ws_length = len(ws_title_list) - 1

    # Excelシート並び替え実行
    for ws_title in ws_title_list:
        ws = automate_book[ws_title]
        automate_book.move_sheet(ws, offset=ws_length)
    
    # 表紙、変更履歴を先頭へ移動する
    target_sheet_names = ["表紙", "変更履歴"]
    for offset, sheet_name in enumerate(target_sheet_names):
        ws = automate_book[sheet_name]
        automate_book.move_sheet(ws, offset=offset + -ws_length)

    # 表紙をアクティブシートとして設定
    for ws in automate_book.worksheets:
        ws.sheet_view.tabSelected = False
    automate_book.active = automate_book.worksheets[0]
    view = [BookView(activeTab=0)]
    automate_book.views = view

    automate_book.save(automate_book_name)
    automate_book.close()
    
