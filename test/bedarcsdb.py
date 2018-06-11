import hgtiles.bedarcsdb as hgbad
import os.path as op

def test_bedarcsdb_tiles():
    '''
    Retrieve a 1D tile from a 2d file
    '''
    filename = op.join('data', 'arrowhead_domains_short.txt.multires.db')

    pos = 0
    data = hgbad.tiles(filename, ["b.0.{}".format(pos)])
    print('data:', data)

    pass
