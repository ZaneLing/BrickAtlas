"""Explicit semantic selections; never select a module by nearest-neighbour crop."""
WHOLE = [
    dict(id='whole-4018', model='v23-4018', title='完整小船', object='一艘带驾驶舱的小船'),
    dict(id='whole-4016', model='r-omr-4016-1', title='完整小赛车', object='一辆四轮小赛车'),
    dict(id='whole-4017', model='r-omr-4017-1', title='完整海上直升机', object='一架带旋翼的海上直升机'),
    dict(id='whole-4019', model='r-omr-4019-1', title='完整小飞机', object='一架有机翼和尾翼的小飞机'),
    dict(id='whole-4037', model='r-omr-4037-1', title='完整迷你直升机', object='一架完整的迷你直升机'),
    dict(id='whole-4903', model='r-omr-4903-1', title='完整小狮子', object='一只小狮子'),
    dict(id='whole-4904', model='r-omr-4904-1', title='完整小象', object='一只有长鼻子的小象'),
    dict(id='whole-4905', model='r-omr-4905-1', title='完整长颈鹿', object='一只长颈鹿'),
    dict(id='whole-4906', model='r-omr-4906-1', title='完整微型直升机', object='一架完整的微型直升机'),
    dict(id='whole-4002', model='r-omr-4002-1', title='完整快艇', object='一艘快艇'),
    dict(id='whole-4005', model='r-omr-4005-1', title='完整拖船', object='一艘有船舱的拖船'),
    dict(id='whole-30023', model='v23-30023', title='完整灯塔', object='一座带底座和塔灯的灯塔'),
    dict(id='whole-30022', model='v23-30022', title='完整蜜蜂', object='一只带翅膀和触角的蜜蜂'),
    dict(id='whole-1633', model='v23-1633', title='完整铲车', object='一辆带铲斗的装载车'),
    dict(id='whole-1632', model='v23-1632', title='完整摩托艇', object='一艘摩托艇'),
    dict(id='whole-3223', model='v23-3223', title='完整小鱼', object='一条带尾鳍的小鱼'),
    dict(id='whole-30472', model='v23-30472', title='完整鹦鹉', object='一只鹦鹉'),
]

# Existing hand-selected modules retain their complete, unchanged source scene.
# Every selected part has a documented role in a visible finishing operation.
MODULE_IDS = ['cottage-roof', 'racer-top', 'seaplane-tail', 'museum-roof',
              'repair-truck-cab', 'orange-helicopter-tail', 'police-helicopter-top',
              'panda-head', 'burger-stand-roof', 'white-house-roof',
              'rockefeller-crown', 'brandenburg-top']
