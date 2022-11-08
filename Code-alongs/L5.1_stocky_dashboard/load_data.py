import pandas as pd
import os


class StockData:
    def __init__(self, data_folder_path: str) -> None:
        self._data_folder_path = data_folder_path

    def stock_dataframe(self, stockname: str) -> list:
        stock_df_list = []

        for path_ending in [
            "_TIME_SERIES_DAILY_ADJUSTED.csv",
            "_TIME_SERIES_INTRADAY_EXTENDED.csv",
        ]:
            # example:
            # data_folder_path: c/users/User/Folder/...
            # stockname: AAPL
            # path_ending: _TIME_SERIES_DAILY_ADJUSTED.csv
            path = os.path.join(
                self._data_folder_path, stockname + path_ending
            )  # os path join for working in any system regardless of that systems namespace separators

            stock = pd.read_csv(
                path, index_col=0, parse_dates=True
            )  # index_col makes first col index, parse_dates reads as datetime where possible
            stock.index.rename("Date", inplace=True)

            stock_df_list.append(stock)

        return stock_df_list
