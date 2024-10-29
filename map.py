import numpy as np
from dataclasses import dataclass


@dataclass
class Connection:
    start: int
    end: int
    is_indoor: bool
    stairs: int  # positive for up, negative for down
    road_crossings: int
positions = np.array([
        [1765, 752],  # 0: Lee Wee Nam Lib
        [1765, 790],  # 1:
        [1391, 803],  # 2:
        [1375, 760],  # 3:
        [1300, 795],  # 4:
        [1276, 815],  # 5:
        [1250, 826],  # 6
        [1227, 846],  # 7
        [1066, 907],  # 8
        [836, 935],  # 9
        [836, 980],  # 10
        [813, 980],  # 11
        [813, 936],  # 12
        [595, 947],  # 13
        [477, 942],  # 14
        [388, 906],  # 15
        [253, 768],  # 16
        [272, 758],  # 17
        [231, 660],  # 18
        [223, 645],  # 19
        [217, 609],  # 20
        [420, 553],  # 21
        [455, 367],  # 22: NIE Lib
        [458, 164],  # 23
        [1719, 156],  # 24
        [1854, 151],  # 25
        [1942, 72],  # 26
        [2085, 205],  # 27
        [2107, 274],  # 28
        [2038, 346],  # 29
        [1746, 509],  # 30
        [1756, 532],  # 31
        [1788, 512],  # 32
        [1868, 728],  # 33
        [1284, 779],  # 34
        [1259, 796],  # 35
        [1212, 578],  # 36
        [1164, 383],  # 37
        [508, 554],   # 38
    ])

# Connection(nodeA, nodeB, is_indoor, stair_count, cross_road)
connections = [
    Connection(0, 1, True, 0, 0),
    Connection(1, 2, True, 0, 0),
    Connection(2, 3, True, 0, 0),
    Connection(3, 4, False, 0, 0),
    Connection(4, 5, False, 0, 1),
    Connection(5, 6, False, 0, 0),
    Connection(6, 7, False, 0, 1),
    Connection(7, 8, False, 0, 0),
    Connection(8, 9, False, 0, 0),
    Connection(9, 10, False, 0, 0),
    Connection(10, 11, False, 0, 1),
    Connection(11, 12, False, 0, 0),
    Connection(12, 13, False, 0, 0),
    Connection(13, 14, False, 0, 0),
    Connection(14, 15, False, 0, 0),
    Connection(15, 16, False, 0, 0),
    Connection(16, 17, False, 0, 1),
    Connection(17, 18, False, 0, 0),
    Connection(18, 19, False, 0, 1),
    Connection(19, 20, False, 0, 0),
    Connection(20, 21, False, 60, 0),   # Stair near NIE Lib
    Connection(21, 22, True, 0, 0),
    Connection(22, 23, True, 0, 0),
    Connection(23, 24, True, 0, 0),
    Connection(24, 25, False, 0, 0),
    Connection(25, 26, True, -20, 0),  # Stair to NIE
    Connection(26, 27, False, 0, 0),
    Connection(27, 28, False, 0, 0),
    Connection(28, 29, False, 0, 0),
    Connection(29, 30, False, 0, 0),
    Connection(30, 31, False, 0, 1),
    Connection(31, 32, True, 0, 0),
    Connection(32, 33, True, 0, 0),
    Connection(33, 1, True, 0, 0),
    Connection(4, 34, False, 0, 1),
    Connection(34, 35, False, 0, 0),
    Connection(35, 36, False, 0, 0),
    Connection(36, 37, True, 0, 0),
    Connection(37, 38, True, 0, 0),
    Connection(38, 22, True, 0, 0),

]
