for row in seed.stream_rows(connection):
    print(row)
    break  # remove this break to stream all rows

