## D2 装配单元·双层维修回转台

### 模块识别（h3-exp-d2-turntable-2-identify）

高亮的维修模块对应哪个 ID？

能力：模块识别；形式：single-choice；证据：model-state。

- A：cell-0-offset-load
- B：foundation
- C：cell-0-shuttle
- D：cell-0-mount

```json
{
  "input": {
    "moduleNames": [
      {
        "id": "foundation",
        "name": "foundation"
      },
      {
        "id": "cell-0-shuttle",
        "name": "cell 0 shuttle"
      },
      {
        "id": "cell-0-mount",
        "name": "cell 0 mount"
      },
      {
        "id": "cell-0-pedestal",
        "name": "cell 0 pedestal"
      },
      {
        "id": "cell-0-rotor",
        "name": "cell 0 rotor"
      },
      {
        "id": "cell-0-offset-load",
        "name": "cell 0 offset load"
      },
      {
        "id": "cell-0-upper-stage",
        "name": "cell 0 upper stage"
      },
      {
        "id": "cell-0-console",
        "name": "cell 0 console"
      }
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 部件计数（h3-exp-d2-turntable-2-count）

模块 cell-0-offset-load 有多少个可视零件？

能力：部件计数；形式：single-choice；证据：model-state。

- A：5
- B：2
- C：3
- D：1

```json
{
  "input": {
    "parts": [
      {
        "id": "foundation-p0",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p1",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p2",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p3",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p4",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p5",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p6",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p7",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p8",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p9",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p10",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p11",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p12",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p13",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p14",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p15",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p16",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p17",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p18",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p19",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p20",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p21",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p22",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p23",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p24",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p25",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p26",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p27",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p28",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p29",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p30",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p31",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p32",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p33",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p34",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p35",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p36",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p37",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p38",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p39",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p40",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p41",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p42",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p43",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p44",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p45",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p46",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p47",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p48",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p49",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p50",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p51",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p52",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p53",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p54",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p55",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-shuttle-p56",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p57",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p58",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p59",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p60",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p61",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p62",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p63",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p64",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p65",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p66",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p67",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p68",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p69",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p70",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p71",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p72",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p73",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p74",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p75",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p76",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p77",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p78",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p79",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p80",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p81",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p82",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p83",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p84",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p85",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p86",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p87",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p88",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p89",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p90",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p91",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p92",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p93",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p94",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p95",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p96",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p97",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p98",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p99",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p100",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p101",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p102",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p103",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-mount-p104",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p105",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p106",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p107",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p108",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p109",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p110",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p111",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p112",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p113",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p114",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p115",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p116",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p117",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p118",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p119",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p120",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p121",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p122",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p123",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p124",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p125",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p126",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p127",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p128",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p129",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p130",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p131",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p132",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p133",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p134",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p135",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p136",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p137",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p138",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-pedestal-p139",
        "moduleId": "cell-0-pedestal",
        "shape": "cylinder",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-rotor-p140",
        "moduleId": "cell-0-rotor",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-0-rotor-p141",
        "moduleId": "cell-0-rotor",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-0-rotor-p142",
        "moduleId": "cell-0-rotor",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-0-rotor-p143",
        "moduleId": "cell-0-rotor",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-0-rotor-p144",
        "moduleId": "cell-0-rotor",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-0-rotor-p145",
        "moduleId": "cell-0-rotor",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-0-rotor-p146",
        "moduleId": "cell-0-rotor",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-0-rotor-p147",
        "moduleId": "cell-0-rotor",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-0-rotor-p148",
        "moduleId": "cell-0-rotor",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-0-rotor-p149",
        "moduleId": "cell-0-rotor",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-0-rotor-p150",
        "moduleId": "cell-0-rotor",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-0-rotor-p151",
        "moduleId": "cell-0-rotor",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-0-rotor-p152",
        "moduleId": "cell-0-rotor",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-0-rotor-p153",
        "moduleId": "cell-0-rotor",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-0-rotor-p154",
        "moduleId": "cell-0-rotor",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-0-rotor-p155",
        "moduleId": "cell-0-rotor",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-0-offset-load-p156",
        "moduleId": "cell-0-offset-load",
        "shape": "cylinder",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-offset-load-p157",
        "moduleId": "cell-0-offset-load",
        "shape": "gear",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-upper-stage-p158",
        "moduleId": "cell-0-upper-stage",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-0-upper-stage-p159",
        "moduleId": "cell-0-upper-stage",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-0-upper-stage-p160",
        "moduleId": "cell-0-upper-stage",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-0-upper-stage-p161",
        "moduleId": "cell-0-upper-stage",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-0-console-p162",
        "moduleId": "cell-0-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-console-p163",
        "moduleId": "cell-0-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-console-p164",
        "moduleId": "cell-0-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-console-p165",
        "moduleId": "cell-0-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-console-p166",
        "moduleId": "cell-0-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-console-p167",
        "moduleId": "cell-0-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-console-p168",
        "moduleId": "cell-0-console",
        "shape": "window",
        "color": "#79c7d8"
      },
      {
        "id": "cell-0-console-p169",
        "moduleId": "cell-0-console",
        "shape": "slope",
        "color": "#dfebed"
      }
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 颜色识别（h3-exp-d2-turntable-2-color）

零件 cell-0-offset-load-p156 的颜色值是什么？

能力：颜色识别；形式：single-choice；证据：model-state。

- A：#f2bf3c
- B：#dc6040
- C：#2878b8
- D：#d43a32

```json
{
  "input": {
    "part": {
      "id": "cell-0-offset-load-p156",
      "moduleId": "cell-0-offset-load",
      "shape": "cylinder",
      "position": [
        0,
        -0.16249999999999964,
        1.1102230246251565e-16
      ],
      "size": [
        1.3,
        1.1,
        1.3
      ],
      "color": "#dc6040",
      "rotation": [
        0,
        0,
        0,
        1
      ]
    }
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 三维位置（h3-exp-d2-turntable-2-position）

模块 cell-0-offset-load 的世界包围盒中心是什么？

能力：三维位置；形式：single-choice；证据：model-state。

- A：[1,4.1625,0.5999999999999999]
- B：[0,0.2,0]
- C：[0,0.75,0]
- D：[0,1.35,0]

```json
{
  "input": {
    "centers": {
      "foundation": [
        0,
        0.2,
        0
      ],
      "cell-0-shuttle": [
        0,
        0.75,
        0
      ],
      "cell-0-mount": [
        0,
        1.35,
        0
      ],
      "cell-0-pedestal": [
        0,
        2.2,
        0
      ],
      "cell-0-rotor": [
        0,
        3.25,
        0
      ],
      "cell-0-offset-load": [
        1,
        4.1625,
        0.5999999999999999
      ],
      "cell-0-upper-stage": [
        -1,
        4.35,
        -1
      ],
      "cell-0-console": [
        0,
        1.8775000000000002,
        6
      ]
    }
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 关节类型（h3-exp-d2-turntable-2-joint-type）

cell-0-rotor-joint 采用什么约束类型？

能力：关节类型；形式：single-choice；证据：model-state。

- A：fixed
- B：prismatic
- C：spring
- D：revolute

```json
{
  "input": {
    "joint": {
      "id": "cell-0-rotor-joint",
      "name": "cell-0-rotor interface",
      "parent": "cell-0-pedestal",
      "child": "cell-0-rotor",
      "type": "revolute",
      "anchorParent": [
        0,
        1,
        0
      ],
      "anchorChild": [
        0,
        -0.04999999999999982,
        0
      ],
      "axis": [
        0,
        1,
        0
      ],
      "limits": [
        -0.6,
        0.6
      ]
    }
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 直接连接（h3-exp-d2-turntable-2-parent）

cell-0-offset-load 的直接父模块集合是什么？

能力：直接连接；形式：single-choice；证据：model-state。

- A：["cell-0-rotor"]
- B：["cell-0-offset-load"]
- C：[]
- D：["foundation","cell-0-shuttle","cell-0-mount","cell-0-pedestal","cell-0-rotor","cell-0-offset-load","cell-0-upper-stage","cell-0-console"]

```json
{
  "input": {
    "joints": [
      {
        "id": "cell-0-shuttle-joint",
        "name": "cell-0-shuttle interface",
        "parent": "foundation",
        "child": "cell-0-shuttle",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.4999999999999999,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-0-mount-joint",
        "name": "cell-0-mount interface",
        "parent": "cell-0-shuttle",
        "child": "cell-0-mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.55,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-pedestal-joint",
        "name": "cell-0-pedestal interface",
        "parent": "cell-0-mount",
        "child": "cell-0-pedestal",
        "type": "fixed",
        "anchorParent": [
          0,
          0.8500000000000001,
          0
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-rotor-joint",
        "name": "cell-0-rotor interface",
        "parent": "cell-0-pedestal",
        "child": "cell-0-rotor",
        "type": "revolute",
        "anchorParent": [
          0,
          1,
          0
        ],
        "anchorChild": [
          0,
          -0.04999999999999982,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-0-offset-load-joint",
        "name": "cell-0-offset-load interface",
        "parent": "cell-0-rotor",
        "child": "cell-0-offset-load",
        "type": "fixed",
        "anchorParent": [
          1,
          0.75,
          0.6
        ],
        "anchorChild": [
          0,
          -0.16249999999999964,
          1.1102230246251565e-16
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-upper-stage-joint",
        "name": "cell-0-upper-stage interface",
        "parent": "cell-0-rotor",
        "child": "cell-0-upper-stage",
        "type": "prismatic",
        "anchorParent": [
          -1,
          1.0499999999999998,
          -1
        ],
        "anchorChild": [
          0,
          -0.04999999999999982,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-0-console-joint",
        "name": "cell-0-console interface",
        "parent": "foundation",
        "child": "cell-0-console",
        "type": "fixed",
        "anchorParent": [
          0,
          1.1,
          6
        ],
        "anchorChild": [
          0,
          -0.5775000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      }
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 基座识别（h3-exp-d2-turntable-2-anchor）

哪些模块被声明为固定基座？

能力：基座识别；形式：single-choice；证据：model-state。

- A：["foundation","cell-0-shuttle","cell-0-mount","cell-0-pedestal","cell-0-rotor","cell-0-offset-load","cell-0-upper-stage","cell-0-console"]
- B：["cell-0-offset-load"]
- C：["foundation"]
- D：[]

```json
{
  "input": {
    "modules": [
      {
        "id": "foundation",
        "name": "foundation",
        "role": "foundation",
        "anchored": true,
        "mass": 30,
        "position": [
          0,
          0.2,
          0
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "cell-0-shuttle",
        "name": "cell 0 shuttle",
        "role": "actuator",
        "anchored": false,
        "mass": 3,
        "position": [
          0,
          0.75,
          0
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "cell-0-mount",
        "name": "cell 0 mount",
        "role": "structure",
        "anchored": false,
        "mass": 1.2,
        "position": [
          0,
          1.35,
          0
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "cell-0-pedestal",
        "name": "cell 0 pedestal",
        "role": "structure",
        "anchored": false,
        "mass": 1.2,
        "position": [
          0,
          2.2,
          0
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "cell-0-rotor",
        "name": "cell 0 rotor",
        "role": "actuator",
        "anchored": false,
        "mass": 1.2,
        "position": [
          0,
          3.25,
          0
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "cell-0-offset-load",
        "name": "cell 0 offset load",
        "role": "structure",
        "anchored": false,
        "mass": 0.8,
        "position": [
          1,
          4.1625,
          0.5999999999999999
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "cell-0-upper-stage",
        "name": "cell 0 upper stage",
        "role": "actuator",
        "anchored": false,
        "mass": 0.8,
        "position": [
          -1,
          4.35,
          -1
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "cell-0-console",
        "name": "cell 0 console",
        "role": "structure",
        "anchored": false,
        "mass": 1.2,
        "position": [
          0,
          1.8775000000000002,
          6
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
    "choiceId": "C"
  }
}
```

### 接口计数（h3-exp-d2-turntable-2-degree）

cell-0-offset-load 连接几个声明关节？平行关节分别计数。

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
        "id": "cell-0-shuttle-joint",
        "name": "cell-0-shuttle interface",
        "parent": "foundation",
        "child": "cell-0-shuttle",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.4999999999999999,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-0-mount-joint",
        "name": "cell-0-mount interface",
        "parent": "cell-0-shuttle",
        "child": "cell-0-mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.55,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-pedestal-joint",
        "name": "cell-0-pedestal interface",
        "parent": "cell-0-mount",
        "child": "cell-0-pedestal",
        "type": "fixed",
        "anchorParent": [
          0,
          0.8500000000000001,
          0
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-rotor-joint",
        "name": "cell-0-rotor interface",
        "parent": "cell-0-pedestal",
        "child": "cell-0-rotor",
        "type": "revolute",
        "anchorParent": [
          0,
          1,
          0
        ],
        "anchorChild": [
          0,
          -0.04999999999999982,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-0-offset-load-joint",
        "name": "cell-0-offset-load interface",
        "parent": "cell-0-rotor",
        "child": "cell-0-offset-load",
        "type": "fixed",
        "anchorParent": [
          1,
          0.75,
          0.6
        ],
        "anchorChild": [
          0,
          -0.16249999999999964,
          1.1102230246251565e-16
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-upper-stage-joint",
        "name": "cell-0-upper-stage interface",
        "parent": "cell-0-rotor",
        "child": "cell-0-upper-stage",
        "type": "prismatic",
        "anchorParent": [
          -1,
          1.0499999999999998,
          -1
        ],
        "anchorChild": [
          0,
          -0.04999999999999982,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-0-console-joint",
        "name": "cell-0-console interface",
        "parent": "foundation",
        "child": "cell-0-console",
        "type": "fixed",
        "anchorParent": [
          0,
          1.1,
          6
        ],
        "anchorChild": [
          0,
          -0.5775000000000001,
          0
        ],
        "axis": [
          0,
          1,
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

### 局部改色（h3-exp-d2-turntable-2-recolor）

仅将 cell-0-offset-load-p156 改成 #e8792e，其他零件不变。选择正确补丁。

能力：局部改色；形式：single-choice；证据：model-state。

- A：{"id":"*","color":"#e8792e"}
- B：{"id":"cell-0-offset-load-p156","color":"#e8792e"}
- C：{"id":"cell-0-offset-load-p157","color":"#e8792e"}
- D：{"id":"cell-0-offset-load-p156","color":"#2878b8"}

```json
{
  "input": {
    "part": {
      "id": "cell-0-offset-load-p156",
      "moduleId": "cell-0-offset-load",
      "shape": "cylinder",
      "position": [
        0,
        -0.16249999999999964,
        1.1102230246251565e-16
      ],
      "size": [
        1.3,
        1.1,
        1.3
      ],
      "color": "#dc6040",
      "rotation": [
        0,
        0,
        0,
        1
      ]
    }
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 补装部件（h3-exp-d2-turntable-2-add）

模块 cell-0-offset-load 缺失零件 cell-0-offset-load-p156。选择与目标清单一致的补装描述。

能力：补装部件；形式：single-choice；证据：model-state。

- A：{"id":"cell-0-offset-load-p156","moduleId":"cell-0-offset-load","shape":"cylinder","position":[0,-0.16249999999999964,1.1102230246251565e-16],"size":[1.3,1.1,1.3],"color":"#dc6040","rotation":[0,0,0,1]}
- B：{"id":"cell-0-offset-load-p156","moduleId":"foundation","shape":"cylinder","position":[0,-0.16249999999999964,1.1102230246251565e-16],"size":[1.3,1.1,1.3],"color":"#dc6040","rotation":[0,0,0,1]}
- C：{"id":"cell-0-offset-load-p156","moduleId":"cell-0-offset-load","shape":"cylinder","position":[0,-0.16249999999999964,1.1102230246251565e-16],"size":[3,3,3],"color":"#dc6040","rotation":[0,0,0,1]}
- D：{"id":"cell-0-offset-load-p156","moduleId":"cell-0-offset-load","shape":"cylinder","position":[0,-0.16249999999999964,1.1102230246251565e-16],"size":[1.3,1.1,1.3],"color":"#000000","rotation":[0,0,0,1]}

```json
{
  "input": {
    "targetPart": {
      "id": "cell-0-offset-load-p156",
      "moduleId": "cell-0-offset-load",
      "shape": "cylinder",
      "position": [
        0,
        -0.16249999999999964,
        1.1102230246251565e-16
      ],
      "size": [
        1.3,
        1.1,
        1.3
      ],
      "color": "#dc6040",
      "rotation": [
        0,
        0,
        0,
        1
      ]
    },
    "existingIds": [
      "foundation-p0",
      "foundation-p1",
      "foundation-p2",
      "foundation-p3",
      "foundation-p4",
      "foundation-p5",
      "foundation-p6",
      "foundation-p7",
      "foundation-p8",
      "foundation-p9",
      "foundation-p10",
      "foundation-p11",
      "foundation-p12",
      "foundation-p13",
      "foundation-p14",
      "foundation-p15",
      "foundation-p16",
      "foundation-p17",
      "foundation-p18",
      "foundation-p19",
      "foundation-p20",
      "foundation-p21",
      "foundation-p22",
      "foundation-p23",
      "foundation-p24",
      "foundation-p25",
      "foundation-p26",
      "foundation-p27",
      "foundation-p28",
      "foundation-p29",
      "foundation-p30",
      "foundation-p31",
      "foundation-p32",
      "foundation-p33",
      "foundation-p34",
      "foundation-p35",
      "foundation-p36",
      "foundation-p37",
      "foundation-p38",
      "foundation-p39",
      "foundation-p40",
      "foundation-p41",
      "foundation-p42",
      "foundation-p43",
      "foundation-p44",
      "foundation-p45",
      "foundation-p46",
      "foundation-p47",
      "foundation-p48",
      "foundation-p49",
      "foundation-p50",
      "foundation-p51",
      "foundation-p52",
      "foundation-p53",
      "foundation-p54",
      "foundation-p55",
      "cell-0-shuttle-p56",
      "cell-0-shuttle-p57",
      "cell-0-shuttle-p58",
      "cell-0-shuttle-p59",
      "cell-0-shuttle-p60",
      "cell-0-shuttle-p61",
      "cell-0-shuttle-p62",
      "cell-0-shuttle-p63",
      "cell-0-shuttle-p64",
      "cell-0-shuttle-p65",
      "cell-0-shuttle-p66",
      "cell-0-shuttle-p67",
      "cell-0-shuttle-p68",
      "cell-0-shuttle-p69",
      "cell-0-shuttle-p70",
      "cell-0-shuttle-p71",
      "cell-0-shuttle-p72",
      "cell-0-shuttle-p73",
      "cell-0-shuttle-p74",
      "cell-0-shuttle-p75",
      "cell-0-shuttle-p76",
      "cell-0-shuttle-p77",
      "cell-0-shuttle-p78",
      "cell-0-shuttle-p79",
      "cell-0-shuttle-p80",
      "cell-0-shuttle-p81",
      "cell-0-shuttle-p82",
      "cell-0-shuttle-p83",
      "cell-0-shuttle-p84",
      "cell-0-shuttle-p85",
      "cell-0-shuttle-p86",
      "cell-0-shuttle-p87",
      "cell-0-shuttle-p88",
      "cell-0-shuttle-p89",
      "cell-0-shuttle-p90",
      "cell-0-shuttle-p91",
      "cell-0-shuttle-p92",
      "cell-0-shuttle-p93",
      "cell-0-shuttle-p94",
      "cell-0-shuttle-p95",
      "cell-0-shuttle-p96",
      "cell-0-shuttle-p97",
      "cell-0-shuttle-p98",
      "cell-0-shuttle-p99",
      "cell-0-shuttle-p100",
      "cell-0-shuttle-p101",
      "cell-0-shuttle-p102",
      "cell-0-shuttle-p103",
      "cell-0-mount-p104",
      "cell-0-mount-p105",
      "cell-0-mount-p106",
      "cell-0-mount-p107",
      "cell-0-mount-p108",
      "cell-0-mount-p109",
      "cell-0-mount-p110",
      "cell-0-mount-p111",
      "cell-0-mount-p112",
      "cell-0-mount-p113",
      "cell-0-mount-p114",
      "cell-0-mount-p115",
      "cell-0-mount-p116",
      "cell-0-mount-p117",
      "cell-0-mount-p118",
      "cell-0-mount-p119",
      "cell-0-mount-p120",
      "cell-0-mount-p121",
      "cell-0-mount-p122",
      "cell-0-mount-p123",
      "cell-0-mount-p124",
      "cell-0-mount-p125",
      "cell-0-mount-p126",
      "cell-0-mount-p127",
      "cell-0-mount-p128",
      "cell-0-mount-p129",
      "cell-0-mount-p130",
      "cell-0-mount-p131",
      "cell-0-mount-p132",
      "cell-0-mount-p133",
      "cell-0-mount-p134",
      "cell-0-mount-p135",
      "cell-0-mount-p136",
      "cell-0-mount-p137",
      "cell-0-mount-p138",
      "cell-0-pedestal-p139",
      "cell-0-rotor-p140",
      "cell-0-rotor-p141",
      "cell-0-rotor-p142",
      "cell-0-rotor-p143",
      "cell-0-rotor-p144",
      "cell-0-rotor-p145",
      "cell-0-rotor-p146",
      "cell-0-rotor-p147",
      "cell-0-rotor-p148",
      "cell-0-rotor-p149",
      "cell-0-rotor-p150",
      "cell-0-rotor-p151",
      "cell-0-rotor-p152",
      "cell-0-rotor-p153",
      "cell-0-rotor-p154",
      "cell-0-rotor-p155",
      "cell-0-offset-load-p157",
      "cell-0-upper-stage-p158",
      "cell-0-upper-stage-p159",
      "cell-0-upper-stage-p160",
      "cell-0-upper-stage-p161",
      "cell-0-console-p162",
      "cell-0-console-p163",
      "cell-0-console-p164",
      "cell-0-console-p165",
      "cell-0-console-p166",
      "cell-0-console-p167",
      "cell-0-console-p168",
      "cell-0-console-p169"
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 安全拆除（h3-exp-d2-turntable-2-remove）

按声明依赖图，当前可以先拆哪些叶模块？

能力：安全拆除；形式：single-choice；证据：model-state。

- A：[]
- B：["foundation","cell-0-shuttle","cell-0-mount","cell-0-pedestal","cell-0-rotor","cell-0-offset-load","cell-0-upper-stage","cell-0-console"]
- C：["cell-0-console","cell-0-offset-load","cell-0-upper-stage"]
- D：["foundation"]

```json
{
  "input": {
    "joints": [
      {
        "id": "cell-0-shuttle-joint",
        "name": "cell-0-shuttle interface",
        "parent": "foundation",
        "child": "cell-0-shuttle",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.4999999999999999,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-0-mount-joint",
        "name": "cell-0-mount interface",
        "parent": "cell-0-shuttle",
        "child": "cell-0-mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.55,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-pedestal-joint",
        "name": "cell-0-pedestal interface",
        "parent": "cell-0-mount",
        "child": "cell-0-pedestal",
        "type": "fixed",
        "anchorParent": [
          0,
          0.8500000000000001,
          0
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-rotor-joint",
        "name": "cell-0-rotor interface",
        "parent": "cell-0-pedestal",
        "child": "cell-0-rotor",
        "type": "revolute",
        "anchorParent": [
          0,
          1,
          0
        ],
        "anchorChild": [
          0,
          -0.04999999999999982,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-0-offset-load-joint",
        "name": "cell-0-offset-load interface",
        "parent": "cell-0-rotor",
        "child": "cell-0-offset-load",
        "type": "fixed",
        "anchorParent": [
          1,
          0.75,
          0.6
        ],
        "anchorChild": [
          0,
          -0.16249999999999964,
          1.1102230246251565e-16
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-upper-stage-joint",
        "name": "cell-0-upper-stage interface",
        "parent": "cell-0-rotor",
        "child": "cell-0-upper-stage",
        "type": "prismatic",
        "anchorParent": [
          -1,
          1.0499999999999998,
          -1
        ],
        "anchorChild": [
          0,
          -0.04999999999999982,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-0-console-joint",
        "name": "cell-0-console interface",
        "parent": "foundation",
        "child": "cell-0-console",
        "type": "fixed",
        "anchorParent": [
          0,
          1.1,
          6
        ],
        "anchorChild": [
          0,
          -0.5775000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      }
    ],
    "modules": [
      "foundation",
      "cell-0-shuttle",
      "cell-0-mount",
      "cell-0-pedestal",
      "cell-0-rotor",
      "cell-0-offset-load",
      "cell-0-upper-stage",
      "cell-0-console"
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 替换选择（h3-exp-d2-turntable-2-replace）

在成本上限内选择刚度最大的替换件；并列选成本低者，再并列选ID字典序最小者。

能力：替换选择；形式：single-choice；证据：model-state。

- A：stock-0
- B：stock-2
- C：stock-3
- D：stock-1

```json
{
  "input": {
    "alternatives": [
      {
        "id": "stock-0",
        "cost": 7,
        "stiffness": 3,
        "mass": 1.5
      },
      {
        "id": "stock-1",
        "cost": 7,
        "stiffness": 8,
        "mass": 0.5
      },
      {
        "id": "stock-2",
        "cost": 2,
        "stiffness": 4,
        "mass": 1.9
      },
      {
        "id": "stock-3",
        "cost": 7,
        "stiffness": 8,
        "mass": 1.1
      }
    ],
    "maxCost": 7
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 平移纠偏（h3-exp-d2-turntable-2-translate）

观察到相对目标的平移误差 delta，选择补偿平移。

能力：平移纠偏；形式：single-choice；证据：model-state。

- A：[-2,0,2]
- B：[2,0,-2]
- C：[0,0,0]
- D：[0,2,0]

```json
{
  "input": {
    "delta": [
      2,
      0,
      -2
    ],
    "target": "cell-0-offset-load"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 姿态纠偏（h3-exp-d2-turntable-2-rotate）

选择从当前yaw到目标yaw的最短有符号旋转；恰好180°时使用-180°。

能力：姿态纠偏；形式：single-choice；证据：model-state。

- A：-90
- B：90
- C：0
- D：-180

```json
{
  "input": {
    "module": "cell-0-offset-load",
    "currentYaw": 135,
    "targetYaw": 45
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 下一步放置（h3-exp-d2-turntable-2-next-module）

已完成给定前缀，选择所有前置依赖已满足的下一模块集合。

能力：下一步放置；形式：single-choice；证据：model-state。

- A：["foundation","cell-0-shuttle","cell-0-mount","cell-0-pedestal"]
- B：["cell-0-rotor","cell-0-offset-load","cell-0-upper-stage","cell-0-console"]
- C：["cell-0-console","cell-0-rotor"]
- D：[]

```json
{
  "input": {
    "prefix": [
      "foundation",
      "cell-0-shuttle",
      "cell-0-mount",
      "cell-0-pedestal"
    ],
    "joints": [
      {
        "id": "cell-0-shuttle-joint",
        "name": "cell-0-shuttle interface",
        "parent": "foundation",
        "child": "cell-0-shuttle",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.4999999999999999,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-0-mount-joint",
        "name": "cell-0-mount interface",
        "parent": "cell-0-shuttle",
        "child": "cell-0-mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.55,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-pedestal-joint",
        "name": "cell-0-pedestal interface",
        "parent": "cell-0-mount",
        "child": "cell-0-pedestal",
        "type": "fixed",
        "anchorParent": [
          0,
          0.8500000000000001,
          0
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-rotor-joint",
        "name": "cell-0-rotor interface",
        "parent": "cell-0-pedestal",
        "child": "cell-0-rotor",
        "type": "revolute",
        "anchorParent": [
          0,
          1,
          0
        ],
        "anchorChild": [
          0,
          -0.04999999999999982,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-0-offset-load-joint",
        "name": "cell-0-offset-load interface",
        "parent": "cell-0-rotor",
        "child": "cell-0-offset-load",
        "type": "fixed",
        "anchorParent": [
          1,
          0.75,
          0.6
        ],
        "anchorChild": [
          0,
          -0.16249999999999964,
          1.1102230246251565e-16
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-upper-stage-joint",
        "name": "cell-0-upper-stage interface",
        "parent": "cell-0-rotor",
        "child": "cell-0-upper-stage",
        "type": "prismatic",
        "anchorParent": [
          -1,
          1.0499999999999998,
          -1
        ],
        "anchorChild": [
          0,
          -0.04999999999999982,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-0-console-joint",
        "name": "cell-0-console interface",
        "parent": "foundation",
        "child": "cell-0-console",
        "type": "fixed",
        "anchorParent": [
          0,
          1.1,
          6
        ],
        "anchorChild": [
          0,
          -0.5775000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      }
    ],
    "modules": [
      "foundation",
      "cell-0-shuttle",
      "cell-0-mount",
      "cell-0-pedestal",
      "cell-0-rotor",
      "cell-0-offset-load",
      "cell-0-upper-stage",
      "cell-0-console"
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 库存核算（h3-exp-d2-turntable-2-inventory）

备件库有 6 件，替换模块需 2 件，还剩多少？

能力：库存核算；形式：single-choice；证据：model-state。

- A：4
- B：5
- C：3
- D：7

```json
{
  "input": {
    "available": 6,
    "required": 2
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 子装配边界（h3-exp-d2-turntable-2-boundary）

隔离 cell-0-offset-load 需要断开哪些边界关节？

能力：子装配边界；形式：single-choice；证据：model-state。

- A：["cell-0-offset-load-joint"]
- B：[]
- C：["cell-0-shuttle-joint","cell-0-mount-joint","cell-0-pedestal-joint","cell-0-rotor-joint","cell-0-offset-load-joint","cell-0-upper-stage-joint","cell-0-console-joint"]
- D：["cell-0-rotor-joint"]

```json
{
  "input": {
    "joints": [
      {
        "id": "cell-0-shuttle-joint",
        "name": "cell-0-shuttle interface",
        "parent": "foundation",
        "child": "cell-0-shuttle",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.4999999999999999,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-0-mount-joint",
        "name": "cell-0-mount interface",
        "parent": "cell-0-shuttle",
        "child": "cell-0-mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.55,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-pedestal-joint",
        "name": "cell-0-pedestal interface",
        "parent": "cell-0-mount",
        "child": "cell-0-pedestal",
        "type": "fixed",
        "anchorParent": [
          0,
          0.8500000000000001,
          0
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-rotor-joint",
        "name": "cell-0-rotor interface",
        "parent": "cell-0-pedestal",
        "child": "cell-0-rotor",
        "type": "revolute",
        "anchorParent": [
          0,
          1,
          0
        ],
        "anchorChild": [
          0,
          -0.04999999999999982,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-0-offset-load-joint",
        "name": "cell-0-offset-load interface",
        "parent": "cell-0-rotor",
        "child": "cell-0-offset-load",
        "type": "fixed",
        "anchorParent": [
          1,
          0.75,
          0.6
        ],
        "anchorChild": [
          0,
          -0.16249999999999964,
          1.1102230246251565e-16
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-upper-stage-joint",
        "name": "cell-0-upper-stage interface",
        "parent": "cell-0-rotor",
        "child": "cell-0-upper-stage",
        "type": "prismatic",
        "anchorParent": [
          -1,
          1.0499999999999998,
          -1
        ],
        "anchorChild": [
          0,
          -0.04999999999999982,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-0-console-joint",
        "name": "cell-0-console interface",
        "parent": "foundation",
        "child": "cell-0-console",
        "type": "fixed",
        "anchorParent": [
          0,
          1.1,
          6
        ],
        "anchorChild": [
          0,
          -0.5775000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      }
    ],
    "target": "cell-0-offset-load"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 最小干预（h3-exp-d2-turntable-2-no-op）

当前模块颜色已满足指令，且无需改变位姿。最少需要几次编辑？

能力：最小干预；形式：single-choice；证据：model-state。

- A：0
- B：1
- C：2

```json
{
  "input": {
    "module": "cell-0-offset-load"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 全过程依赖（h3-exp-d2-turntable-2-prefix）

给定候选顺序，首次违反前置依赖的步骤是？从 0 编号，-1 表示没有违反。

能力：全过程依赖；形式：single-choice；证据：support-graph。

- A：3
- B：-1
- C：4
- D：7

```json
{
  "input": {
    "order": [
      "foundation",
      "cell-0-shuttle",
      "cell-0-mount",
      "cell-0-rotor",
      "cell-0-pedestal",
      "cell-0-offset-load",
      "cell-0-upper-stage",
      "cell-0-console"
    ],
    "joints": [
      {
        "id": "cell-0-shuttle-joint",
        "name": "cell-0-shuttle interface",
        "parent": "foundation",
        "child": "cell-0-shuttle",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.4999999999999999,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-0-mount-joint",
        "name": "cell-0-mount interface",
        "parent": "cell-0-shuttle",
        "child": "cell-0-mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.55,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-pedestal-joint",
        "name": "cell-0-pedestal interface",
        "parent": "cell-0-mount",
        "child": "cell-0-pedestal",
        "type": "fixed",
        "anchorParent": [
          0,
          0.8500000000000001,
          0
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-rotor-joint",
        "name": "cell-0-rotor interface",
        "parent": "cell-0-pedestal",
        "child": "cell-0-rotor",
        "type": "revolute",
        "anchorParent": [
          0,
          1,
          0
        ],
        "anchorChild": [
          0,
          -0.04999999999999982,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-0-offset-load-joint",
        "name": "cell-0-offset-load interface",
        "parent": "cell-0-rotor",
        "child": "cell-0-offset-load",
        "type": "fixed",
        "anchorParent": [
          1,
          0.75,
          0.6
        ],
        "anchorChild": [
          0,
          -0.16249999999999964,
          1.1102230246251565e-16
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-upper-stage-joint",
        "name": "cell-0-upper-stage interface",
        "parent": "cell-0-rotor",
        "child": "cell-0-upper-stage",
        "type": "prismatic",
        "anchorParent": [
          -1,
          1.0499999999999998,
          -1
        ],
        "anchorChild": [
          0,
          -0.04999999999999982,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-0-console-joint",
        "name": "cell-0-console interface",
        "parent": "foundation",
        "child": "cell-0-console",
        "type": "fixed",
        "anchorParent": [
          0,
          1.1,
          6
        ],
        "anchorChild": [
          0,
          -0.5775000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      }
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 连续维修路径（h3-exp-d2-turntable-2-access）

根据实际 Rapier shape cast 记录，选择全部无碰撞路径。

能力：连续维修路径；形式：multiple-choice；证据：Rapier。

- A：path-1
- B：path-2
- C：path-0

```json
{
  "input": {
    "paths": [
      {
        "id": "path-0",
        "start": [
          7.98,
          4.1625,
          0.5999999999999999
        ],
        "end": [
          1,
          4.1625,
          0.5999999999999999
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
          1,
          8.875,
          0.5999999999999999
        ],
        "end": [
          1,
          4.1625,
          0.5999999999999999
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
        "id": "path-2",
        "start": [
          1,
          4.1625,
          10.98
        ],
        "end": [
          1,
          4.1625,
          0.5999999999999999
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
      "A",
      "B",
      "C"
    ]
  }
}
```

### 支撑反事实（h3-exp-d2-turntable-2-counterfactual）

移除指定模块后，哪些其余模块失去到任一基座的关节路径？不包含被移除模块本身。

能力：支撑反事实；形式：single-choice；证据：support-graph。

- A：[]
- B：["foundation","cell-0-shuttle","cell-0-mount","cell-0-pedestal","cell-0-rotor","cell-0-offset-load","cell-0-upper-stage","cell-0-console"]
- C：["cell-0-mount","cell-0-offset-load","cell-0-pedestal","cell-0-rotor","cell-0-upper-stage"]
- D：["cell-0-shuttle"]

```json
{
  "input": {
    "removed": "cell-0-shuttle",
    "roots": [
      "foundation"
    ],
    "joints": [
      {
        "id": "cell-0-shuttle-joint",
        "name": "cell-0-shuttle interface",
        "parent": "foundation",
        "child": "cell-0-shuttle",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.4999999999999999,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-0-mount-joint",
        "name": "cell-0-mount interface",
        "parent": "cell-0-shuttle",
        "child": "cell-0-mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.55,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-pedestal-joint",
        "name": "cell-0-pedestal interface",
        "parent": "cell-0-mount",
        "child": "cell-0-pedestal",
        "type": "fixed",
        "anchorParent": [
          0,
          0.8500000000000001,
          0
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-rotor-joint",
        "name": "cell-0-rotor interface",
        "parent": "cell-0-pedestal",
        "child": "cell-0-rotor",
        "type": "revolute",
        "anchorParent": [
          0,
          1,
          0
        ],
        "anchorChild": [
          0,
          -0.04999999999999982,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-0-offset-load-joint",
        "name": "cell-0-offset-load interface",
        "parent": "cell-0-rotor",
        "child": "cell-0-offset-load",
        "type": "fixed",
        "anchorParent": [
          1,
          0.75,
          0.6
        ],
        "anchorChild": [
          0,
          -0.16249999999999964,
          1.1102230246251565e-16
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-upper-stage-joint",
        "name": "cell-0-upper-stage interface",
        "parent": "cell-0-rotor",
        "child": "cell-0-upper-stage",
        "type": "prismatic",
        "anchorParent": [
          -1,
          1.0499999999999998,
          -1
        ],
        "anchorChild": [
          0,
          -0.04999999999999982,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-0-console-joint",
        "name": "cell-0-console interface",
        "parent": "foundation",
        "child": "cell-0-console",
        "type": "fixed",
        "anchorParent": [
          0,
          1.1,
          6
        ],
        "anchorChild": [
          0,
          -0.5775000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      }
    ],
    "modules": [
      "foundation",
      "cell-0-shuttle",
      "cell-0-mount",
      "cell-0-pedestal",
      "cell-0-rotor",
      "cell-0-offset-load",
      "cell-0-upper-stage",
      "cell-0-console"
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 冲击响应读数（h3-exp-d2-turntable-2-dynamic）

Rapier 实际采样轨迹中的最大平移位移是多少？按四位小数报告。

能力：冲击响应读数；形式：single-choice；证据：Rapier。

- A：1.0007
- B：0.0007
- C：0.2007
- D：0

```json
{
  "input": {
    "trace": [
      {
        "time": 0.008333333333333333,
        "displacement": 0.0007247338170267352
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.000006794929504394531
      },
      {
        "time": 0.20833333333333334,
        "displacement": 3.209808353861871e-7
      },
      {
        "time": 0.30833333333333335,
        "displacement": 2.6656007498500226e-7
      },
      {
        "time": 0.4083333333333333,
        "displacement": 2.149076029934877e-7
      },
      {
        "time": 0.5083333333333333,
        "displacement": 2.149076029934877e-7
      },
      {
        "time": 0.6083333333333333,
        "displacement": 2.149076029934877e-7
      },
      {
        "time": 0.7083333333333334,
        "displacement": 2.149076029934877e-7
      },
      {
        "time": 0.8083333333333333,
        "displacement": 2.149076029934877e-7
      },
      {
        "time": 0.9083333333333333,
        "displacement": 2.149076029934877e-7
      },
      {
        "time": 1,
        "displacement": 2.149076029934877e-7
      }
    ],
    "impulse": [
      10,
      1.8,
      3.5
    ],
    "nominalDrift": 0.00008878781911037729,
    "scope": "采样轨迹极值，非连续时间极值；不代表实物安全阈值"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 关节限位推理（h3-exp-d2-turntable-2-kinematic）

下列目标位置/角度中哪些在关节声明限位内（含边界）？

能力：关节限位推理；形式：multiple-choice；证据：model-state。

- A：1.1
- B：-0.6
- C：0
- D：-1.1

```json
{
  "input": {
    "joint": "cell-0-rotor-joint",
    "limits": [
      -0.6,
      0.6
    ],
    "units": "radians"
  },
  "answer": {
    "choiceIds": [
      "B",
      "C"
    ]
  }
}
```

### 约束故障诊断（h3-exp-d2-turntable-2-diagnosis）

已检测到端点和约束类型如下，选择匹配的全部关节。

能力：约束故障诊断；形式：multiple-choice；证据：model-state。

- A：cell-0-shuttle-joint
- B：cell-0-mount-joint
- C：cell-0-pedestal-joint
- D：cell-0-offset-load-joint

```json
{
  "input": {
    "endpoints": [
      "cell-0-rotor",
      "cell-0-offset-load"
    ],
    "type": "fixed",
    "joints": [
      {
        "id": "cell-0-shuttle-joint",
        "name": "cell-0-shuttle interface",
        "parent": "foundation",
        "child": "cell-0-shuttle",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.4999999999999999,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-0-mount-joint",
        "name": "cell-0-mount interface",
        "parent": "cell-0-shuttle",
        "child": "cell-0-mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.55,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-pedestal-joint",
        "name": "cell-0-pedestal interface",
        "parent": "cell-0-mount",
        "child": "cell-0-pedestal",
        "type": "fixed",
        "anchorParent": [
          0,
          0.8500000000000001,
          0
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-rotor-joint",
        "name": "cell-0-rotor interface",
        "parent": "cell-0-pedestal",
        "child": "cell-0-rotor",
        "type": "revolute",
        "anchorParent": [
          0,
          1,
          0
        ],
        "anchorChild": [
          0,
          -0.04999999999999982,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-0-offset-load-joint",
        "name": "cell-0-offset-load interface",
        "parent": "cell-0-rotor",
        "child": "cell-0-offset-load",
        "type": "fixed",
        "anchorParent": [
          1,
          0.75,
          0.6
        ],
        "anchorChild": [
          0,
          -0.16249999999999964,
          1.1102230246251565e-16
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-upper-stage-joint",
        "name": "cell-0-upper-stage interface",
        "parent": "cell-0-rotor",
        "child": "cell-0-upper-stage",
        "type": "prismatic",
        "anchorParent": [
          -1,
          1.0499999999999998,
          -1
        ],
        "anchorChild": [
          0,
          -0.04999999999999982,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-0-console-joint",
        "name": "cell-0-console interface",
        "parent": "foundation",
        "child": "cell-0-console",
        "type": "fixed",
        "anchorParent": [
          0,
          1.1,
          6
        ],
        "anchorChild": [
          0,
          -0.5775000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      }
    ]
  },
  "answer": {
    "choiceIds": [
      "D"
    ]
  }
}
```

### 主动检查收益（h3-exp-d2-turntable-2-information-gain）

均匀先验四个世界，选择信息增益/成本最大的全部检查。

能力：主动检查收益；形式：multiple-choice；证据：finite-world。

- A：query-0
- B：query-1
- C：query-2

```json
{
  "input": {
    "queries": [
      {
        "id": "query-0",
        "cost": 2,
        "returns": [
          0,
          0,
          1,
          1
        ]
      },
      {
        "id": "query-1",
        "cost": 3,
        "returns": [
          0,
          1,
          2,
          3
        ]
      },
      {
        "id": "query-2",
        "cost": 1,
        "returns": [
          0,
          0,
          0,
          1
        ]
      }
    ],
    "module": "cell-0-offset-load",
    "worlds": [
      "normal",
      "jammed",
      "reversed",
      "loose"
    ]
  },
  "answer": {
    "choiceIds": [
      "C"
    ]
  }
}
```

### 不确定性与弃答（h3-exp-d2-turntable-2-abstention）

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

### 观测后信念更新（h3-exp-d2-turntable-2-posterior）

均匀先验，得到给定观测后，jammed 世界的后验概率是多少？

能力：观测后信念更新；形式：single-choice；证据：finite-world。

- A：0.3333333333333333
- B：0.5
- C：0
- D：0.25

```json
{
  "input": {
    "module": "cell-0-offset-load",
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
    "choiceId": "C"
  }
}
```

### 多目标工程权衡（h3-exp-d2-turntable-2-pareto）

最小成本、最小质量、最大刚度，选择完整非支配集合。

能力：多目标工程权衡；形式：multiple-choice；证据：model-state。

- A：stock-0
- B：stock-3
- C：stock-1
- D：stock-2

```json
{
  "input": {
    "alternatives": [
      {
        "id": "stock-0",
        "cost": 7,
        "stiffness": 3,
        "mass": 1.5
      },
      {
        "id": "stock-1",
        "cost": 7,
        "stiffness": 8,
        "mass": 0.5
      },
      {
        "id": "stock-2",
        "cost": 2,
        "stiffness": 4,
        "mass": 1.9
      },
      {
        "id": "stock-3",
        "cost": 7,
        "stiffness": 8,
        "mass": 1.1
      }
    ]
  },
  "answer": {
    "choiceIds": [
      "C",
      "D"
    ]
  }
}
```

### 依赖装配（h3-exp-d2-turntable-2-assembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖装配；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [],
    "initialModules": [],
    "actions": [
      {
        "id": "place:cell-0-rotor",
        "label": "安装 cell-0-rotor",
        "requires": [
          "present:cell-0-pedestal"
        ],
        "forbids": [
          "present:cell-0-rotor"
        ],
        "adds": [
          "present:cell-0-rotor"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-rotor",
          "visible": true
        }
      },
      {
        "id": "place:cell-0-pedestal",
        "label": "安装 cell-0-pedestal",
        "requires": [
          "present:cell-0-mount"
        ],
        "forbids": [
          "present:cell-0-pedestal"
        ],
        "adds": [
          "present:cell-0-pedestal"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-pedestal",
          "visible": true
        }
      },
      {
        "id": "place:cell-0-shuttle",
        "label": "安装 cell-0-shuttle",
        "requires": [
          "present:foundation"
        ],
        "forbids": [
          "present:cell-0-shuttle"
        ],
        "adds": [
          "present:cell-0-shuttle"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-shuttle",
          "visible": true
        }
      },
      {
        "id": "place:cell-0-offset-load",
        "label": "安装 cell-0-offset-load",
        "requires": [
          "present:cell-0-rotor"
        ],
        "forbids": [
          "present:cell-0-offset-load"
        ],
        "adds": [
          "present:cell-0-offset-load"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-offset-load",
          "visible": true
        }
      },
      {
        "id": "place:cell-0-mount",
        "label": "安装 cell-0-mount",
        "requires": [
          "present:cell-0-shuttle"
        ],
        "forbids": [
          "present:cell-0-mount"
        ],
        "adds": [
          "present:cell-0-mount"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-mount",
          "visible": true
        }
      },
      {
        "id": "place:foundation",
        "label": "安装 foundation",
        "requires": [],
        "forbids": [
          "present:foundation"
        ],
        "adds": [
          "present:foundation"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "foundation",
          "visible": true
        }
      },
      {
        "id": "place:cell-0-upper-stage",
        "label": "安装 cell-0-upper-stage",
        "requires": [
          "present:cell-0-rotor"
        ],
        "forbids": [
          "present:cell-0-upper-stage"
        ],
        "adds": [
          "present:cell-0-upper-stage"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-upper-stage",
          "visible": true
        }
      },
      {
        "id": "place:cell-0-console",
        "label": "安装 cell-0-console",
        "requires": [
          "present:foundation"
        ],
        "forbids": [
          "present:cell-0-console"
        ],
        "adds": [
          "present:cell-0-console"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-console",
          "visible": true
        }
      }
    ],
    "goalFacts": [
      "present:foundation",
      "present:cell-0-shuttle",
      "present:cell-0-mount",
      "present:cell-0-pedestal",
      "present:cell-0-rotor",
      "present:cell-0-offset-load",
      "present:cell-0-upper-stage",
      "present:cell-0-console"
    ],
    "budget": 8,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "place:foundation",
      "place:cell-0-shuttle",
      "place:cell-0-mount",
      "place:cell-0-pedestal",
      "place:cell-0-rotor",
      "place:cell-0-offset-load",
      "place:cell-0-upper-stage",
      "place:cell-0-console"
    ]
  }
}
```

### 依赖拆解（h3-exp-d2-turntable-2-disassembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖拆解；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "present:foundation",
      "present:cell-0-shuttle",
      "present:cell-0-mount",
      "present:cell-0-pedestal",
      "present:cell-0-rotor",
      "present:cell-0-offset-load",
      "present:cell-0-upper-stage",
      "present:cell-0-console"
    ],
    "initialModules": [
      "foundation",
      "cell-0-shuttle",
      "cell-0-mount",
      "cell-0-pedestal",
      "cell-0-rotor",
      "cell-0-offset-load",
      "cell-0-upper-stage",
      "cell-0-console"
    ],
    "actions": [
      {
        "id": "remove:cell-0-console",
        "label": "拆除 cell-0-console",
        "requires": [
          "present:cell-0-console"
        ],
        "forbids": [],
        "adds": [
          "removed:cell-0-console"
        ],
        "deletes": [
          "present:cell-0-console"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-console",
          "visible": false
        }
      },
      {
        "id": "remove:cell-0-offset-load",
        "label": "拆除 cell-0-offset-load",
        "requires": [
          "present:cell-0-offset-load"
        ],
        "forbids": [],
        "adds": [
          "removed:cell-0-offset-load"
        ],
        "deletes": [
          "present:cell-0-offset-load"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-offset-load",
          "visible": false
        }
      },
      {
        "id": "remove:cell-0-rotor",
        "label": "拆除 cell-0-rotor",
        "requires": [
          "present:cell-0-rotor"
        ],
        "forbids": [
          "present:cell-0-offset-load",
          "present:cell-0-upper-stage"
        ],
        "adds": [
          "removed:cell-0-rotor"
        ],
        "deletes": [
          "present:cell-0-rotor"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-rotor",
          "visible": false
        }
      },
      {
        "id": "remove:foundation",
        "label": "拆除 foundation",
        "requires": [
          "present:foundation"
        ],
        "forbids": [
          "present:cell-0-shuttle",
          "present:cell-0-console"
        ],
        "adds": [
          "removed:foundation"
        ],
        "deletes": [
          "present:foundation"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "foundation",
          "visible": false
        }
      },
      {
        "id": "remove:cell-0-pedestal",
        "label": "拆除 cell-0-pedestal",
        "requires": [
          "present:cell-0-pedestal"
        ],
        "forbids": [
          "present:cell-0-rotor"
        ],
        "adds": [
          "removed:cell-0-pedestal"
        ],
        "deletes": [
          "present:cell-0-pedestal"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-pedestal",
          "visible": false
        }
      },
      {
        "id": "remove:cell-0-mount",
        "label": "拆除 cell-0-mount",
        "requires": [
          "present:cell-0-mount"
        ],
        "forbids": [
          "present:cell-0-pedestal"
        ],
        "adds": [
          "removed:cell-0-mount"
        ],
        "deletes": [
          "present:cell-0-mount"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-mount",
          "visible": false
        }
      },
      {
        "id": "remove:cell-0-upper-stage",
        "label": "拆除 cell-0-upper-stage",
        "requires": [
          "present:cell-0-upper-stage"
        ],
        "forbids": [],
        "adds": [
          "removed:cell-0-upper-stage"
        ],
        "deletes": [
          "present:cell-0-upper-stage"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-upper-stage",
          "visible": false
        }
      },
      {
        "id": "remove:cell-0-shuttle",
        "label": "拆除 cell-0-shuttle",
        "requires": [
          "present:cell-0-shuttle"
        ],
        "forbids": [
          "present:cell-0-mount"
        ],
        "adds": [
          "removed:cell-0-shuttle"
        ],
        "deletes": [
          "present:cell-0-shuttle"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-shuttle",
          "visible": false
        }
      }
    ],
    "goalFacts": [
      "removed:cell-0-console",
      "removed:cell-0-upper-stage",
      "removed:cell-0-offset-load",
      "removed:cell-0-rotor",
      "removed:cell-0-pedestal",
      "removed:cell-0-mount",
      "removed:cell-0-shuttle",
      "removed:foundation"
    ],
    "budget": 8,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "remove:cell-0-console",
      "remove:cell-0-offset-load",
      "remove:cell-0-upper-stage",
      "remove:cell-0-rotor",
      "remove:cell-0-pedestal",
      "remove:cell-0-mount",
      "remove:cell-0-shuttle",
      "remove:foundation"
    ]
  }
}
```

### 承载维修（h3-exp-d2-turntable-2-service-repair）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：承载维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:cell-0-offset-load",
      "closed:cell-0-offset-load"
    ],
    "initialModules": [
      "foundation",
      "cell-0-shuttle",
      "cell-0-mount",
      "cell-0-pedestal",
      "cell-0-rotor",
      "cell-0-offset-load",
      "cell-0-upper-stage",
      "cell-0-console"
    ],
    "actions": [
      {
        "id": "open:cell-0-offset-load",
        "label": "open cell-0-offset-load",
        "requires": [
          "done:support:cell-0-offset-load"
        ],
        "forbids": [
          "done:open:cell-0-offset-load"
        ],
        "adds": [
          "done:open:cell-0-offset-load"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-offset-load"
        }
      },
      {
        "id": "remove:cell-0-offset-load",
        "label": "remove cell-0-offset-load",
        "requires": [
          "done:open:cell-0-offset-load"
        ],
        "forbids": [
          "done:remove:cell-0-offset-load"
        ],
        "adds": [
          "done:remove:cell-0-offset-load"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-offset-load",
          "visible": false
        }
      },
      {
        "id": "replace:cell-0-offset-load",
        "label": "replace cell-0-offset-load",
        "requires": [
          "done:remove:cell-0-offset-load"
        ],
        "forbids": [
          "done:replace:cell-0-offset-load"
        ],
        "adds": [
          "done:replace:cell-0-offset-load"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-offset-load",
          "visible": true
        }
      },
      {
        "id": "close:cell-0-offset-load",
        "label": "close cell-0-offset-load",
        "requires": [
          "done:verify:cell-0-offset-load"
        ],
        "forbids": [
          "done:close:cell-0-offset-load"
        ],
        "adds": [
          "done:close:cell-0-offset-load"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-offset-load"
        }
      },
      {
        "id": "support:cell-0-offset-load",
        "label": "support cell-0-offset-load",
        "requires": [
          "fault:cell-0-offset-load"
        ],
        "forbids": [
          "done:support:cell-0-offset-load"
        ],
        "adds": [
          "done:support:cell-0-offset-load"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-offset-load"
        }
      },
      {
        "id": "release:cell-0-offset-load",
        "label": "release cell-0-offset-load",
        "requires": [
          "done:close:cell-0-offset-load"
        ],
        "forbids": [
          "done:release:cell-0-offset-load"
        ],
        "adds": [
          "done:release:cell-0-offset-load",
          "repaired:cell-0-offset-load"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-offset-load"
        }
      },
      {
        "id": "verify:cell-0-offset-load",
        "label": "verify cell-0-offset-load",
        "requires": [
          "done:replace:cell-0-offset-load"
        ],
        "forbids": [
          "done:verify:cell-0-offset-load"
        ],
        "adds": [
          "done:verify:cell-0-offset-load"
        ],
        "deletes": [
          "fault:cell-0-offset-load"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-offset-load"
        }
      }
    ],
    "goalFacts": [
      "repaired:cell-0-offset-load"
    ],
    "budget": 7,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:cell-0-offset-load",
      "open:cell-0-offset-load",
      "remove:cell-0-offset-load",
      "replace:cell-0-offset-load",
      "verify:cell-0-offset-load",
      "close:cell-0-offset-load",
      "release:cell-0-offset-load"
    ]
  }
}
```

### 复合编辑验证（h3-exp-d2-turntable-2-compound-edit）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：复合编辑验证；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:cell-0-offset-load",
      "closed:cell-0-offset-load"
    ],
    "initialModules": [
      "foundation",
      "cell-0-shuttle",
      "cell-0-mount",
      "cell-0-pedestal",
      "cell-0-rotor",
      "cell-0-offset-load",
      "cell-0-upper-stage",
      "cell-0-console"
    ],
    "actions": [
      {
        "id": "open:cell-0-offset-load",
        "label": "open cell-0-offset-load",
        "requires": [
          "done:support:cell-0-offset-load"
        ],
        "forbids": [
          "done:open:cell-0-offset-load"
        ],
        "adds": [
          "done:open:cell-0-offset-load"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-offset-load"
        }
      },
      {
        "id": "close:cell-0-offset-load",
        "label": "close cell-0-offset-load",
        "requires": [
          "done:verify:cell-0-offset-load"
        ],
        "forbids": [
          "done:close:cell-0-offset-load"
        ],
        "adds": [
          "done:close:cell-0-offset-load"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-offset-load"
        }
      },
      {
        "id": "support:cell-0-offset-load",
        "label": "support cell-0-offset-load",
        "requires": [
          "fault:cell-0-offset-load"
        ],
        "forbids": [
          "done:support:cell-0-offset-load"
        ],
        "adds": [
          "done:support:cell-0-offset-load"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-offset-load"
        }
      },
      {
        "id": "recolor:cell-0-offset-load",
        "label": "recolor cell-0-offset-load",
        "requires": [
          "done:open:cell-0-offset-load"
        ],
        "forbids": [
          "done:recolor:cell-0-offset-load"
        ],
        "adds": [
          "done:recolor:cell-0-offset-load"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-offset-load",
          "color": "#ea7635"
        }
      },
      {
        "id": "release:cell-0-offset-load",
        "label": "release cell-0-offset-load",
        "requires": [
          "done:close:cell-0-offset-load"
        ],
        "forbids": [
          "done:release:cell-0-offset-load"
        ],
        "adds": [
          "done:release:cell-0-offset-load",
          "repaired:cell-0-offset-load"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-offset-load"
        }
      },
      {
        "id": "verify:cell-0-offset-load",
        "label": "verify cell-0-offset-load",
        "requires": [
          "done:recolor:cell-0-offset-load"
        ],
        "forbids": [
          "done:verify:cell-0-offset-load"
        ],
        "adds": [
          "done:verify:cell-0-offset-load"
        ],
        "deletes": [
          "fault:cell-0-offset-load"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-offset-load"
        }
      }
    ],
    "goalFacts": [
      "repaired:cell-0-offset-load"
    ],
    "budget": 6,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:cell-0-offset-load",
      "open:cell-0-offset-load",
      "recolor:cell-0-offset-load",
      "verify:cell-0-offset-load",
      "close:cell-0-offset-load",
      "release:cell-0-offset-load"
    ]
  }
}
```

### 跨区域联合维修（h3-exp-d2-turntable-2-multi-fault）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：跨区域联合维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:cell-0-upper-stage",
      "closed:cell-0-upper-stage",
      "fault:cell-0-console",
      "closed:cell-0-console"
    ],
    "initialModules": [
      "foundation",
      "cell-0-shuttle",
      "cell-0-mount",
      "cell-0-pedestal",
      "cell-0-rotor",
      "cell-0-offset-load",
      "cell-0-upper-stage",
      "cell-0-console"
    ],
    "actions": [
      {
        "id": "close:cell-0-upper-stage",
        "label": "close cell-0-upper-stage",
        "requires": [
          "done:verify:cell-0-upper-stage"
        ],
        "forbids": [
          "done:close:cell-0-upper-stage"
        ],
        "adds": [
          "done:close:cell-0-upper-stage"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-upper-stage"
        }
      },
      {
        "id": "verify:cell-0-upper-stage",
        "label": "verify cell-0-upper-stage",
        "requires": [
          "done:replace:cell-0-upper-stage"
        ],
        "forbids": [
          "done:verify:cell-0-upper-stage"
        ],
        "adds": [
          "done:verify:cell-0-upper-stage"
        ],
        "deletes": [
          "fault:cell-0-upper-stage"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-upper-stage"
        }
      },
      {
        "id": "remove:cell-0-console",
        "label": "remove cell-0-console",
        "requires": [
          "done:open:cell-0-console"
        ],
        "forbids": [
          "done:remove:cell-0-console"
        ],
        "adds": [
          "done:remove:cell-0-console"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-console",
          "visible": false
        }
      },
      {
        "id": "replace:cell-0-upper-stage",
        "label": "replace cell-0-upper-stage",
        "requires": [
          "done:remove:cell-0-upper-stage"
        ],
        "forbids": [
          "done:replace:cell-0-upper-stage"
        ],
        "adds": [
          "done:replace:cell-0-upper-stage"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-upper-stage",
          "visible": true
        }
      },
      {
        "id": "replace:cell-0-console",
        "label": "replace cell-0-console",
        "requires": [
          "done:remove:cell-0-console"
        ],
        "forbids": [
          "done:replace:cell-0-console"
        ],
        "adds": [
          "done:replace:cell-0-console"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-console",
          "visible": true
        }
      },
      {
        "id": "release:cell-0-upper-stage",
        "label": "release cell-0-upper-stage",
        "requires": [
          "done:close:cell-0-upper-stage"
        ],
        "forbids": [
          "done:release:cell-0-upper-stage"
        ],
        "adds": [
          "done:release:cell-0-upper-stage",
          "repaired:cell-0-upper-stage"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-upper-stage"
        }
      },
      {
        "id": "verify:cell-0-console",
        "label": "verify cell-0-console",
        "requires": [
          "done:replace:cell-0-console"
        ],
        "forbids": [
          "done:verify:cell-0-console"
        ],
        "adds": [
          "done:verify:cell-0-console"
        ],
        "deletes": [
          "fault:cell-0-console"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-console"
        }
      },
      {
        "id": "remove:cell-0-upper-stage",
        "label": "remove cell-0-upper-stage",
        "requires": [
          "done:open:cell-0-upper-stage"
        ],
        "forbids": [
          "done:remove:cell-0-upper-stage"
        ],
        "adds": [
          "done:remove:cell-0-upper-stage"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-upper-stage",
          "visible": false
        }
      },
      {
        "id": "close:cell-0-console",
        "label": "close cell-0-console",
        "requires": [
          "done:verify:cell-0-console"
        ],
        "forbids": [
          "done:close:cell-0-console"
        ],
        "adds": [
          "done:close:cell-0-console"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-console"
        }
      },
      {
        "id": "open:cell-0-upper-stage",
        "label": "open cell-0-upper-stage",
        "requires": [
          "done:support:cell-0-upper-stage"
        ],
        "forbids": [
          "done:open:cell-0-upper-stage"
        ],
        "adds": [
          "done:open:cell-0-upper-stage"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-upper-stage"
        }
      },
      {
        "id": "release:cell-0-console",
        "label": "release cell-0-console",
        "requires": [
          "done:close:cell-0-console"
        ],
        "forbids": [
          "done:release:cell-0-console"
        ],
        "adds": [
          "done:release:cell-0-console",
          "repaired:cell-0-console"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-console"
        }
      },
      {
        "id": "support:cell-0-upper-stage",
        "label": "support cell-0-upper-stage",
        "requires": [
          "fault:cell-0-upper-stage"
        ],
        "forbids": [
          "done:support:cell-0-upper-stage"
        ],
        "adds": [
          "done:support:cell-0-upper-stage"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-upper-stage"
        }
      },
      {
        "id": "open:cell-0-console",
        "label": "open cell-0-console",
        "requires": [
          "done:support:cell-0-console"
        ],
        "forbids": [
          "done:open:cell-0-console"
        ],
        "adds": [
          "done:open:cell-0-console"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-console"
        }
      },
      {
        "id": "support:cell-0-console",
        "label": "support cell-0-console",
        "requires": [
          "fault:cell-0-console"
        ],
        "forbids": [
          "done:support:cell-0-console"
        ],
        "adds": [
          "done:support:cell-0-console"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-console"
        }
      }
    ],
    "goalFacts": [
      "repaired:cell-0-upper-stage",
      "repaired:cell-0-console"
    ],
    "budget": 14,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:cell-0-upper-stage",
      "open:cell-0-upper-stage",
      "remove:cell-0-upper-stage",
      "replace:cell-0-upper-stage",
      "verify:cell-0-upper-stage",
      "close:cell-0-upper-stage",
      "release:cell-0-upper-stage",
      "support:cell-0-console",
      "open:cell-0-console",
      "remove:cell-0-console",
      "replace:cell-0-console",
      "verify:cell-0-console",
      "close:cell-0-console",
      "release:cell-0-console"
    ]
  }
}
```

### 多工位资源调度（h3-exp-d2-turntable-2-scheduling）

为所有工单提交整数 starts，满足先后关系、独占工位及截止时间。

能力：多工位资源调度；形式：schedule；证据：resource-schedule。


```json
{
  "input": {
    "jobs": [
      {
        "id": "job-0",
        "module": "foundation",
        "duration": 1,
        "resource": "test-bench",
        "after": []
      },
      {
        "id": "job-1",
        "module": "cell-0-shuttle",
        "duration": 1,
        "resource": "technician",
        "after": []
      },
      {
        "id": "job-2",
        "module": "cell-0-mount",
        "duration": 3,
        "resource": "test-bench",
        "after": [
          "job-0"
        ]
      },
      {
        "id": "job-3",
        "module": "cell-0-pedestal",
        "duration": 3,
        "resource": "technician",
        "after": [
          "job-1"
        ]
      },
      {
        "id": "job-4",
        "module": "cell-0-rotor",
        "duration": 1,
        "resource": "test-bench",
        "after": [
          "job-2"
        ]
      },
      {
        "id": "job-5",
        "module": "cell-0-offset-load",
        "duration": 1,
        "resource": "technician",
        "after": [
          "job-3"
        ]
      }
    ],
    "deadline": 5
  },
  "answer": {
    "starts": {
      "job-0": 0,
      "job-1": 0,
      "job-2": 1,
      "job-3": 1,
      "job-4": 4,
      "job-5": 4
    }
  }
}
```

### 检查后条件策略（h3-exp-d2-turntable-2-policy）

提交一个检查及 observation→action 决策表，在所有相容世界中采取正确动作。

能力：检查后条件策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "cell-0-offset-load",
    "worlds": [
      {
        "id": "normal",
        "action": "tighten"
      },
      {
        "id": "loose",
        "action": "replace"
      },
      {
        "id": "jammed",
        "action": "continue"
      }
    ],
    "budget": 2,
    "queries": [
      {
        "id": "visual",
        "cost": 1,
        "returns": {
          "normal": "same",
          "loose": "same",
          "jammed": "other"
        }
      },
      {
        "id": "probe",
        "cost": 2,
        "returns": {
          "normal": "signal-0",
          "loose": "signal-1",
          "jammed": "signal-2"
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
    "queryId": "probe",
    "decisions": {
      "signal-0": "tighten",
      "signal-1": "replace",
      "signal-2": "continue"
    }
  }
}
```

### 局部坐标变换（h3-exp-d2-turntable-2-local-frame）

将模块局部点通过给定四元数与平移转换为世界点，保留五位小数。

能力：局部坐标变换；形式：single-choice；证据：model-state。

- A：[2,5,2.6]
- B：[1,4,1.6]
- C：[1,-0.1625,0]
- D：[2,4,0.6]

```json
{
  "input": {
    "localPoint": [
      1,
      -0.16249999999999964,
      1.1102230246251565e-16
    ],
    "rotationXYZW": [
      0,
      0.7071067811865476,
      0,
      -0.7071067811865475
    ],
    "translation": [
      1,
      4.1625,
      0.5999999999999999
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 正交视图投影（h3-exp-d2-turntable-2-projection）

按公开视图坐标约定，选择该世界点投影后的二维坐标。

能力：正交视图投影；形式：single-choice；证据：model-state。

- A：[0,0]
- B：[-4,7]
- C：[7,3]
- D：[3,4]

```json
{
  "input": {
    "view": "side",
    "point": [
      3,
      7,
      -4
    ],
    "convention": "front=(x,y), side=(z,y), top=(x,z)"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 空间相对关系（h3-exp-d2-turntable-2-relative-order）

比较B相对A在指定世界轴上的模块原点坐标。

能力：空间相对关系；形式：single-choice；证据：model-state。

- A：greater
- B：less
- C：equal

```json
{
  "input": {
    "A": {
      "id": "foundation",
      "position": [
        0,
        0.2,
        0
      ]
    },
    "B": {
      "id": "cell-0-console",
      "position": [
        0,
        1.8775000000000002,
        6
      ]
    },
    "axis": "y"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 约束自由度（h3-exp-d2-turntable-2-joint-axis）

仅考虑这一声明约束，不计闭环、马达与限位激活，保留多少相对运动自由度？弹簧仅施力、不消除自由度。

能力：约束自由度；形式：single-choice；证据：model-state。

- A：0
- B：3
- C：6
- D：1

```json
{
  "input": {
    "joint": {
      "id": "cell-0-rotor-joint",
      "name": "cell-0-rotor interface",
      "parent": "cell-0-pedestal",
      "child": "cell-0-rotor",
      "type": "revolute",
      "anchorParent": [
        0,
        1,
        0
      ],
      "anchorChild": [
        0,
        -0.04999999999999982,
        0
      ],
      "axis": [
        0,
        1,
        0
      ],
      "limits": [
        -0.6,
        0.6
      ]
    }
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 维修间隙预算（h3-exp-d2-turntable-2-clearance-margin）

给定理想直槽净宽、工具宽度、单侧安全余量，工具是否满足横向间隙要求？

能力：维修间隙预算；形式：single-choice；证据：model-state。

- A：feasible
- B：blocked

```json
{
  "input": {
    "module": "cell-0-offset-load",
    "aperture": 0.6100000000000001,
    "toolWidth": 0.45,
    "eachSideMargin": 0.05
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 载荷力矩（h3-exp-d2-turntable-2-load-moment）

绕给定原点的载荷力矩r×F是多少？采用右手系，忽略其他力。

能力：载荷力矩；形式：single-choice；证据：model-state。

- A：[0,0,0]
- B：[0,-2,0]
- C：[0,0,-12]
- D：[0,0,12]

```json
{
  "input": {
    "module": "cell-0-offset-load",
    "lever": [
      2,
      2,
      0
    ],
    "force": [
      0,
      -6,
      0
    ],
    "units": "scene-length × force"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 非均匀先验更新（h3-exp-d2-turntable-2-weighted-posterior）

先验权重未归一化，观测只保留normal和jammed，求jammed后验概率。

能力：非均匀先验更新；形式：single-choice；证据：finite-world。

- A：1
- B：0.16666666666666666
- C：0.1111111111111111
- D：0

```json
{
  "input": {
    "module": "cell-0-offset-load",
    "worlds": [
      "normal",
      "jammed",
      "loose"
    ],
    "weights": [
      5,
      1,
      3
    ],
    "compatible": [
      "normal",
      "jammed"
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 风险最小决策（h3-exp-d2-turntable-2-expected-loss）

继续运行期望损失=p×failureLoss，预防维修损失=repairCost，选择损失较低者；并列选继续。

能力：风险最小决策；形式：single-choice；证据：finite-world。

- A：continue
- B：repair

```json
{
  "input": {
    "faultProbability": 0.4,
    "repairCost": 1,
    "failureLoss": 10,
    "module": "cell-0-offset-load"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 轨迹阈值判定（h3-exp-d2-turntable-2-trace-threshold）

实际采样轨迹中是否有位移严格超过给定阈值？只评价采样点。

能力：轨迹阈值判定；形式：single-choice；证据：Rapier。

- A：within
- B：exceeded

```json
{
  "input": {
    "trace": [
      {
        "time": 0.008333333333333333,
        "displacement": 0.0007247338170267352
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.000006794929504394531
      },
      {
        "time": 0.20833333333333334,
        "displacement": 3.209808353861871e-7
      },
      {
        "time": 0.30833333333333335,
        "displacement": 2.6656007498500226e-7
      },
      {
        "time": 0.4083333333333333,
        "displacement": 2.149076029934877e-7
      },
      {
        "time": 0.5083333333333333,
        "displacement": 2.149076029934877e-7
      },
      {
        "time": 0.6083333333333333,
        "displacement": 2.149076029934877e-7
      },
      {
        "time": 0.7083333333333334,
        "displacement": 2.149076029934877e-7
      },
      {
        "time": 0.8083333333333333,
        "displacement": 2.149076029934877e-7
      },
      {
        "time": 0.9083333333333333,
        "displacement": 2.149076029934877e-7
      },
      {
        "time": 1,
        "displacement": 2.149076029934877e-7
      }
    ],
    "threshold": 0.0008696805804320822
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 安全联锁维修（h3-exp-d2-turntable-2-guarded-repair）

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
        "id": "release:cell-0-offset-load",
        "label": "release cell-0-offset-load",
        "requires": [
          "done:relock:cell-0-offset-load"
        ],
        "forbids": [
          "done:release:cell-0-offset-load"
        ],
        "adds": [
          "done:release:cell-0-offset-load",
          "ready:cell-0-offset-load",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-offset-load"
        }
      },
      {
        "id": "relock:cell-0-offset-load",
        "label": "relock cell-0-offset-load",
        "requires": [
          "done:verify:cell-0-offset-load"
        ],
        "forbids": [
          "done:relock:cell-0-offset-load"
        ],
        "adds": [
          "done:relock:cell-0-offset-load"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-offset-load"
        }
      },
      {
        "id": "verify:cell-0-offset-load",
        "label": "verify cell-0-offset-load",
        "requires": [
          "done:replace:cell-0-offset-load"
        ],
        "forbids": [
          "done:verify:cell-0-offset-load"
        ],
        "adds": [
          "done:verify:cell-0-offset-load"
        ],
        "deletes": [
          "fault:cell-0-offset-load",
          "misaligned:cell-0-offset-load"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-offset-load"
        }
      },
      {
        "id": "replace:cell-0-offset-load",
        "label": "replace cell-0-offset-load",
        "requires": [
          "done:unlock:cell-0-offset-load"
        ],
        "forbids": [
          "done:replace:cell-0-offset-load"
        ],
        "adds": [
          "done:replace:cell-0-offset-load"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "cell-0-offset-load"
        }
      },
      {
        "id": "unlock:cell-0-offset-load",
        "label": "unlock cell-0-offset-load",
        "requires": [
          "done:support:cell-0-offset-load"
        ],
        "forbids": [
          "done:unlock:cell-0-offset-load"
        ],
        "adds": [
          "done:unlock:cell-0-offset-load"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-offset-load"
        }
      },
      {
        "id": "support:cell-0-offset-load",
        "label": "support cell-0-offset-load",
        "requires": [
          "done:isolate:cell-0-offset-load"
        ],
        "forbids": [
          "done:support:cell-0-offset-load"
        ],
        "adds": [
          "done:support:cell-0-offset-load"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-offset-load"
        }
      },
      {
        "id": "isolate:cell-0-offset-load",
        "label": "isolate cell-0-offset-load",
        "requires": [
          "tool:free",
          "fault:cell-0-offset-load"
        ],
        "forbids": [
          "done:isolate:cell-0-offset-load"
        ],
        "adds": [
          "done:isolate:cell-0-offset-load"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-offset-load"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:cell-0-offset-load"
    ],
    "initialModules": [
      "foundation",
      "cell-0-shuttle",
      "cell-0-mount",
      "cell-0-pedestal",
      "cell-0-rotor",
      "cell-0-offset-load",
      "cell-0-upper-stage",
      "cell-0-console"
    ],
    "goalFacts": [
      "ready:cell-0-offset-load"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 8
  },
  "answer": {
    "actionIds": [
      "isolate:cell-0-offset-load",
      "support:cell-0-offset-load",
      "unlock:cell-0-offset-load",
      "replace:cell-0-offset-load",
      "verify:cell-0-offset-load",
      "relock:cell-0-offset-load",
      "release:cell-0-offset-load"
    ]
  }
}
```

### 失败状态回退（h3-exp-d2-turntable-2-rollback）

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
        "id": "resume:cell-0-offset-load",
        "label": "resume cell-0-offset-load",
        "requires": [
          "done:verify:cell-0-offset-load"
        ],
        "forbids": [
          "done:resume:cell-0-offset-load"
        ],
        "adds": [
          "done:resume:cell-0-offset-load",
          "ready:cell-0-offset-load",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-offset-load"
        }
      },
      {
        "id": "verify:cell-0-offset-load",
        "label": "verify cell-0-offset-load",
        "requires": [
          "done:align:cell-0-offset-load"
        ],
        "forbids": [
          "done:verify:cell-0-offset-load"
        ],
        "adds": [
          "done:verify:cell-0-offset-load"
        ],
        "deletes": [
          "fault:cell-0-offset-load",
          "misaligned:cell-0-offset-load"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-offset-load"
        }
      },
      {
        "id": "align:cell-0-offset-load",
        "label": "align cell-0-offset-load",
        "requires": [
          "done:undo:cell-0-offset-load"
        ],
        "forbids": [
          "done:align:cell-0-offset-load"
        ],
        "adds": [
          "done:align:cell-0-offset-load"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-offset-load",
          "visible": true
        }
      },
      {
        "id": "undo:cell-0-offset-load",
        "label": "undo cell-0-offset-load",
        "requires": [
          "done:isolate:cell-0-offset-load"
        ],
        "forbids": [
          "done:undo:cell-0-offset-load"
        ],
        "adds": [
          "done:undo:cell-0-offset-load"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-offset-load",
          "visible": false
        }
      },
      {
        "id": "isolate:cell-0-offset-load",
        "label": "isolate cell-0-offset-load",
        "requires": [
          "tool:free",
          "fault:cell-0-offset-load"
        ],
        "forbids": [
          "done:isolate:cell-0-offset-load"
        ],
        "adds": [
          "done:isolate:cell-0-offset-load"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-offset-load"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:cell-0-offset-load",
      "misaligned:cell-0-offset-load"
    ],
    "initialModules": [
      "foundation",
      "cell-0-shuttle",
      "cell-0-mount",
      "cell-0-pedestal",
      "cell-0-rotor",
      "cell-0-offset-load",
      "cell-0-upper-stage",
      "cell-0-console"
    ],
    "goalFacts": [
      "ready:cell-0-offset-load"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 5
  },
  "answer": {
    "actionIds": [
      "isolate:cell-0-offset-load",
      "undo:cell-0-offset-load",
      "align:cell-0-offset-load",
      "verify:cell-0-offset-load",
      "resume:cell-0-offset-load"
    ]
  }
}
```

### 共享工具协同维修（h3-exp-d2-turntable-2-resource-repair）

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
        "id": "release:cell-0-console",
        "label": "release cell-0-console",
        "requires": [
          "done:relock:cell-0-console"
        ],
        "forbids": [
          "done:release:cell-0-console"
        ],
        "adds": [
          "done:release:cell-0-console",
          "ready:cell-0-console",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-console"
        }
      },
      {
        "id": "relock:cell-0-console",
        "label": "relock cell-0-console",
        "requires": [
          "done:verify:cell-0-console"
        ],
        "forbids": [
          "done:relock:cell-0-console"
        ],
        "adds": [
          "done:relock:cell-0-console"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-console"
        }
      },
      {
        "id": "verify:cell-0-console",
        "label": "verify cell-0-console",
        "requires": [
          "done:replace:cell-0-console"
        ],
        "forbids": [
          "done:verify:cell-0-console"
        ],
        "adds": [
          "done:verify:cell-0-console"
        ],
        "deletes": [
          "fault:cell-0-console",
          "misaligned:cell-0-console"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-console"
        }
      },
      {
        "id": "replace:cell-0-console",
        "label": "replace cell-0-console",
        "requires": [
          "done:unlock:cell-0-console"
        ],
        "forbids": [
          "done:replace:cell-0-console"
        ],
        "adds": [
          "done:replace:cell-0-console"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "cell-0-console"
        }
      },
      {
        "id": "unlock:cell-0-console",
        "label": "unlock cell-0-console",
        "requires": [
          "done:support:cell-0-console"
        ],
        "forbids": [
          "done:unlock:cell-0-console"
        ],
        "adds": [
          "done:unlock:cell-0-console"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-console"
        }
      },
      {
        "id": "support:cell-0-console",
        "label": "support cell-0-console",
        "requires": [
          "done:isolate:cell-0-console"
        ],
        "forbids": [
          "done:support:cell-0-console"
        ],
        "adds": [
          "done:support:cell-0-console"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-console"
        }
      },
      {
        "id": "isolate:cell-0-console",
        "label": "isolate cell-0-console",
        "requires": [
          "tool:free",
          "fault:cell-0-console"
        ],
        "forbids": [
          "done:isolate:cell-0-console"
        ],
        "adds": [
          "done:isolate:cell-0-console"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-console"
        }
      },
      {
        "id": "release:cell-0-upper-stage",
        "label": "release cell-0-upper-stage",
        "requires": [
          "done:relock:cell-0-upper-stage"
        ],
        "forbids": [
          "done:release:cell-0-upper-stage"
        ],
        "adds": [
          "done:release:cell-0-upper-stage",
          "ready:cell-0-upper-stage",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-upper-stage"
        }
      },
      {
        "id": "relock:cell-0-upper-stage",
        "label": "relock cell-0-upper-stage",
        "requires": [
          "done:verify:cell-0-upper-stage"
        ],
        "forbids": [
          "done:relock:cell-0-upper-stage"
        ],
        "adds": [
          "done:relock:cell-0-upper-stage"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-upper-stage"
        }
      },
      {
        "id": "verify:cell-0-upper-stage",
        "label": "verify cell-0-upper-stage",
        "requires": [
          "done:replace:cell-0-upper-stage"
        ],
        "forbids": [
          "done:verify:cell-0-upper-stage"
        ],
        "adds": [
          "done:verify:cell-0-upper-stage"
        ],
        "deletes": [
          "fault:cell-0-upper-stage",
          "misaligned:cell-0-upper-stage"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-upper-stage"
        }
      },
      {
        "id": "replace:cell-0-upper-stage",
        "label": "replace cell-0-upper-stage",
        "requires": [
          "done:unlock:cell-0-upper-stage"
        ],
        "forbids": [
          "done:replace:cell-0-upper-stage"
        ],
        "adds": [
          "done:replace:cell-0-upper-stage"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "cell-0-upper-stage"
        }
      },
      {
        "id": "unlock:cell-0-upper-stage",
        "label": "unlock cell-0-upper-stage",
        "requires": [
          "done:support:cell-0-upper-stage"
        ],
        "forbids": [
          "done:unlock:cell-0-upper-stage"
        ],
        "adds": [
          "done:unlock:cell-0-upper-stage"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-upper-stage"
        }
      },
      {
        "id": "support:cell-0-upper-stage",
        "label": "support cell-0-upper-stage",
        "requires": [
          "done:isolate:cell-0-upper-stage"
        ],
        "forbids": [
          "done:support:cell-0-upper-stage"
        ],
        "adds": [
          "done:support:cell-0-upper-stage"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-upper-stage"
        }
      },
      {
        "id": "isolate:cell-0-upper-stage",
        "label": "isolate cell-0-upper-stage",
        "requires": [
          "tool:free",
          "fault:cell-0-upper-stage"
        ],
        "forbids": [
          "done:isolate:cell-0-upper-stage"
        ],
        "adds": [
          "done:isolate:cell-0-upper-stage"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-upper-stage"
        }
      },
      {
        "id": "release:cell-0-offset-load",
        "label": "release cell-0-offset-load",
        "requires": [
          "done:relock:cell-0-offset-load"
        ],
        "forbids": [
          "done:release:cell-0-offset-load"
        ],
        "adds": [
          "done:release:cell-0-offset-load",
          "ready:cell-0-offset-load",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-offset-load"
        }
      },
      {
        "id": "relock:cell-0-offset-load",
        "label": "relock cell-0-offset-load",
        "requires": [
          "done:verify:cell-0-offset-load"
        ],
        "forbids": [
          "done:relock:cell-0-offset-load"
        ],
        "adds": [
          "done:relock:cell-0-offset-load"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-offset-load"
        }
      },
      {
        "id": "verify:cell-0-offset-load",
        "label": "verify cell-0-offset-load",
        "requires": [
          "done:replace:cell-0-offset-load"
        ],
        "forbids": [
          "done:verify:cell-0-offset-load"
        ],
        "adds": [
          "done:verify:cell-0-offset-load"
        ],
        "deletes": [
          "fault:cell-0-offset-load",
          "misaligned:cell-0-offset-load"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-offset-load"
        }
      },
      {
        "id": "replace:cell-0-offset-load",
        "label": "replace cell-0-offset-load",
        "requires": [
          "done:unlock:cell-0-offset-load"
        ],
        "forbids": [
          "done:replace:cell-0-offset-load"
        ],
        "adds": [
          "done:replace:cell-0-offset-load"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "cell-0-offset-load"
        }
      },
      {
        "id": "unlock:cell-0-offset-load",
        "label": "unlock cell-0-offset-load",
        "requires": [
          "done:support:cell-0-offset-load"
        ],
        "forbids": [
          "done:unlock:cell-0-offset-load"
        ],
        "adds": [
          "done:unlock:cell-0-offset-load"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-offset-load"
        }
      },
      {
        "id": "support:cell-0-offset-load",
        "label": "support cell-0-offset-load",
        "requires": [
          "done:isolate:cell-0-offset-load"
        ],
        "forbids": [
          "done:support:cell-0-offset-load"
        ],
        "adds": [
          "done:support:cell-0-offset-load"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-offset-load"
        }
      },
      {
        "id": "isolate:cell-0-offset-load",
        "label": "isolate cell-0-offset-load",
        "requires": [
          "tool:free",
          "fault:cell-0-offset-load"
        ],
        "forbids": [
          "done:isolate:cell-0-offset-load"
        ],
        "adds": [
          "done:isolate:cell-0-offset-load"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-offset-load"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:cell-0-offset-load",
      "fault:cell-0-upper-stage",
      "fault:cell-0-console"
    ],
    "initialModules": [
      "foundation",
      "cell-0-shuttle",
      "cell-0-mount",
      "cell-0-pedestal",
      "cell-0-rotor",
      "cell-0-offset-load",
      "cell-0-upper-stage",
      "cell-0-console"
    ],
    "goalFacts": [
      "ready:cell-0-offset-load",
      "ready:cell-0-upper-stage",
      "ready:cell-0-console"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 24
  },
  "answer": {
    "actionIds": [
      "isolate:cell-0-console",
      "support:cell-0-console",
      "unlock:cell-0-console",
      "replace:cell-0-console",
      "verify:cell-0-console",
      "relock:cell-0-console",
      "release:cell-0-console",
      "isolate:cell-0-upper-stage",
      "support:cell-0-upper-stage",
      "unlock:cell-0-upper-stage",
      "replace:cell-0-upper-stage",
      "verify:cell-0-upper-stage",
      "relock:cell-0-upper-stage",
      "release:cell-0-upper-stage",
      "isolate:cell-0-offset-load",
      "support:cell-0-offset-load",
      "unlock:cell-0-offset-load",
      "replace:cell-0-offset-load",
      "verify:cell-0-offset-load",
      "relock:cell-0-offset-load",
      "release:cell-0-offset-load"
    ]
  }
}
```

### 预算约束检查策略（h3-exp-d2-turntable-2-budget-policy）

提交预算内、对所有相容世界均正确的检查决策表。

能力：预算约束检查策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "cell-0-offset-load",
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
        "cost": 2,
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
        "cost": 3,
        "returns": {
          "nominal": "clear",
          "fault": "alert"
        }
      }
    ],
    "budget": 2
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
