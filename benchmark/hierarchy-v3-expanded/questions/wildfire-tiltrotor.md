## D3 山火救援倾转旋翼机

### 模块识别（h3-wildfire-tiltrotor-identify）

高亮的维修模块对应哪个 ID？

能力：模块识别；形式：single-choice；证据：model-state。

- A：nacelle-left
- B：rotor-left
- C：water-tank
- D：fuselage

```json
{
  "input": {
    "moduleNames": [
      {
        "id": "fuselage",
        "name": "Firefighting tiltrotor fuselage"
      },
      {
        "id": "nacelle-left",
        "name": "Left tilting nacelle"
      },
      {
        "id": "rotor-left",
        "name": "Left rotor"
      },
      {
        "id": "nacelle-right",
        "name": "Right tilting nacelle"
      },
      {
        "id": "rotor-right",
        "name": "Right rotor"
      },
      {
        "id": "water-tank",
        "name": "Removable water tank"
      }
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 部件计数（h3-wildfire-tiltrotor-count）

模块 water-tank 有多少个可视零件？

能力：部件计数；形式：single-choice；证据：model-state。

- A：5
- B：6
- C：4
- D：8

```json
{
  "input": {
    "parts": [
      {
        "id": "v0001",
        "moduleId": "fuselage",
        "shape": "brick",
        "color": "#d43a32"
      },
      {
        "id": "v0002",
        "moduleId": "fuselage",
        "shape": "brick",
        "color": "#d43a32"
      },
      {
        "id": "v0003",
        "moduleId": "fuselage",
        "shape": "slope",
        "color": "#d43a32"
      },
      {
        "id": "v0004",
        "moduleId": "fuselage",
        "shape": "brick",
        "color": "#d43a32"
      },
      {
        "id": "v0005",
        "moduleId": "fuselage",
        "shape": "brick",
        "color": "#d43a32"
      },
      {
        "id": "v0006",
        "moduleId": "fuselage",
        "shape": "slope",
        "color": "#d43a32"
      },
      {
        "id": "v0007",
        "moduleId": "fuselage",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0008",
        "moduleId": "fuselage",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0009",
        "moduleId": "fuselage",
        "shape": "slope",
        "color": "#d43a32"
      },
      {
        "id": "v0010",
        "moduleId": "fuselage",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0011",
        "moduleId": "fuselage",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0012",
        "moduleId": "fuselage",
        "shape": "slope",
        "color": "#d43a32"
      },
      {
        "id": "v0013",
        "moduleId": "fuselage",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0014",
        "moduleId": "fuselage",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0015",
        "moduleId": "fuselage",
        "shape": "slope",
        "color": "#d43a32"
      },
      {
        "id": "v0016",
        "moduleId": "fuselage",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0017",
        "moduleId": "fuselage",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0018",
        "moduleId": "fuselage",
        "shape": "window",
        "color": "#79c7d8"
      },
      {
        "id": "v0019",
        "moduleId": "fuselage",
        "shape": "panel",
        "color": "#d43a32"
      },
      {
        "id": "v0020",
        "moduleId": "fuselage",
        "shape": "beam",
        "color": "#edf1f2"
      },
      {
        "id": "v0021",
        "moduleId": "fuselage",
        "shape": "beam",
        "color": "#edf1f2"
      },
      {
        "id": "v0022",
        "moduleId": "fuselage",
        "shape": "beam",
        "color": "#edf1f2"
      },
      {
        "id": "v0023",
        "moduleId": "fuselage",
        "shape": "beam",
        "color": "#edf1f2"
      },
      {
        "id": "v0024",
        "moduleId": "fuselage",
        "shape": "beam",
        "color": "#edf1f2"
      },
      {
        "id": "v0025",
        "moduleId": "fuselage",
        "shape": "beam",
        "color": "#edf1f2"
      },
      {
        "id": "v0026",
        "moduleId": "fuselage",
        "shape": "panel",
        "color": "#d43a32"
      },
      {
        "id": "v0027",
        "moduleId": "nacelle-left",
        "shape": "cylinder",
        "color": "#26323b"
      },
      {
        "id": "v0028",
        "moduleId": "nacelle-left",
        "shape": "gear",
        "color": "#e8792e"
      },
      {
        "id": "v0029",
        "moduleId": "rotor-left",
        "shape": "axle",
        "color": "#c6cdd2"
      },
      {
        "id": "v0030",
        "moduleId": "rotor-left",
        "shape": "beam",
        "color": "#101820"
      },
      {
        "id": "v0031",
        "moduleId": "rotor-left",
        "shape": "beam",
        "color": "#101820"
      },
      {
        "id": "v0032",
        "moduleId": "rotor-left",
        "shape": "gear",
        "color": "#f2bf3c"
      },
      {
        "id": "v0033",
        "moduleId": "nacelle-right",
        "shape": "cylinder",
        "color": "#26323b"
      },
      {
        "id": "v0034",
        "moduleId": "nacelle-right",
        "shape": "gear",
        "color": "#e8792e"
      },
      {
        "id": "v0035",
        "moduleId": "rotor-right",
        "shape": "axle",
        "color": "#c6cdd2"
      },
      {
        "id": "v0036",
        "moduleId": "rotor-right",
        "shape": "beam",
        "color": "#101820"
      },
      {
        "id": "v0037",
        "moduleId": "rotor-right",
        "shape": "beam",
        "color": "#101820"
      },
      {
        "id": "v0038",
        "moduleId": "rotor-right",
        "shape": "gear",
        "color": "#f2bf3c"
      },
      {
        "id": "v0039",
        "moduleId": "water-tank",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "v0040",
        "moduleId": "water-tank",
        "shape": "plate",
        "color": "#c6cdd2"
      },
      {
        "id": "v0041",
        "moduleId": "water-tank",
        "shape": "plate",
        "color": "#c6cdd2"
      },
      {
        "id": "v0042",
        "moduleId": "water-tank",
        "shape": "plate",
        "color": "#c6cdd2"
      },
      {
        "id": "v0043",
        "moduleId": "water-tank",
        "shape": "plate",
        "color": "#c6cdd2"
      }
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 颜色识别（h3-wildfire-tiltrotor-color）

零件 v0039 的颜色值是什么？

能力：颜色识别；形式：single-choice；证据：model-state。

- A：#d43a32
- B：#f2bf3c
- C：#26323b
- D：#2878b8

```json
{
  "input": {
    "part": {
      "id": "v0039",
      "moduleId": "water-tank",
      "shape": "panel",
      "size": [
        3.2,
        1.4,
        4
      ],
      "position": [
        0,
        -0.20000000000000007,
        0
      ],
      "rotation": [
        0,
        0,
        0,
        1
      ],
      "color": "#2878b8"
    }
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 三维位置（h3-wildfire-tiltrotor-position）

模块 water-tank 的世界包围盒中心是什么？

能力：三维位置；形式：single-choice；证据：model-state。

- A：[-5.7,3.6,-0.20000000000000007]
- B：[-4.8,5.345,-0.20000000000000018]
- C：[0,1.9000000000000004,0.7999999999999999]
- D：[0,3.9639201731620024,1.3168942074233891]

```json
{
  "input": {
    "centers": {
      "fuselage": [
        0,
        3.9639201731620024,
        1.3168942074233891
      ],
      "nacelle-left": [
        -5.7,
        3.6,
        -0.20000000000000007
      ],
      "rotor-left": [
        -4.8,
        5.345,
        -0.20000000000000018
      ],
      "nacelle-right": [
        5.7,
        3.6,
        -0.20000000000000007
      ],
      "rotor-right": [
        4.8,
        5.345,
        -0.20000000000000018
      ],
      "water-tank": [
        0,
        1.9000000000000004,
        0.7999999999999999
      ]
    }
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 关节类型（h3-wildfire-tiltrotor-joint-type）

nacelle-left-tilt 采用什么约束类型？

能力：关节类型；形式：single-choice；证据：model-state。

- A：prismatic
- B：spring
- C：revolute
- D：fixed

```json
{
  "input": {
    "joint": {
      "id": "nacelle-left-tilt",
      "name": "nacelle-left tilt hinge",
      "type": "revolute",
      "parent": "fuselage",
      "child": "nacelle-left",
      "anchorParent": [
        -5.7,
        -0.363920173162002,
        -1.516894207423389
      ],
      "anchorChild": [
        0,
        0,
        0
      ],
      "axis": [
        0,
        0,
        1
      ],
      "limits": [
        0,
        1.5707963267948966
      ]
    }
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 直接连接（h3-wildfire-tiltrotor-parent）

water-tank 的直接父模块集合是什么？

能力：直接连接；形式：single-choice；证据：model-state。

- A：["fuselage","nacelle-left","rotor-left","nacelle-right","rotor-right","water-tank"]
- B：["fuselage"]
- C：["water-tank"]
- D：[]

```json
{
  "input": {
    "joints": [
      {
        "id": "nacelle-left-tilt",
        "name": "nacelle-left tilt hinge",
        "type": "revolute",
        "parent": "fuselage",
        "child": "nacelle-left",
        "anchorParent": [
          -5.7,
          -0.363920173162002,
          -1.516894207423389
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          0,
          1.5707963267948966
        ]
      },
      {
        "id": "rotor-left-shaft",
        "name": "rotor-left shaft",
        "type": "revolute",
        "parent": "nacelle-left",
        "child": "rotor-left",
        "anchorParent": [
          0.9,
          1.5,
          0
        ],
        "anchorChild": [
          0,
          -0.24500000000000005,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "nacelle-right-tilt",
        "name": "nacelle-right tilt hinge",
        "type": "revolute",
        "parent": "fuselage",
        "child": "nacelle-right",
        "anchorParent": [
          5.7,
          -0.363920173162002,
          -1.516894207423389
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          0,
          1.5707963267948966
        ]
      },
      {
        "id": "rotor-right-shaft",
        "name": "rotor-right shaft",
        "type": "revolute",
        "parent": "nacelle-right",
        "child": "rotor-right",
        "anchorParent": [
          -0.9,
          1.5,
          0
        ],
        "anchorChild": [
          0,
          -0.24500000000000005,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "tank-latch",
        "name": "Water tank latch",
        "type": "fixed",
        "parent": "fuselage",
        "child": "water-tank",
        "anchorParent": [
          0,
          -2.263920173162002,
          -0.5168942074233891
        ],
        "anchorChild": [
          0,
          -0.20000000000000007,
          0
        ]
      }
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 基座识别（h3-wildfire-tiltrotor-anchor）

哪些模块被声明为固定基座？

能力：基座识别；形式：single-choice；证据：model-state。

- A：[]
- B：["fuselage","nacelle-left","rotor-left","nacelle-right","rotor-right","water-tank"]
- C：["water-tank"]
- D：["fuselage"]

```json
{
  "input": {
    "modules": [
      {
        "id": "fuselage",
        "name": "Firefighting tiltrotor fuselage",
        "role": "airframe",
        "anchored": true,
        "mass": 22,
        "position": [
          0,
          3.963920173162002,
          1.3168942074233891
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "nacelle-left",
        "name": "Left tilting nacelle",
        "role": "actuator",
        "anchored": false,
        "mass": 3.2,
        "position": [
          -5.7,
          3.6,
          -0.2
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "rotor-left",
        "name": "Left rotor",
        "role": "rotor",
        "anchored": false,
        "mass": 1.5,
        "position": [
          -4.8,
          5.345,
          -0.2
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "nacelle-right",
        "name": "Right tilting nacelle",
        "role": "actuator",
        "anchored": false,
        "mass": 3.2,
        "position": [
          5.7,
          3.6,
          -0.2
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "rotor-right",
        "name": "Right rotor",
        "role": "rotor",
        "anchored": false,
        "mass": 1.5,
        "position": [
          4.8,
          5.345,
          -0.2
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "water-tank",
        "name": "Removable water tank",
        "role": "service-module",
        "anchored": false,
        "mass": 6,
        "position": [
          0,
          1.9000000000000004,
          0.8
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      }
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 接口计数（h3-wildfire-tiltrotor-degree）

water-tank 连接几个声明关节？平行关节分别计数。

能力：接口计数；形式：single-choice；证据：model-state。

- A：3
- B：1
- C：2
- D：0

```json
{
  "input": {
    "joints": [
      {
        "id": "nacelle-left-tilt",
        "name": "nacelle-left tilt hinge",
        "type": "revolute",
        "parent": "fuselage",
        "child": "nacelle-left",
        "anchorParent": [
          -5.7,
          -0.363920173162002,
          -1.516894207423389
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          0,
          1.5707963267948966
        ]
      },
      {
        "id": "rotor-left-shaft",
        "name": "rotor-left shaft",
        "type": "revolute",
        "parent": "nacelle-left",
        "child": "rotor-left",
        "anchorParent": [
          0.9,
          1.5,
          0
        ],
        "anchorChild": [
          0,
          -0.24500000000000005,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "nacelle-right-tilt",
        "name": "nacelle-right tilt hinge",
        "type": "revolute",
        "parent": "fuselage",
        "child": "nacelle-right",
        "anchorParent": [
          5.7,
          -0.363920173162002,
          -1.516894207423389
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          0,
          1.5707963267948966
        ]
      },
      {
        "id": "rotor-right-shaft",
        "name": "rotor-right shaft",
        "type": "revolute",
        "parent": "nacelle-right",
        "child": "rotor-right",
        "anchorParent": [
          -0.9,
          1.5,
          0
        ],
        "anchorChild": [
          0,
          -0.24500000000000005,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "tank-latch",
        "name": "Water tank latch",
        "type": "fixed",
        "parent": "fuselage",
        "child": "water-tank",
        "anchorParent": [
          0,
          -2.263920173162002,
          -0.5168942074233891
        ],
        "anchorChild": [
          0,
          -0.20000000000000007,
          0
        ]
      }
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 局部改色（h3-wildfire-tiltrotor-recolor）

仅将 v0039 改成 #e8792e，其他零件不变。选择正确补丁。

能力：局部改色；形式：single-choice；证据：model-state。

- A：{"id":"v0040","color":"#e8792e"}
- B：{"id":"v0039","color":"#2878b8"}
- C：{"id":"*","color":"#e8792e"}
- D：{"id":"v0039","color":"#e8792e"}

```json
{
  "input": {
    "part": {
      "id": "v0039",
      "moduleId": "water-tank",
      "shape": "panel",
      "size": [
        3.2,
        1.4,
        4
      ],
      "position": [
        0,
        -0.20000000000000007,
        0
      ],
      "rotation": [
        0,
        0,
        0,
        1
      ],
      "color": "#2878b8"
    }
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 补装部件（h3-wildfire-tiltrotor-add）

模块 water-tank 缺失零件 v0039。选择与目标清单一致的补装描述。

能力：补装部件；形式：single-choice；证据：model-state。

- A：{"id":"v0039","moduleId":"water-tank","shape":"panel","size":[3.2,1.4,4],"position":[0,-0.20000000000000007,0],"rotation":[0,0,0,1],"color":"#000000"}
- B：{"id":"v0039","moduleId":"water-tank","shape":"panel","size":[3.2,1.4,4],"position":[0,-0.20000000000000007,0],"rotation":[0,0,0,1],"color":"#2878b8"}
- C：{"id":"v0039","moduleId":"fuselage","shape":"panel","size":[3.2,1.4,4],"position":[0,-0.20000000000000007,0],"rotation":[0,0,0,1],"color":"#2878b8"}
- D：{"id":"v0039","moduleId":"water-tank","shape":"panel","size":[3,3,3],"position":[0,-0.20000000000000007,0],"rotation":[0,0,0,1],"color":"#2878b8"}

```json
{
  "input": {
    "targetPart": {
      "id": "v0039",
      "moduleId": "water-tank",
      "shape": "panel",
      "size": [
        3.2,
        1.4,
        4
      ],
      "position": [
        0,
        -0.20000000000000007,
        0
      ],
      "rotation": [
        0,
        0,
        0,
        1
      ],
      "color": "#2878b8"
    },
    "existingIds": [
      "v0001",
      "v0002",
      "v0003",
      "v0004",
      "v0005",
      "v0006",
      "v0007",
      "v0008",
      "v0009",
      "v0010",
      "v0011",
      "v0012",
      "v0013",
      "v0014",
      "v0015",
      "v0016",
      "v0017",
      "v0018",
      "v0019",
      "v0020",
      "v0021",
      "v0022",
      "v0023",
      "v0024",
      "v0025",
      "v0026",
      "v0027",
      "v0028",
      "v0029",
      "v0030",
      "v0031",
      "v0032",
      "v0033",
      "v0034",
      "v0035",
      "v0036",
      "v0037",
      "v0038",
      "v0040",
      "v0041",
      "v0042",
      "v0043"
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 安全拆除（h3-wildfire-tiltrotor-remove）

按声明依赖图，当前可以先拆哪些叶模块？

能力：安全拆除；形式：single-choice；证据：model-state。

- A：["rotor-left","rotor-right","water-tank"]
- B：["fuselage"]
- C：[]
- D：["fuselage","nacelle-left","rotor-left","nacelle-right","rotor-right","water-tank"]

```json
{
  "input": {
    "joints": [
      {
        "id": "nacelle-left-tilt",
        "name": "nacelle-left tilt hinge",
        "type": "revolute",
        "parent": "fuselage",
        "child": "nacelle-left",
        "anchorParent": [
          -5.7,
          -0.363920173162002,
          -1.516894207423389
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          0,
          1.5707963267948966
        ]
      },
      {
        "id": "rotor-left-shaft",
        "name": "rotor-left shaft",
        "type": "revolute",
        "parent": "nacelle-left",
        "child": "rotor-left",
        "anchorParent": [
          0.9,
          1.5,
          0
        ],
        "anchorChild": [
          0,
          -0.24500000000000005,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "nacelle-right-tilt",
        "name": "nacelle-right tilt hinge",
        "type": "revolute",
        "parent": "fuselage",
        "child": "nacelle-right",
        "anchorParent": [
          5.7,
          -0.363920173162002,
          -1.516894207423389
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          0,
          1.5707963267948966
        ]
      },
      {
        "id": "rotor-right-shaft",
        "name": "rotor-right shaft",
        "type": "revolute",
        "parent": "nacelle-right",
        "child": "rotor-right",
        "anchorParent": [
          -0.9,
          1.5,
          0
        ],
        "anchorChild": [
          0,
          -0.24500000000000005,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "tank-latch",
        "name": "Water tank latch",
        "type": "fixed",
        "parent": "fuselage",
        "child": "water-tank",
        "anchorParent": [
          0,
          -2.263920173162002,
          -0.5168942074233891
        ],
        "anchorChild": [
          0,
          -0.20000000000000007,
          0
        ]
      }
    ],
    "modules": [
      "fuselage",
      "nacelle-left",
      "rotor-left",
      "nacelle-right",
      "rotor-right",
      "water-tank"
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 替换选择（h3-wildfire-tiltrotor-replace）

在成本上限内选择刚度最大的替换件；并列选成本低者，再并列选ID字典序最小者。

能力：替换选择；形式：single-choice；证据：model-state。

- A：stock-3
- B：stock-0
- C：stock-1
- D：stock-2

```json
{
  "input": {
    "alternatives": [
      {
        "id": "stock-0",
        "cost": 3,
        "stiffness": 8,
        "mass": 0.7
      },
      {
        "id": "stock-1",
        "cost": 2,
        "stiffness": 3,
        "mass": 0.7
      },
      {
        "id": "stock-2",
        "cost": 3,
        "stiffness": 4,
        "mass": 0.8
      },
      {
        "id": "stock-3",
        "cost": 2,
        "stiffness": 9,
        "mass": 1.4
      }
    ],
    "maxCost": 6
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 平移纠偏（h3-wildfire-tiltrotor-translate）

观察到相对目标的平移误差 delta，选择补偿平移。

能力：平移纠偏；形式：single-choice；证据：model-state。

- A：[0,0,0]
- B：[0,2,0]
- C：[-3,0,2]
- D：[3,0,-2]

```json
{
  "input": {
    "delta": [
      3,
      0,
      -2
    ],
    "target": "water-tank"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 姿态纠偏（h3-wildfire-tiltrotor-rotate）

选择从当前yaw到目标yaw的最短有符号旋转；恰好180°时使用-180°。

能力：姿态纠偏；形式：single-choice；证据：model-state。

- A：90
- B：45
- C：-45
- D：0

```json
{
  "input": {
    "module": "water-tank",
    "currentYaw": 135,
    "targetYaw": 180
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 下一步放置（h3-wildfire-tiltrotor-next-module）

已完成给定前缀，选择所有前置依赖已满足的下一模块集合。

能力：下一步放置；形式：single-choice；证据：model-state。

- A：["fuselage","water-tank","nacelle-left"]
- B：["rotor-left","nacelle-right","rotor-right"]
- C：["nacelle-right","rotor-left"]
- D：[]

```json
{
  "input": {
    "prefix": [
      "fuselage",
      "water-tank",
      "nacelle-left"
    ],
    "joints": [
      {
        "id": "nacelle-left-tilt",
        "name": "nacelle-left tilt hinge",
        "type": "revolute",
        "parent": "fuselage",
        "child": "nacelle-left",
        "anchorParent": [
          -5.7,
          -0.363920173162002,
          -1.516894207423389
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          0,
          1.5707963267948966
        ]
      },
      {
        "id": "rotor-left-shaft",
        "name": "rotor-left shaft",
        "type": "revolute",
        "parent": "nacelle-left",
        "child": "rotor-left",
        "anchorParent": [
          0.9,
          1.5,
          0
        ],
        "anchorChild": [
          0,
          -0.24500000000000005,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "nacelle-right-tilt",
        "name": "nacelle-right tilt hinge",
        "type": "revolute",
        "parent": "fuselage",
        "child": "nacelle-right",
        "anchorParent": [
          5.7,
          -0.363920173162002,
          -1.516894207423389
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          0,
          1.5707963267948966
        ]
      },
      {
        "id": "rotor-right-shaft",
        "name": "rotor-right shaft",
        "type": "revolute",
        "parent": "nacelle-right",
        "child": "rotor-right",
        "anchorParent": [
          -0.9,
          1.5,
          0
        ],
        "anchorChild": [
          0,
          -0.24500000000000005,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "tank-latch",
        "name": "Water tank latch",
        "type": "fixed",
        "parent": "fuselage",
        "child": "water-tank",
        "anchorParent": [
          0,
          -2.263920173162002,
          -0.5168942074233891
        ],
        "anchorChild": [
          0,
          -0.20000000000000007,
          0
        ]
      }
    ],
    "modules": [
      "fuselage",
      "nacelle-left",
      "rotor-left",
      "nacelle-right",
      "rotor-right",
      "water-tank"
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 库存核算（h3-wildfire-tiltrotor-inventory）

备件库有 8 件，替换模块需 5 件，还剩多少？

能力：库存核算；形式：single-choice；证据：model-state。

- A：6
- B：3
- C：4
- D：2

```json
{
  "input": {
    "available": 8,
    "required": 5
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 子装配边界（h3-wildfire-tiltrotor-boundary）

隔离 water-tank 需要断开哪些边界关节？

能力：子装配边界；形式：single-choice；证据：model-state。

- A：[]
- B：["nacelle-left-tilt","rotor-left-shaft","nacelle-right-tilt","rotor-right-shaft","tank-latch"]
- C：["nacelle-left-tilt"]
- D：["tank-latch"]

```json
{
  "input": {
    "joints": [
      {
        "id": "nacelle-left-tilt",
        "name": "nacelle-left tilt hinge",
        "type": "revolute",
        "parent": "fuselage",
        "child": "nacelle-left",
        "anchorParent": [
          -5.7,
          -0.363920173162002,
          -1.516894207423389
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          0,
          1.5707963267948966
        ]
      },
      {
        "id": "rotor-left-shaft",
        "name": "rotor-left shaft",
        "type": "revolute",
        "parent": "nacelle-left",
        "child": "rotor-left",
        "anchorParent": [
          0.9,
          1.5,
          0
        ],
        "anchorChild": [
          0,
          -0.24500000000000005,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "nacelle-right-tilt",
        "name": "nacelle-right tilt hinge",
        "type": "revolute",
        "parent": "fuselage",
        "child": "nacelle-right",
        "anchorParent": [
          5.7,
          -0.363920173162002,
          -1.516894207423389
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          0,
          1.5707963267948966
        ]
      },
      {
        "id": "rotor-right-shaft",
        "name": "rotor-right shaft",
        "type": "revolute",
        "parent": "nacelle-right",
        "child": "rotor-right",
        "anchorParent": [
          -0.9,
          1.5,
          0
        ],
        "anchorChild": [
          0,
          -0.24500000000000005,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "tank-latch",
        "name": "Water tank latch",
        "type": "fixed",
        "parent": "fuselage",
        "child": "water-tank",
        "anchorParent": [
          0,
          -2.263920173162002,
          -0.5168942074233891
        ],
        "anchorChild": [
          0,
          -0.20000000000000007,
          0
        ]
      }
    ],
    "target": "water-tank"
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 最小干预（h3-wildfire-tiltrotor-no-op）

当前模块颜色已满足指令，且无需改变位姿。最少需要几次编辑？

能力：最小干预；形式：single-choice；证据：model-state。

- A：1
- B：2
- C：5
- D：0

```json
{
  "input": {
    "module": "water-tank"
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 全过程依赖（h3-wildfire-tiltrotor-prefix）

给定候选顺序，首次违反前置依赖的步骤是？从 0 编号，-1 表示没有违反。

能力：全过程依赖；形式：single-choice；证据：support-graph。

- A：-1
- B：1
- C：5
- D：0

```json
{
  "input": {
    "order": [
      "nacelle-left",
      "fuselage",
      "water-tank",
      "nacelle-right",
      "rotor-left",
      "rotor-right"
    ],
    "joints": [
      {
        "id": "nacelle-left-tilt",
        "name": "nacelle-left tilt hinge",
        "type": "revolute",
        "parent": "fuselage",
        "child": "nacelle-left",
        "anchorParent": [
          -5.7,
          -0.363920173162002,
          -1.516894207423389
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          0,
          1.5707963267948966
        ]
      },
      {
        "id": "rotor-left-shaft",
        "name": "rotor-left shaft",
        "type": "revolute",
        "parent": "nacelle-left",
        "child": "rotor-left",
        "anchorParent": [
          0.9,
          1.5,
          0
        ],
        "anchorChild": [
          0,
          -0.24500000000000005,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "nacelle-right-tilt",
        "name": "nacelle-right tilt hinge",
        "type": "revolute",
        "parent": "fuselage",
        "child": "nacelle-right",
        "anchorParent": [
          5.7,
          -0.363920173162002,
          -1.516894207423389
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          0,
          1.5707963267948966
        ]
      },
      {
        "id": "rotor-right-shaft",
        "name": "rotor-right shaft",
        "type": "revolute",
        "parent": "nacelle-right",
        "child": "rotor-right",
        "anchorParent": [
          -0.9,
          1.5,
          0
        ],
        "anchorChild": [
          0,
          -0.24500000000000005,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "tank-latch",
        "name": "Water tank latch",
        "type": "fixed",
        "parent": "fuselage",
        "child": "water-tank",
        "anchorParent": [
          0,
          -2.263920173162002,
          -0.5168942074233891
        ],
        "anchorChild": [
          0,
          -0.20000000000000007,
          0
        ]
      }
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 连续维修路径（h3-wildfire-tiltrotor-access）

根据实际 Rapier shape cast 记录，选择全部无碰撞路径。

能力：连续维修路径；形式：multiple-choice；证据：Rapier。

- A：path-1
- B：path-0
- C：path-2

```json
{
  "input": {
    "paths": [
      {
        "id": "path-0",
        "start": [
          12.4,
          1.9000000000000004,
          0.7999999999999999
        ],
        "end": [
          0,
          1.9000000000000004,
          0.7999999999999999
        ],
        "halfExtents": [
          0.18,
          0.18,
          0.18
        ],
        "clear": true,
        "timeOfImpact": null
      },
      {
        "id": "path-1",
        "start": [
          0,
          10.19,
          0.7999999999999999
        ],
        "end": [
          0,
          1.9000000000000004,
          0.7999999999999999
        ],
        "halfExtents": [
          0.18,
          0.18,
          0.18
        ],
        "clear": false,
        "timeOfImpact": 0.6876422166824341
      },
      {
        "id": "path-2",
        "start": [
          0,
          1.9000000000000004,
          10.8
        ],
        "end": [
          0,
          1.9000000000000004,
          0.7999999999999999
        ],
        "halfExtents": [
          0.18,
          0.18,
          0.18
        ],
        "clear": true,
        "timeOfImpact": null
      }
    ],
    "simulator": "stud-inclusive conservative cuboids; anchored base; force-limited position servos; no clutch/material calibration"
  },
  "answer": {
    "choiceIds": [
      "B",
      "C"
    ]
  }
}
```

### 支撑反事实（h3-wildfire-tiltrotor-counterfactual）

移除指定模块后，哪些其余模块失去到任一基座的关节路径？不包含被移除模块本身。

能力：支撑反事实；形式：single-choice；证据：support-graph。

- A：["rotor-left"]
- B：["nacelle-left"]
- C：[]
- D：["fuselage","nacelle-left","rotor-left","nacelle-right","rotor-right","water-tank"]

```json
{
  "input": {
    "removed": "nacelle-left",
    "roots": [
      "fuselage"
    ],
    "joints": [
      {
        "id": "nacelle-left-tilt",
        "name": "nacelle-left tilt hinge",
        "type": "revolute",
        "parent": "fuselage",
        "child": "nacelle-left",
        "anchorParent": [
          -5.7,
          -0.363920173162002,
          -1.516894207423389
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          0,
          1.5707963267948966
        ]
      },
      {
        "id": "rotor-left-shaft",
        "name": "rotor-left shaft",
        "type": "revolute",
        "parent": "nacelle-left",
        "child": "rotor-left",
        "anchorParent": [
          0.9,
          1.5,
          0
        ],
        "anchorChild": [
          0,
          -0.24500000000000005,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "nacelle-right-tilt",
        "name": "nacelle-right tilt hinge",
        "type": "revolute",
        "parent": "fuselage",
        "child": "nacelle-right",
        "anchorParent": [
          5.7,
          -0.363920173162002,
          -1.516894207423389
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          0,
          1.5707963267948966
        ]
      },
      {
        "id": "rotor-right-shaft",
        "name": "rotor-right shaft",
        "type": "revolute",
        "parent": "nacelle-right",
        "child": "rotor-right",
        "anchorParent": [
          -0.9,
          1.5,
          0
        ],
        "anchorChild": [
          0,
          -0.24500000000000005,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "tank-latch",
        "name": "Water tank latch",
        "type": "fixed",
        "parent": "fuselage",
        "child": "water-tank",
        "anchorParent": [
          0,
          -2.263920173162002,
          -0.5168942074233891
        ],
        "anchorChild": [
          0,
          -0.20000000000000007,
          0
        ]
      }
    ],
    "modules": [
      "fuselage",
      "nacelle-left",
      "rotor-left",
      "nacelle-right",
      "rotor-right",
      "water-tank"
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 冲击响应读数（h3-wildfire-tiltrotor-dynamic）

Rapier 实际采样轨迹中的最大平移位移是多少？按四位小数报告。

能力：冲击响应读数；形式：single-choice；证据：Rapier。

- A：1.0074
- B：0.0074
- C：0.2074
- D：0

```json
{
  "input": {
    "trace": [
      {
        "time": 0.008333333333333333,
        "displacement": 0.0073585474047615776
      },
      {
        "time": 0.10833333333333334,
        "displacement": 6.743495761743046e-7
      },
      {
        "time": 0.20833333333333334,
        "displacement": 6.743495761743046e-7
      },
      {
        "time": 0.30833333333333335,
        "displacement": 6.743495761743046e-7
      },
      {
        "time": 0.4083333333333333,
        "displacement": 6.743495761743046e-7
      },
      {
        "time": 0.5083333333333333,
        "displacement": 6.743495761743046e-7
      },
      {
        "time": 0.6083333333333333,
        "displacement": 6.743495761743046e-7
      },
      {
        "time": 0.7083333333333334,
        "displacement": 6.743495761743046e-7
      },
      {
        "time": 0.8083333333333333,
        "displacement": 6.743495761743046e-7
      },
      {
        "time": 0.9083333333333333,
        "displacement": 6.743495761743046e-7
      },
      {
        "time": 1,
        "displacement": 6.743495761743046e-7
      }
    ],
    "impulse": [
      10,
      1.8,
      3.5
    ],
    "nominalDrift": 0.00042901220212066774,
    "scope": "采样轨迹极值，非连续时间极值；不代表实物安全阈值"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 关节限位推理（h3-wildfire-tiltrotor-kinematic）

下列目标位置/角度中哪些在关节声明限位内（含边界）？

能力：关节限位推理；形式：multiple-choice；证据：model-state。

- A：0.7853981633974483
- B：-0.5
- C：2.0707963267948966
- D：0

```json
{
  "input": {
    "joint": "nacelle-left-tilt",
    "limits": [
      0,
      1.5707963267948966
    ],
    "units": "radians"
  },
  "answer": {
    "choiceIds": [
      "A",
      "D"
    ]
  }
}
```

### 约束故障诊断（h3-wildfire-tiltrotor-diagnosis）

已检测到端点和约束类型如下，选择匹配的全部关节。

能力：约束故障诊断；形式：multiple-choice；证据：model-state。

- A：tank-latch
- B：nacelle-left-tilt
- C：rotor-left-shaft
- D：nacelle-right-tilt

```json
{
  "input": {
    "endpoints": [
      "fuselage",
      "water-tank"
    ],
    "type": "fixed",
    "joints": [
      {
        "id": "nacelle-left-tilt",
        "name": "nacelle-left tilt hinge",
        "type": "revolute",
        "parent": "fuselage",
        "child": "nacelle-left",
        "anchorParent": [
          -5.7,
          -0.363920173162002,
          -1.516894207423389
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          0,
          1.5707963267948966
        ]
      },
      {
        "id": "rotor-left-shaft",
        "name": "rotor-left shaft",
        "type": "revolute",
        "parent": "nacelle-left",
        "child": "rotor-left",
        "anchorParent": [
          0.9,
          1.5,
          0
        ],
        "anchorChild": [
          0,
          -0.24500000000000005,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "nacelle-right-tilt",
        "name": "nacelle-right tilt hinge",
        "type": "revolute",
        "parent": "fuselage",
        "child": "nacelle-right",
        "anchorParent": [
          5.7,
          -0.363920173162002,
          -1.516894207423389
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          0,
          1.5707963267948966
        ]
      },
      {
        "id": "rotor-right-shaft",
        "name": "rotor-right shaft",
        "type": "revolute",
        "parent": "nacelle-right",
        "child": "rotor-right",
        "anchorParent": [
          -0.9,
          1.5,
          0
        ],
        "anchorChild": [
          0,
          -0.24500000000000005,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "tank-latch",
        "name": "Water tank latch",
        "type": "fixed",
        "parent": "fuselage",
        "child": "water-tank",
        "anchorParent": [
          0,
          -2.263920173162002,
          -0.5168942074233891
        ],
        "anchorChild": [
          0,
          -0.20000000000000007,
          0
        ]
      }
    ]
  },
  "answer": {
    "choiceIds": [
      "A"
    ]
  }
}
```

### 主动检查收益（h3-wildfire-tiltrotor-information-gain）

均匀先验四个世界，选择信息增益/成本最大的全部检查。

能力：主动检查收益；形式：multiple-choice；证据：finite-world。

- A：query-2
- B：query-0
- C：query-1

```json
{
  "input": {
    "queries": [
      {
        "id": "query-0",
        "cost": 1,
        "returns": [
          0,
          0,
          1,
          1
        ]
      },
      {
        "id": "query-1",
        "cost": 2,
        "returns": [
          0,
          1,
          2,
          3
        ]
      },
      {
        "id": "query-2",
        "cost": 3,
        "returns": [
          0,
          0,
          0,
          1
        ]
      }
    ],
    "module": "water-tank",
    "worlds": [
      "normal",
      "jammed",
      "reversed",
      "loose"
    ]
  },
  "answer": {
    "choiceIds": [
      "B",
      "C"
    ]
  }
}
```

### 不确定性与弃答（h3-wildfire-tiltrotor-abstention）

所有相容世界是否允许同一个后续动作？选择继续执行或请求检查。

能力：不确定性与弃答；形式：single-choice；证据：finite-world。

- A：commit
- B：inspect

```json
{
  "input": {
    "worlds": [
      {
        "id": "w0",
        "action": "continue"
      },
      {
        "id": "w1",
        "action": "continue"
      }
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 观测后信念更新（h3-wildfire-tiltrotor-posterior）

均匀先验，得到给定观测后，jammed 世界的后验概率是多少？

能力：观测后信念更新；形式：single-choice；证据：finite-world。

- A：0
- B：0.25
- C：0.3333333333333333
- D：0.5

```json
{
  "input": {
    "module": "water-tank",
    "worlds": [
      "normal",
      "jammed",
      "reversed",
      "loose"
    ],
    "observationByWorld": [
      "positive",
      "positive",
      "negative",
      "negative"
    ],
    "observed": "negative"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 多目标工程权衡（h3-wildfire-tiltrotor-pareto）

最小成本、最小质量、最大刚度，选择完整非支配集合。

能力：多目标工程权衡；形式：multiple-choice；证据：model-state。

- A：stock-1
- B：stock-3
- C：stock-2
- D：stock-0

```json
{
  "input": {
    "alternatives": [
      {
        "id": "stock-0",
        "cost": 3,
        "stiffness": 8,
        "mass": 0.7
      },
      {
        "id": "stock-1",
        "cost": 2,
        "stiffness": 3,
        "mass": 0.7
      },
      {
        "id": "stock-2",
        "cost": 3,
        "stiffness": 4,
        "mass": 0.8
      },
      {
        "id": "stock-3",
        "cost": 2,
        "stiffness": 9,
        "mass": 1.4
      }
    ]
  },
  "answer": {
    "choiceIds": [
      "A",
      "B",
      "D"
    ]
  }
}
```

### 依赖装配（h3-wildfire-tiltrotor-assembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖装配；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [],
    "initialModules": [],
    "actions": [
      {
        "id": "place:rotor-left",
        "label": "安装 rotor-left",
        "requires": [
          "present:nacelle-left"
        ],
        "forbids": [
          "present:rotor-left"
        ],
        "adds": [
          "present:rotor-left"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rotor-left",
          "visible": true
        }
      },
      {
        "id": "place:rotor-right",
        "label": "安装 rotor-right",
        "requires": [
          "present:nacelle-right"
        ],
        "forbids": [
          "present:rotor-right"
        ],
        "adds": [
          "present:rotor-right"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rotor-right",
          "visible": true
        }
      },
      {
        "id": "place:nacelle-right",
        "label": "安装 nacelle-right",
        "requires": [
          "present:fuselage"
        ],
        "forbids": [
          "present:nacelle-right"
        ],
        "adds": [
          "present:nacelle-right"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "nacelle-right",
          "visible": true
        }
      },
      {
        "id": "place:fuselage",
        "label": "安装 fuselage",
        "requires": [],
        "forbids": [
          "present:fuselage"
        ],
        "adds": [
          "present:fuselage"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "fuselage",
          "visible": true
        }
      },
      {
        "id": "place:nacelle-left",
        "label": "安装 nacelle-left",
        "requires": [
          "present:fuselage"
        ],
        "forbids": [
          "present:nacelle-left"
        ],
        "adds": [
          "present:nacelle-left"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "nacelle-left",
          "visible": true
        }
      },
      {
        "id": "place:water-tank",
        "label": "安装 water-tank",
        "requires": [
          "present:fuselage"
        ],
        "forbids": [
          "present:water-tank"
        ],
        "adds": [
          "present:water-tank"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "water-tank",
          "visible": true
        }
      }
    ],
    "goalFacts": [
      "present:fuselage",
      "present:water-tank",
      "present:nacelle-left",
      "present:nacelle-right",
      "present:rotor-left",
      "present:rotor-right"
    ],
    "budget": 6,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "place:fuselage",
      "place:nacelle-right",
      "place:rotor-right",
      "place:nacelle-left",
      "place:rotor-left",
      "place:water-tank"
    ]
  }
}
```

### 依赖拆解（h3-wildfire-tiltrotor-disassembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖拆解；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "present:fuselage",
      "present:nacelle-left",
      "present:rotor-left",
      "present:nacelle-right",
      "present:rotor-right",
      "present:water-tank"
    ],
    "initialModules": [
      "fuselage",
      "nacelle-left",
      "rotor-left",
      "nacelle-right",
      "rotor-right",
      "water-tank"
    ],
    "actions": [
      {
        "id": "remove:rotor-right",
        "label": "拆除 rotor-right",
        "requires": [
          "present:rotor-right"
        ],
        "forbids": [],
        "adds": [
          "removed:rotor-right"
        ],
        "deletes": [
          "present:rotor-right"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "rotor-right",
          "visible": false
        }
      },
      {
        "id": "remove:water-tank",
        "label": "拆除 water-tank",
        "requires": [
          "present:water-tank"
        ],
        "forbids": [],
        "adds": [
          "removed:water-tank"
        ],
        "deletes": [
          "present:water-tank"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "water-tank",
          "visible": false
        }
      },
      {
        "id": "remove:rotor-left",
        "label": "拆除 rotor-left",
        "requires": [
          "present:rotor-left"
        ],
        "forbids": [],
        "adds": [
          "removed:rotor-left"
        ],
        "deletes": [
          "present:rotor-left"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "rotor-left",
          "visible": false
        }
      },
      {
        "id": "remove:nacelle-right",
        "label": "拆除 nacelle-right",
        "requires": [
          "present:nacelle-right"
        ],
        "forbids": [
          "present:rotor-right"
        ],
        "adds": [
          "removed:nacelle-right"
        ],
        "deletes": [
          "present:nacelle-right"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "nacelle-right",
          "visible": false
        }
      },
      {
        "id": "remove:fuselage",
        "label": "拆除 fuselage",
        "requires": [
          "present:fuselage"
        ],
        "forbids": [
          "present:nacelle-left",
          "present:nacelle-right",
          "present:water-tank"
        ],
        "adds": [
          "removed:fuselage"
        ],
        "deletes": [
          "present:fuselage"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "fuselage",
          "visible": false
        }
      },
      {
        "id": "remove:nacelle-left",
        "label": "拆除 nacelle-left",
        "requires": [
          "present:nacelle-left"
        ],
        "forbids": [
          "present:rotor-left"
        ],
        "adds": [
          "removed:nacelle-left"
        ],
        "deletes": [
          "present:nacelle-left"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "nacelle-left",
          "visible": false
        }
      }
    ],
    "goalFacts": [
      "removed:rotor-right",
      "removed:rotor-left",
      "removed:nacelle-right",
      "removed:nacelle-left",
      "removed:water-tank",
      "removed:fuselage"
    ],
    "budget": 6,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "remove:rotor-right",
      "remove:water-tank",
      "remove:rotor-left",
      "remove:nacelle-right",
      "remove:nacelle-left",
      "remove:fuselage"
    ]
  }
}
```

### 承载维修（h3-wildfire-tiltrotor-service-repair）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：承载维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:water-tank",
      "closed:water-tank"
    ],
    "initialModules": [
      "fuselage",
      "nacelle-left",
      "rotor-left",
      "nacelle-right",
      "rotor-right",
      "water-tank"
    ],
    "actions": [
      {
        "id": "close:water-tank",
        "label": "close water-tank",
        "requires": [
          "done:verify:water-tank"
        ],
        "forbids": [
          "done:close:water-tank"
        ],
        "adds": [
          "done:close:water-tank"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "water-tank"
        }
      },
      {
        "id": "support:water-tank",
        "label": "support water-tank",
        "requires": [
          "fault:water-tank"
        ],
        "forbids": [
          "done:support:water-tank"
        ],
        "adds": [
          "done:support:water-tank"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "water-tank"
        }
      },
      {
        "id": "release:water-tank",
        "label": "release water-tank",
        "requires": [
          "done:close:water-tank"
        ],
        "forbids": [
          "done:release:water-tank"
        ],
        "adds": [
          "done:release:water-tank",
          "repaired:water-tank"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "water-tank"
        }
      },
      {
        "id": "open:water-tank",
        "label": "open water-tank",
        "requires": [
          "done:support:water-tank"
        ],
        "forbids": [
          "done:open:water-tank"
        ],
        "adds": [
          "done:open:water-tank"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "water-tank"
        }
      },
      {
        "id": "remove:water-tank",
        "label": "remove water-tank",
        "requires": [
          "done:open:water-tank"
        ],
        "forbids": [
          "done:remove:water-tank"
        ],
        "adds": [
          "done:remove:water-tank"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "water-tank",
          "visible": false
        }
      },
      {
        "id": "replace:water-tank",
        "label": "replace water-tank",
        "requires": [
          "done:remove:water-tank"
        ],
        "forbids": [
          "done:replace:water-tank"
        ],
        "adds": [
          "done:replace:water-tank"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "water-tank",
          "visible": true
        }
      },
      {
        "id": "verify:water-tank",
        "label": "verify water-tank",
        "requires": [
          "done:replace:water-tank"
        ],
        "forbids": [
          "done:verify:water-tank"
        ],
        "adds": [
          "done:verify:water-tank"
        ],
        "deletes": [
          "fault:water-tank"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "water-tank"
        }
      }
    ],
    "goalFacts": [
      "repaired:water-tank"
    ],
    "budget": 7,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:water-tank",
      "open:water-tank",
      "remove:water-tank",
      "replace:water-tank",
      "verify:water-tank",
      "close:water-tank",
      "release:water-tank"
    ]
  }
}
```

### 复合编辑验证（h3-wildfire-tiltrotor-compound-edit）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：复合编辑验证；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:water-tank",
      "closed:water-tank"
    ],
    "initialModules": [
      "fuselage",
      "nacelle-left",
      "rotor-left",
      "nacelle-right",
      "rotor-right",
      "water-tank"
    ],
    "actions": [
      {
        "id": "close:water-tank",
        "label": "close water-tank",
        "requires": [
          "done:verify:water-tank"
        ],
        "forbids": [
          "done:close:water-tank"
        ],
        "adds": [
          "done:close:water-tank"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "water-tank"
        }
      },
      {
        "id": "support:water-tank",
        "label": "support water-tank",
        "requires": [
          "fault:water-tank"
        ],
        "forbids": [
          "done:support:water-tank"
        ],
        "adds": [
          "done:support:water-tank"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "water-tank"
        }
      },
      {
        "id": "release:water-tank",
        "label": "release water-tank",
        "requires": [
          "done:close:water-tank"
        ],
        "forbids": [
          "done:release:water-tank"
        ],
        "adds": [
          "done:release:water-tank",
          "repaired:water-tank"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "water-tank"
        }
      },
      {
        "id": "open:water-tank",
        "label": "open water-tank",
        "requires": [
          "done:support:water-tank"
        ],
        "forbids": [
          "done:open:water-tank"
        ],
        "adds": [
          "done:open:water-tank"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "water-tank"
        }
      },
      {
        "id": "verify:water-tank",
        "label": "verify water-tank",
        "requires": [
          "done:recolor:water-tank"
        ],
        "forbids": [
          "done:verify:water-tank"
        ],
        "adds": [
          "done:verify:water-tank"
        ],
        "deletes": [
          "fault:water-tank"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "water-tank"
        }
      },
      {
        "id": "recolor:water-tank",
        "label": "recolor water-tank",
        "requires": [
          "done:open:water-tank"
        ],
        "forbids": [
          "done:recolor:water-tank"
        ],
        "adds": [
          "done:recolor:water-tank"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "water-tank",
          "color": "#ea7635"
        }
      }
    ],
    "goalFacts": [
      "repaired:water-tank"
    ],
    "budget": 6,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:water-tank",
      "open:water-tank",
      "recolor:water-tank",
      "verify:water-tank",
      "close:water-tank",
      "release:water-tank"
    ]
  }
}
```

### 跨区域联合维修（h3-wildfire-tiltrotor-multi-fault）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：跨区域联合维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:nacelle-right",
      "closed:nacelle-right",
      "fault:rotor-right",
      "closed:rotor-right",
      "fault:water-tank",
      "closed:water-tank"
    ],
    "initialModules": [
      "fuselage",
      "nacelle-left",
      "rotor-left",
      "nacelle-right",
      "rotor-right",
      "water-tank"
    ],
    "actions": [
      {
        "id": "verify:nacelle-right",
        "label": "verify nacelle-right",
        "requires": [
          "done:replace:nacelle-right"
        ],
        "forbids": [
          "done:verify:nacelle-right"
        ],
        "adds": [
          "done:verify:nacelle-right"
        ],
        "deletes": [
          "fault:nacelle-right"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "nacelle-right"
        }
      },
      {
        "id": "close:water-tank",
        "label": "close water-tank",
        "requires": [
          "done:verify:water-tank"
        ],
        "forbids": [
          "done:close:water-tank"
        ],
        "adds": [
          "done:close:water-tank"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "water-tank"
        }
      },
      {
        "id": "support:water-tank",
        "label": "support water-tank",
        "requires": [
          "fault:water-tank"
        ],
        "forbids": [
          "done:support:water-tank"
        ],
        "adds": [
          "done:support:water-tank"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "water-tank"
        }
      },
      {
        "id": "open:nacelle-right",
        "label": "open nacelle-right",
        "requires": [
          "done:support:nacelle-right"
        ],
        "forbids": [
          "done:open:nacelle-right"
        ],
        "adds": [
          "done:open:nacelle-right"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "nacelle-right"
        }
      },
      {
        "id": "open:rotor-right",
        "label": "open rotor-right",
        "requires": [
          "done:support:rotor-right"
        ],
        "forbids": [
          "done:open:rotor-right"
        ],
        "adds": [
          "done:open:rotor-right"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rotor-right"
        }
      },
      {
        "id": "replace:rotor-right",
        "label": "replace rotor-right",
        "requires": [
          "done:remove:rotor-right"
        ],
        "forbids": [
          "done:replace:rotor-right"
        ],
        "adds": [
          "done:replace:rotor-right"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rotor-right",
          "visible": true
        }
      },
      {
        "id": "release:water-tank",
        "label": "release water-tank",
        "requires": [
          "done:close:water-tank"
        ],
        "forbids": [
          "done:release:water-tank"
        ],
        "adds": [
          "done:release:water-tank",
          "repaired:water-tank"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "water-tank"
        }
      },
      {
        "id": "remove:rotor-right",
        "label": "remove rotor-right",
        "requires": [
          "done:open:rotor-right"
        ],
        "forbids": [
          "done:remove:rotor-right"
        ],
        "adds": [
          "done:remove:rotor-right"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rotor-right",
          "visible": false
        }
      },
      {
        "id": "open:water-tank",
        "label": "open water-tank",
        "requires": [
          "done:support:water-tank"
        ],
        "forbids": [
          "done:open:water-tank"
        ],
        "adds": [
          "done:open:water-tank"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "water-tank"
        }
      },
      {
        "id": "close:nacelle-right",
        "label": "close nacelle-right",
        "requires": [
          "done:verify:nacelle-right"
        ],
        "forbids": [
          "done:close:nacelle-right"
        ],
        "adds": [
          "done:close:nacelle-right"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "nacelle-right"
        }
      },
      {
        "id": "remove:water-tank",
        "label": "remove water-tank",
        "requires": [
          "done:open:water-tank"
        ],
        "forbids": [
          "done:remove:water-tank"
        ],
        "adds": [
          "done:remove:water-tank"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "water-tank",
          "visible": false
        }
      },
      {
        "id": "remove:nacelle-right",
        "label": "remove nacelle-right",
        "requires": [
          "done:open:nacelle-right"
        ],
        "forbids": [
          "done:remove:nacelle-right"
        ],
        "adds": [
          "done:remove:nacelle-right"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "nacelle-right",
          "visible": false
        }
      },
      {
        "id": "support:rotor-right",
        "label": "support rotor-right",
        "requires": [
          "fault:rotor-right"
        ],
        "forbids": [
          "done:support:rotor-right"
        ],
        "adds": [
          "done:support:rotor-right"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rotor-right"
        }
      },
      {
        "id": "close:rotor-right",
        "label": "close rotor-right",
        "requires": [
          "done:verify:rotor-right"
        ],
        "forbids": [
          "done:close:rotor-right"
        ],
        "adds": [
          "done:close:rotor-right"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rotor-right"
        }
      },
      {
        "id": "support:nacelle-right",
        "label": "support nacelle-right",
        "requires": [
          "fault:nacelle-right"
        ],
        "forbids": [
          "done:support:nacelle-right"
        ],
        "adds": [
          "done:support:nacelle-right"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "nacelle-right"
        }
      },
      {
        "id": "replace:water-tank",
        "label": "replace water-tank",
        "requires": [
          "done:remove:water-tank"
        ],
        "forbids": [
          "done:replace:water-tank"
        ],
        "adds": [
          "done:replace:water-tank"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "water-tank",
          "visible": true
        }
      },
      {
        "id": "verify:rotor-right",
        "label": "verify rotor-right",
        "requires": [
          "done:replace:rotor-right"
        ],
        "forbids": [
          "done:verify:rotor-right"
        ],
        "adds": [
          "done:verify:rotor-right"
        ],
        "deletes": [
          "fault:rotor-right"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "rotor-right"
        }
      },
      {
        "id": "release:nacelle-right",
        "label": "release nacelle-right",
        "requires": [
          "done:close:nacelle-right"
        ],
        "forbids": [
          "done:release:nacelle-right"
        ],
        "adds": [
          "done:release:nacelle-right",
          "repaired:nacelle-right"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "nacelle-right"
        }
      },
      {
        "id": "verify:water-tank",
        "label": "verify water-tank",
        "requires": [
          "done:replace:water-tank"
        ],
        "forbids": [
          "done:verify:water-tank"
        ],
        "adds": [
          "done:verify:water-tank"
        ],
        "deletes": [
          "fault:water-tank"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "water-tank"
        }
      },
      {
        "id": "release:rotor-right",
        "label": "release rotor-right",
        "requires": [
          "done:close:rotor-right"
        ],
        "forbids": [
          "done:release:rotor-right"
        ],
        "adds": [
          "done:release:rotor-right",
          "repaired:rotor-right"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rotor-right"
        }
      },
      {
        "id": "replace:nacelle-right",
        "label": "replace nacelle-right",
        "requires": [
          "done:remove:nacelle-right"
        ],
        "forbids": [
          "done:replace:nacelle-right"
        ],
        "adds": [
          "done:replace:nacelle-right"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "nacelle-right",
          "visible": true
        }
      }
    ],
    "goalFacts": [
      "repaired:nacelle-right",
      "repaired:rotor-right",
      "repaired:water-tank"
    ],
    "budget": 21,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:water-tank",
      "open:water-tank",
      "remove:water-tank",
      "support:rotor-right",
      "open:rotor-right",
      "remove:rotor-right",
      "replace:rotor-right",
      "support:nacelle-right",
      "open:nacelle-right",
      "remove:nacelle-right",
      "replace:water-tank",
      "verify:rotor-right",
      "close:rotor-right",
      "verify:water-tank",
      "close:water-tank",
      "release:water-tank",
      "release:rotor-right",
      "replace:nacelle-right",
      "verify:nacelle-right",
      "close:nacelle-right",
      "release:nacelle-right"
    ]
  }
}
```

### 多工位资源调度（h3-wildfire-tiltrotor-scheduling）

为所有工单提交整数 starts，满足先后关系、独占工位及截止时间。

能力：多工位资源调度；形式：schedule；证据：resource-schedule。


```json
{
  "input": {
    "jobs": [
      {
        "id": "job-0",
        "module": "fuselage",
        "duration": 3,
        "resource": "test-bench",
        "after": []
      },
      {
        "id": "job-1",
        "module": "nacelle-left",
        "duration": 2,
        "resource": "technician",
        "after": []
      },
      {
        "id": "job-2",
        "module": "rotor-left",
        "duration": 3,
        "resource": "test-bench",
        "after": [
          "job-0"
        ]
      },
      {
        "id": "job-3",
        "module": "nacelle-right",
        "duration": 2,
        "resource": "technician",
        "after": [
          "job-1"
        ]
      },
      {
        "id": "job-4",
        "module": "rotor-right",
        "duration": 1,
        "resource": "test-bench",
        "after": [
          "job-2"
        ]
      },
      {
        "id": "job-5",
        "module": "water-tank",
        "duration": 3,
        "resource": "technician",
        "after": [
          "job-3"
        ]
      }
    ],
    "deadline": 7
  },
  "answer": {
    "starts": {
      "job-0": 0,
      "job-1": 0,
      "job-2": 3,
      "job-3": 2,
      "job-4": 6,
      "job-5": 4
    }
  }
}
```

### 检查后条件策略（h3-wildfire-tiltrotor-policy）

提交一个检查及 observation→action 决策表，在所有相容世界中采取正确动作。

能力：检查后条件策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "water-tank",
    "worlds": [
      {
        "id": "normal",
        "action": "continue"
      },
      {
        "id": "loose",
        "action": "tighten"
      },
      {
        "id": "jammed",
        "action": "replace"
      }
    ],
    "budget": 1,
    "queries": [
      {
        "id": "visual",
        "cost": 1,
        "returns": {
          "normal": "signal-0",
          "loose": "signal-1",
          "jammed": "signal-2"
        }
      },
      {
        "id": "probe",
        "cost": 2,
        "returns": {
          "normal": "same",
          "loose": "same",
          "jammed": "other"
        }
      },
      {
        "id": "thermal",
        "cost": 3,
        "returns": {
          "normal": "same",
          "loose": "same",
          "jammed": "other"
        }
      }
    ]
  },
  "answer": {
    "queryId": "visual",
    "decisions": {
      "signal-0": "continue",
      "signal-1": "tighten",
      "signal-2": "replace"
    }
  }
}
```

### 局部坐标变换（h3-wildfire-tiltrotor-local-frame）

将模块局部点通过给定四元数与平移转换为世界点，保留五位小数。

能力：局部坐标变换；形式：single-choice；证据：model-state。

- A：[0,1.7,1.8]
- B：[1,-0.2,0]
- C：[1,1.7,0.8]
- D：[1,2.7,2.8]

```json
{
  "input": {
    "localPoint": [
      1,
      -0.20000000000000007,
      0
    ],
    "rotationXYZW": [
      0,
      0.7071067811865476,
      0,
      -0.7071067811865475
    ],
    "translation": [
      0,
      1.9000000000000004,
      0.8
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 正交视图投影（h3-wildfire-tiltrotor-projection）

按公开视图坐标约定，选择该世界点投影后的二维坐标。

能力：正交视图投影；形式：single-choice；证据：model-state。

- A：[4,5]
- B：[0,0]
- C：[4,9]
- D：[9,4]

```json
{
  "input": {
    "view": "front",
    "point": [
      4,
      9,
      -5
    ],
    "convention": "front=(x,y), side=(z,y), top=(x,z)"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 空间相对关系（h3-wildfire-tiltrotor-relative-order）

比较B相对A在指定世界轴上的模块原点坐标。

能力：空间相对关系；形式：single-choice；证据：model-state。

- A：less
- B：equal
- C：greater

```json
{
  "input": {
    "A": {
      "id": "fuselage",
      "position": [
        0,
        3.963920173162002,
        1.3168942074233891
      ]
    },
    "B": {
      "id": "water-tank",
      "position": [
        0,
        1.9000000000000004,
        0.8
      ]
    },
    "axis": "x"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 约束自由度（h3-wildfire-tiltrotor-joint-axis）

仅考虑这一声明约束，不计闭环、马达与限位激活，保留多少相对运动自由度？弹簧仅施力、不消除自由度。

能力：约束自由度；形式：single-choice；证据：model-state。

- A：1
- B：0
- C：3
- D：6

```json
{
  "input": {
    "joint": {
      "id": "rotor-left-shaft",
      "name": "rotor-left shaft",
      "type": "revolute",
      "parent": "nacelle-left",
      "child": "rotor-left",
      "anchorParent": [
        0.9,
        1.5,
        0
      ],
      "anchorChild": [
        0,
        -0.24500000000000005,
        0
      ],
      "axis": [
        0,
        1,
        0
      ]
    }
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 维修间隙预算（h3-wildfire-tiltrotor-clearance-margin）

给定理想直槽净宽、工具宽度、单侧安全余量，工具是否满足横向间隙要求？

能力：维修间隙预算；形式：single-choice；证据：model-state。

- A：feasible
- B：blocked

```json
{
  "input": {
    "module": "water-tank",
    "aperture": 0.6100000000000001,
    "toolWidth": 0.55,
    "eachSideMargin": 0
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 载荷力矩（h3-wildfire-tiltrotor-load-moment）

绕给定原点的载荷力矩r×F是多少？采用右手系，忽略其他力。

能力：载荷力矩；形式：single-choice；证据：model-state。

- A：[0,0,9]
- B：[0,0,0]
- C：[0,-3,0]
- D：[0,0,-9]

```json
{
  "input": {
    "module": "water-tank",
    "lever": [
      3,
      1,
      0
    ],
    "force": [
      0,
      -3,
      0
    ],
    "units": "scene-length × force"
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 非均匀先验更新（h3-wildfire-tiltrotor-weighted-posterior）

先验权重未归一化，观测只保留normal和jammed，求jammed后验概率。

能力：非均匀先验更新；形式：single-choice；证据：finite-world。

- A：0.3333333333333333
- B：0
- C：1
- D：0.6

```json
{
  "input": {
    "module": "water-tank",
    "worlds": [
      "normal",
      "jammed",
      "loose"
    ],
    "weights": [
      2,
      3,
      4
    ],
    "compatible": [
      "normal",
      "jammed"
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 风险最小决策（h3-wildfire-tiltrotor-expected-loss）

继续运行期望损失=p×failureLoss，预防维修损失=repairCost，选择损失较低者；并列选继续。

能力：风险最小决策；形式：single-choice；证据：finite-world。

- A：continue
- B：repair

```json
{
  "input": {
    "faultProbability": 0.4,
    "repairCost": 2,
    "failureLoss": 13,
    "module": "water-tank"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 轨迹阈值判定（h3-wildfire-tiltrotor-trace-threshold）

实际采样轨迹中是否有位移严格超过给定阈值？只评价采样点。

能力：轨迹阈值判定；形式：single-choice；证据：Rapier。

- A：exceeded
- B：within

```json
{
  "input": {
    "trace": [
      {
        "time": 0.008333333333333333,
        "displacement": 0.0073585474047615776
      },
      {
        "time": 0.10833333333333334,
        "displacement": 6.743495761743046e-7
      },
      {
        "time": 0.20833333333333334,
        "displacement": 6.743495761743046e-7
      },
      {
        "time": 0.30833333333333335,
        "displacement": 6.743495761743046e-7
      },
      {
        "time": 0.4083333333333333,
        "displacement": 6.743495761743046e-7
      },
      {
        "time": 0.5083333333333333,
        "displacement": 6.743495761743046e-7
      },
      {
        "time": 0.6083333333333333,
        "displacement": 6.743495761743046e-7
      },
      {
        "time": 0.7083333333333334,
        "displacement": 6.743495761743046e-7
      },
      {
        "time": 0.8083333333333333,
        "displacement": 6.743495761743046e-7
      },
      {
        "time": 0.9083333333333333,
        "displacement": 6.743495761743046e-7
      },
      {
        "time": 1,
        "displacement": 6.743495761743046e-7
      }
    ],
    "threshold": 0.008830256885713893
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 安全联锁维修（h3-wildfire-tiltrotor-guarded-repair）

从给定故障状态提交动作序列，满足联锁、独占工具、终态及预算。不要跳过验证。

能力：安全联锁维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "actions": [
      {
        "id": "skip-inspection",
        "label": "跳过检查",
        "requires": [
          "tool:free"
        ],
        "forbids": [],
        "adds": [
          "unverified"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 0
      },
      {
        "id": "release:water-tank",
        "label": "release water-tank",
        "requires": [
          "done:relock:water-tank"
        ],
        "forbids": [
          "done:release:water-tank"
        ],
        "adds": [
          "done:release:water-tank",
          "ready:water-tank",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "water-tank"
        }
      },
      {
        "id": "relock:water-tank",
        "label": "relock water-tank",
        "requires": [
          "done:verify:water-tank"
        ],
        "forbids": [
          "done:relock:water-tank"
        ],
        "adds": [
          "done:relock:water-tank"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "water-tank"
        }
      },
      {
        "id": "verify:water-tank",
        "label": "verify water-tank",
        "requires": [
          "done:replace:water-tank"
        ],
        "forbids": [
          "done:verify:water-tank"
        ],
        "adds": [
          "done:verify:water-tank"
        ],
        "deletes": [
          "fault:water-tank",
          "misaligned:water-tank"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "water-tank"
        }
      },
      {
        "id": "replace:water-tank",
        "label": "replace water-tank",
        "requires": [
          "done:unlock:water-tank"
        ],
        "forbids": [
          "done:replace:water-tank"
        ],
        "adds": [
          "done:replace:water-tank"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "water-tank"
        }
      },
      {
        "id": "unlock:water-tank",
        "label": "unlock water-tank",
        "requires": [
          "done:support:water-tank"
        ],
        "forbids": [
          "done:unlock:water-tank"
        ],
        "adds": [
          "done:unlock:water-tank"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "water-tank"
        }
      },
      {
        "id": "support:water-tank",
        "label": "support water-tank",
        "requires": [
          "done:isolate:water-tank"
        ],
        "forbids": [
          "done:support:water-tank"
        ],
        "adds": [
          "done:support:water-tank"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "water-tank"
        }
      },
      {
        "id": "isolate:water-tank",
        "label": "isolate water-tank",
        "requires": [
          "tool:free",
          "fault:water-tank"
        ],
        "forbids": [
          "done:isolate:water-tank"
        ],
        "adds": [
          "done:isolate:water-tank"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "water-tank"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:water-tank"
    ],
    "initialModules": [
      "fuselage",
      "nacelle-left",
      "rotor-left",
      "nacelle-right",
      "rotor-right",
      "water-tank"
    ],
    "goalFacts": [
      "ready:water-tank"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 8
  },
  "answer": {
    "actionIds": [
      "isolate:water-tank",
      "support:water-tank",
      "unlock:water-tank",
      "replace:water-tank",
      "verify:water-tank",
      "relock:water-tank",
      "release:water-tank"
    ]
  }
}
```

### 失败状态回退（h3-wildfire-tiltrotor-rollback）

从给定故障状态提交动作序列，满足联锁、独占工具、终态及预算。不要跳过验证。

能力：失败状态回退；形式：actions；证据：state-machine。


```json
{
  "input": {
    "actions": [
      {
        "id": "skip-inspection",
        "label": "跳过检查",
        "requires": [
          "tool:free"
        ],
        "forbids": [],
        "adds": [
          "unverified"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 0
      },
      {
        "id": "resume:water-tank",
        "label": "resume water-tank",
        "requires": [
          "done:verify:water-tank"
        ],
        "forbids": [
          "done:resume:water-tank"
        ],
        "adds": [
          "done:resume:water-tank",
          "ready:water-tank",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "water-tank"
        }
      },
      {
        "id": "verify:water-tank",
        "label": "verify water-tank",
        "requires": [
          "done:align:water-tank"
        ],
        "forbids": [
          "done:verify:water-tank"
        ],
        "adds": [
          "done:verify:water-tank"
        ],
        "deletes": [
          "fault:water-tank",
          "misaligned:water-tank"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "water-tank"
        }
      },
      {
        "id": "align:water-tank",
        "label": "align water-tank",
        "requires": [
          "done:undo:water-tank"
        ],
        "forbids": [
          "done:align:water-tank"
        ],
        "adds": [
          "done:align:water-tank"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "water-tank",
          "visible": true
        }
      },
      {
        "id": "undo:water-tank",
        "label": "undo water-tank",
        "requires": [
          "done:isolate:water-tank"
        ],
        "forbids": [
          "done:undo:water-tank"
        ],
        "adds": [
          "done:undo:water-tank"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "water-tank",
          "visible": false
        }
      },
      {
        "id": "isolate:water-tank",
        "label": "isolate water-tank",
        "requires": [
          "tool:free",
          "fault:water-tank"
        ],
        "forbids": [
          "done:isolate:water-tank"
        ],
        "adds": [
          "done:isolate:water-tank"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "water-tank"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:water-tank",
      "misaligned:water-tank"
    ],
    "initialModules": [
      "fuselage",
      "nacelle-left",
      "rotor-left",
      "nacelle-right",
      "rotor-right",
      "water-tank"
    ],
    "goalFacts": [
      "ready:water-tank"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 5
  },
  "answer": {
    "actionIds": [
      "isolate:water-tank",
      "undo:water-tank",
      "align:water-tank",
      "verify:water-tank",
      "resume:water-tank"
    ]
  }
}
```

### 共享工具协同维修（h3-wildfire-tiltrotor-resource-repair）

从给定故障状态提交动作序列，满足联锁、独占工具、终态及预算。不要跳过验证。

能力：共享工具协同维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "actions": [
      {
        "id": "skip-inspection",
        "label": "跳过检查",
        "requires": [
          "tool:free"
        ],
        "forbids": [],
        "adds": [
          "unverified"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 0
      },
      {
        "id": "release:water-tank",
        "label": "release water-tank",
        "requires": [
          "done:relock:water-tank"
        ],
        "forbids": [
          "done:release:water-tank"
        ],
        "adds": [
          "done:release:water-tank",
          "ready:water-tank",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "water-tank"
        }
      },
      {
        "id": "relock:water-tank",
        "label": "relock water-tank",
        "requires": [
          "done:verify:water-tank"
        ],
        "forbids": [
          "done:relock:water-tank"
        ],
        "adds": [
          "done:relock:water-tank"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "water-tank"
        }
      },
      {
        "id": "verify:water-tank",
        "label": "verify water-tank",
        "requires": [
          "done:replace:water-tank"
        ],
        "forbids": [
          "done:verify:water-tank"
        ],
        "adds": [
          "done:verify:water-tank"
        ],
        "deletes": [
          "fault:water-tank",
          "misaligned:water-tank"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "water-tank"
        }
      },
      {
        "id": "replace:water-tank",
        "label": "replace water-tank",
        "requires": [
          "done:unlock:water-tank"
        ],
        "forbids": [
          "done:replace:water-tank"
        ],
        "adds": [
          "done:replace:water-tank"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "water-tank"
        }
      },
      {
        "id": "unlock:water-tank",
        "label": "unlock water-tank",
        "requires": [
          "done:support:water-tank"
        ],
        "forbids": [
          "done:unlock:water-tank"
        ],
        "adds": [
          "done:unlock:water-tank"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "water-tank"
        }
      },
      {
        "id": "support:water-tank",
        "label": "support water-tank",
        "requires": [
          "done:isolate:water-tank"
        ],
        "forbids": [
          "done:support:water-tank"
        ],
        "adds": [
          "done:support:water-tank"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "water-tank"
        }
      },
      {
        "id": "isolate:water-tank",
        "label": "isolate water-tank",
        "requires": [
          "tool:free",
          "fault:water-tank"
        ],
        "forbids": [
          "done:isolate:water-tank"
        ],
        "adds": [
          "done:isolate:water-tank"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "water-tank"
        }
      },
      {
        "id": "release:rotor-right",
        "label": "release rotor-right",
        "requires": [
          "done:relock:rotor-right"
        ],
        "forbids": [
          "done:release:rotor-right"
        ],
        "adds": [
          "done:release:rotor-right",
          "ready:rotor-right",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rotor-right"
        }
      },
      {
        "id": "relock:rotor-right",
        "label": "relock rotor-right",
        "requires": [
          "done:verify:rotor-right"
        ],
        "forbids": [
          "done:relock:rotor-right"
        ],
        "adds": [
          "done:relock:rotor-right"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rotor-right"
        }
      },
      {
        "id": "verify:rotor-right",
        "label": "verify rotor-right",
        "requires": [
          "done:replace:rotor-right"
        ],
        "forbids": [
          "done:verify:rotor-right"
        ],
        "adds": [
          "done:verify:rotor-right"
        ],
        "deletes": [
          "fault:rotor-right",
          "misaligned:rotor-right"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "rotor-right"
        }
      },
      {
        "id": "replace:rotor-right",
        "label": "replace rotor-right",
        "requires": [
          "done:unlock:rotor-right"
        ],
        "forbids": [
          "done:replace:rotor-right"
        ],
        "adds": [
          "done:replace:rotor-right"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "rotor-right"
        }
      },
      {
        "id": "unlock:rotor-right",
        "label": "unlock rotor-right",
        "requires": [
          "done:support:rotor-right"
        ],
        "forbids": [
          "done:unlock:rotor-right"
        ],
        "adds": [
          "done:unlock:rotor-right"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rotor-right"
        }
      },
      {
        "id": "support:rotor-right",
        "label": "support rotor-right",
        "requires": [
          "done:isolate:rotor-right"
        ],
        "forbids": [
          "done:support:rotor-right"
        ],
        "adds": [
          "done:support:rotor-right"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rotor-right"
        }
      },
      {
        "id": "isolate:rotor-right",
        "label": "isolate rotor-right",
        "requires": [
          "tool:free",
          "fault:rotor-right"
        ],
        "forbids": [
          "done:isolate:rotor-right"
        ],
        "adds": [
          "done:isolate:rotor-right"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "rotor-right"
        }
      },
      {
        "id": "release:nacelle-right",
        "label": "release nacelle-right",
        "requires": [
          "done:relock:nacelle-right"
        ],
        "forbids": [
          "done:release:nacelle-right"
        ],
        "adds": [
          "done:release:nacelle-right",
          "ready:nacelle-right",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "nacelle-right"
        }
      },
      {
        "id": "relock:nacelle-right",
        "label": "relock nacelle-right",
        "requires": [
          "done:verify:nacelle-right"
        ],
        "forbids": [
          "done:relock:nacelle-right"
        ],
        "adds": [
          "done:relock:nacelle-right"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "nacelle-right"
        }
      },
      {
        "id": "verify:nacelle-right",
        "label": "verify nacelle-right",
        "requires": [
          "done:replace:nacelle-right"
        ],
        "forbids": [
          "done:verify:nacelle-right"
        ],
        "adds": [
          "done:verify:nacelle-right"
        ],
        "deletes": [
          "fault:nacelle-right",
          "misaligned:nacelle-right"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "nacelle-right"
        }
      },
      {
        "id": "replace:nacelle-right",
        "label": "replace nacelle-right",
        "requires": [
          "done:unlock:nacelle-right"
        ],
        "forbids": [
          "done:replace:nacelle-right"
        ],
        "adds": [
          "done:replace:nacelle-right"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "nacelle-right"
        }
      },
      {
        "id": "unlock:nacelle-right",
        "label": "unlock nacelle-right",
        "requires": [
          "done:support:nacelle-right"
        ],
        "forbids": [
          "done:unlock:nacelle-right"
        ],
        "adds": [
          "done:unlock:nacelle-right"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "nacelle-right"
        }
      },
      {
        "id": "support:nacelle-right",
        "label": "support nacelle-right",
        "requires": [
          "done:isolate:nacelle-right"
        ],
        "forbids": [
          "done:support:nacelle-right"
        ],
        "adds": [
          "done:support:nacelle-right"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "nacelle-right"
        }
      },
      {
        "id": "isolate:nacelle-right",
        "label": "isolate nacelle-right",
        "requires": [
          "tool:free",
          "fault:nacelle-right"
        ],
        "forbids": [
          "done:isolate:nacelle-right"
        ],
        "adds": [
          "done:isolate:nacelle-right"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "nacelle-right"
        }
      },
      {
        "id": "release:rotor-left",
        "label": "release rotor-left",
        "requires": [
          "done:relock:rotor-left"
        ],
        "forbids": [
          "done:release:rotor-left"
        ],
        "adds": [
          "done:release:rotor-left",
          "ready:rotor-left",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rotor-left"
        }
      },
      {
        "id": "relock:rotor-left",
        "label": "relock rotor-left",
        "requires": [
          "done:verify:rotor-left"
        ],
        "forbids": [
          "done:relock:rotor-left"
        ],
        "adds": [
          "done:relock:rotor-left"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rotor-left"
        }
      },
      {
        "id": "verify:rotor-left",
        "label": "verify rotor-left",
        "requires": [
          "done:replace:rotor-left"
        ],
        "forbids": [
          "done:verify:rotor-left"
        ],
        "adds": [
          "done:verify:rotor-left"
        ],
        "deletes": [
          "fault:rotor-left",
          "misaligned:rotor-left"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "rotor-left"
        }
      },
      {
        "id": "replace:rotor-left",
        "label": "replace rotor-left",
        "requires": [
          "done:unlock:rotor-left"
        ],
        "forbids": [
          "done:replace:rotor-left"
        ],
        "adds": [
          "done:replace:rotor-left"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "rotor-left"
        }
      },
      {
        "id": "unlock:rotor-left",
        "label": "unlock rotor-left",
        "requires": [
          "done:support:rotor-left"
        ],
        "forbids": [
          "done:unlock:rotor-left"
        ],
        "adds": [
          "done:unlock:rotor-left"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rotor-left"
        }
      },
      {
        "id": "support:rotor-left",
        "label": "support rotor-left",
        "requires": [
          "done:isolate:rotor-left"
        ],
        "forbids": [
          "done:support:rotor-left"
        ],
        "adds": [
          "done:support:rotor-left"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rotor-left"
        }
      },
      {
        "id": "isolate:rotor-left",
        "label": "isolate rotor-left",
        "requires": [
          "tool:free",
          "fault:rotor-left"
        ],
        "forbids": [
          "done:isolate:rotor-left"
        ],
        "adds": [
          "done:isolate:rotor-left"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "rotor-left"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:rotor-left",
      "fault:nacelle-right",
      "fault:rotor-right",
      "fault:water-tank"
    ],
    "initialModules": [
      "fuselage",
      "nacelle-left",
      "rotor-left",
      "nacelle-right",
      "rotor-right",
      "water-tank"
    ],
    "goalFacts": [
      "ready:rotor-left",
      "ready:nacelle-right",
      "ready:rotor-right",
      "ready:water-tank"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 32
  },
  "answer": {
    "actionIds": [
      "isolate:water-tank",
      "support:water-tank",
      "unlock:water-tank",
      "replace:water-tank",
      "verify:water-tank",
      "relock:water-tank",
      "release:water-tank",
      "isolate:rotor-right",
      "support:rotor-right",
      "unlock:rotor-right",
      "replace:rotor-right",
      "verify:rotor-right",
      "relock:rotor-right",
      "release:rotor-right",
      "isolate:nacelle-right",
      "support:nacelle-right",
      "unlock:nacelle-right",
      "replace:nacelle-right",
      "verify:nacelle-right",
      "relock:nacelle-right",
      "release:nacelle-right",
      "isolate:rotor-left",
      "support:rotor-left",
      "unlock:rotor-left",
      "replace:rotor-left",
      "verify:rotor-left",
      "relock:rotor-left",
      "release:rotor-left"
    ]
  }
}
```

### 预算约束检查策略（h3-wildfire-tiltrotor-budget-policy）

提交预算内、对所有相容世界均正确的检查决策表。

能力：预算约束检查策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "water-tank",
    "worlds": [
      {
        "id": "nominal",
        "action": "continue"
      },
      {
        "id": "fault",
        "action": "replace"
      }
    ],
    "queries": [
      {
        "id": "visual",
        "cost": 1,
        "returns": {
          "nominal": "clear",
          "fault": "alert"
        }
      },
      {
        "id": "probe",
        "cost": 0,
        "returns": {
          "nominal": "clear",
          "fault": "clear"
        }
      },
      {
        "id": "thermal",
        "cost": 2,
        "returns": {
          "nominal": "clear",
          "fault": "alert"
        }
      }
    ],
    "budget": 1
  },
  "answer": {
    "queryId": "visual",
    "decisions": {
      "clear": "continue",
      "alert": "replace"
    }
  }
}
```
