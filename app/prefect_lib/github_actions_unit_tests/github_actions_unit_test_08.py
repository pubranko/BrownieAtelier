from prefect.testing.utilities import prefect_test_harness

def test_exec():
    with prefect_test_harness():
        # カレントディレクトリをpythonpathに追加
        import os
        import sys
        current_directory = os.environ.get('PWD')
        if current_directory:
            sys.path.append(current_directory)

        # <16>
        # 日次朝処理
        from prefect_lib.flow_nets.morning_flow_net import morning_flow_net

        # 絞り込み用の引数がなければ全量チェック
        morning_flow_net()

if __name__ == "__main__":
    test_exec()
