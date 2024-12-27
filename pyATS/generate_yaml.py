
import os
import openpyxl
import jinja2
from   jinja2 import Template, Environment, FileSystemLoader


def setup_j2():
    """
    Jinja2(テンプレートエンジン)の環境セットアップ
    可読性向上+おまじない
    """

    def debug(text) -> None:
        print(text)

    j2_env = Environment(
        trim_blocks             = True,
        keep_trailing_newline   = True,
        extensions              = ['jinja2.ext.do', 'jinja2.ext.loopcontrols'],
        loader                  = FileSystemLoader('./', encoding='utf8')
    )

    j2_env.filters.update({
        'debug'  : debug
    })

    j2_engine = j2_env.get_template('template.j2')

    return j2_engine


def get_hosts_datas():
    """
    自動化対象ホスト群のホスト名/IP/OS/機種情報を取得する
    参照している資料は試験書のチェックリスト
    """

    wb_filename = "Excel.xlsx"

    wb = openpyxl.load_workbook(wb_filename)
    ws = wb["Excel"]

    hostsdatas = {}

    for row in ws:
        column_class = row[2].value
        # もしホスト情報に関する行でなければ後続の処理をスキップする
        if column_class not in ["SW", "WLC", "RT"]:
            continue

        hostname = row[1].value
        classify = row[2].value
        os       = row[3].value
        platform = row[4].value
        ip       = row[5].value
        password = row[7].value

        hostsdatas[hostname] = {
            "platform" : platform,
            "class"    : classify,
            "os"       : os,
            "platform" : platform,
            "ip"       : ip,
            "password" : password
        }

    return hostsdatas


if __name__ == "__main__":
    """
    各関数へdocstringを記載済み。
    コーディング用ソフトウェアを使用している場合
    関数名へカーソルを合わせる事で参照可能。
    """

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    filename   = 'devices.yaml'
    j2_engine  = setup_j2()
    hostsdatas = get_hosts_datas()

    with open(filename, "w") as f:
        generated_str = j2_engine.render(hostsdatas = hostsdatas)
        f.write(generated_str)

