def add_value_to_next_empty_cell_in_row(df, row_index, value):
    row = df.loc[row_index]
    empty_indices = row.index[row.isnull()].tolist()
    if empty_indices:
        empty_index = empty_indices[0]
        df.loc[row_index, empty_index] = value
    else:
        pass