def tiles(filepath, tile_ids):
    '''
    Generate tiles from this dataset.

    Parameters
    ----------
    filepath: str
        The filename of the sqlite db file
    tile_ids: [str...]
        A list of tile ids of the form

    Returns
    -------
    tiles: {pos: tile_value}
        A list of values indexed by the tile position
    '''
    new_obj = {}

    for  tile_id in tile_ids:
        parts = tile_id.split('.')
        uuid = parts[0]
        zoom = int(parts[1])
        xpos = int(parts[2])

    pass

def get_1D_tiles(db_file, zoom, tile_x_pos, numx=1, numy=1):
    '''
    Retrieve a contiguous set of tiles from a 2D db tile file.

    Parameters
    ----------
    db_file: str
        The filename of the sqlite db file
    zoom: int
        The zoom level
    tile_x_pos: int
        The x position of the first tile
    numx: int
        The width of the block of tiles to retrieve

    Returns
    -------
    tiles: {pos: tile_value}
        A set of tiles, indexed by position
    '''
    tileset_info = get_2d_tileset_info(db_file)

    conn = sqlite3.connect(db_file)

    c = conn.cursor()
    tile_width = tileset_info['max_width'] / 2 ** zoom

    tile_x_start_pos = tile_width * tile_x_pos
    tile_x_end_pos = tile_x_start_pos + (numx * tile_width)

    print('tile_x_start:', tile_x_start_pos, tile_x_end_pos)

    query = '''
    SELECT fromX, toX, fromY, toY, chrOffset, importance, fields, uid
    FROM intervals,position_index
    WHERE
        intervals.id=position_index.id AND
        zoomLevel <= {} AND
        rToX >= {} AND
        rFromX <= {}
    '''.format(
        zoom,
        tile_x_start_pos,
        tile_x_end_pos,
    )

    rows = c.execute(query).fetchall()

    new_rows = col.defaultdict(list)
    print("len(rows)", len(rows))

    for r in rows:
        try:
            uid = r[7].decode('utf-8')
        except AttributeError:
            uid = r[7]

        x_start = r[0]
        x_end = r[1]
        y_start = r[2]
        y_end = r[3]

        for i in range(tile_x_pos, tile_x_pos + numx):
            tile_x_start = i * tile_width
            tile_x_end = (i+1) * tile_width

            if (
                x_start < tile_x_end and
                x_end >= tile_x_start
            ):
                # add the position offset to the returned values
                new_rows[i] += [
                    {'xStart': r[0],
                     'xEnd': r[1],
                     'yStart': r[2],
                     'yEnd': r[3],
                     'chrOffset': r[4],
                     'importance': r[5],
                     'uid': uid,
                     'fields': r[6].split('\t')}]
    conn.close()

    return new_rows
