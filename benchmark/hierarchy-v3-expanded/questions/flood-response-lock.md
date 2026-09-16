## D4 洪水应急船闸系统

### 模块识别（h3-flood-response-lock-identify）

高亮的维修模块对应哪个 ID？

能力：模块识别；形式：single-choice；证据：model-state。

- A：gate-south
- B：pump-a
- C：basin
- D：gate-north

```json
{
  "input": {
    "moduleNames": [
      {
        "id": "basin",
        "name": "Flood lock basin"
      },
      {
        "id": "gate-north",
        "name": "North sector gate"
      },
      {
        "id": "gate-south",
        "name": "South sector gate"
      },
      {
        "id": "control-tower",
        "name": "Flood control tower"
      },
      {
        "id": "pump-a",
        "name": "West emergency pump"
      },
      {
        "id": "pump-b",
        "name": "East emergency pump"
      },
      {
        "id": "gantry",
        "name": "Emergency service gantry"
      },
      {
        "id": "gantry-trolley",
        "name": "Gantry maintenance trolley"
      },
      {
        "id": "sensor-north",
        "name": "North level sensor"
      },
      {
        "id": "sensor-south",
        "name": "South level sensor"
      },
      {
        "id": "service-barge",
        "name": "Emergency service barge"
      }
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 部件计数（h3-flood-response-lock-count）

模块 pump-a 有多少个可视零件？

能力：部件计数；形式：single-choice；证据：model-state。

- A：9
- B：10
- C：8
- D：12

```json
{
  "input": {
    "parts": [
      {
        "id": "h0001",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0002",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0003",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0004",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0005",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0006",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0007",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0008",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0009",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0010",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0011",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0012",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0013",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0014",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0015",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0016",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0017",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0018",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0019",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0020",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0021",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0022",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0023",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0024",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0025",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0026",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0027",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0028",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0029",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0030",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0031",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0032",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0033",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0034",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0035",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0036",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0037",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0038",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0039",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0040",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0041",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0042",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0043",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0044",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0045",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0046",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0047",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0048",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0049",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0050",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0051",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0052",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0053",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0054",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0055",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0056",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0057",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0058",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0059",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0060",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0061",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0062",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0063",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0064",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0065",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0066",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0067",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0068",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0069",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0070",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0071",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0072",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0073",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0074",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0075",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0076",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0077",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0078",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0079",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0080",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0081",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0082",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0083",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0084",
        "moduleId": "basin",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0085",
        "moduleId": "gate-north",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0086",
        "moduleId": "gate-north",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0087",
        "moduleId": "gate-north",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0088",
        "moduleId": "gate-north",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0089",
        "moduleId": "gate-north",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0090",
        "moduleId": "gate-north",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0091",
        "moduleId": "gate-north",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0092",
        "moduleId": "gate-north",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0093",
        "moduleId": "gate-north",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0094",
        "moduleId": "gate-north",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0095",
        "moduleId": "gate-north",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0096",
        "moduleId": "gate-north",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0097",
        "moduleId": "gate-north",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0098",
        "moduleId": "gate-north",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0099",
        "moduleId": "gate-north",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0100",
        "moduleId": "gate-north",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0101",
        "moduleId": "gate-north",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0102",
        "moduleId": "gate-north",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0103",
        "moduleId": "gate-south",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0104",
        "moduleId": "gate-south",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0105",
        "moduleId": "gate-south",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0106",
        "moduleId": "gate-south",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0107",
        "moduleId": "gate-south",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0108",
        "moduleId": "gate-south",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0109",
        "moduleId": "gate-south",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0110",
        "moduleId": "gate-south",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0111",
        "moduleId": "gate-south",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0112",
        "moduleId": "gate-south",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0113",
        "moduleId": "gate-south",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0114",
        "moduleId": "gate-south",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0115",
        "moduleId": "gate-south",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0116",
        "moduleId": "gate-south",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0117",
        "moduleId": "gate-south",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0118",
        "moduleId": "gate-south",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0119",
        "moduleId": "gate-south",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0120",
        "moduleId": "gate-south",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0121",
        "moduleId": "control-tower",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "h0122",
        "moduleId": "control-tower",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "h0123",
        "moduleId": "control-tower",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "h0124",
        "moduleId": "control-tower",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "h0125",
        "moduleId": "control-tower",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "h0126",
        "moduleId": "control-tower",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "h0127",
        "moduleId": "control-tower",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "h0128",
        "moduleId": "control-tower",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "h0129",
        "moduleId": "control-tower",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "h0130",
        "moduleId": "control-tower",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "h0131",
        "moduleId": "control-tower",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "h0132",
        "moduleId": "control-tower",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "h0133",
        "moduleId": "control-tower",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "h0134",
        "moduleId": "control-tower",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "h0135",
        "moduleId": "control-tower",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "h0136",
        "moduleId": "control-tower",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "h0137",
        "moduleId": "control-tower",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "h0138",
        "moduleId": "control-tower",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "h0139",
        "moduleId": "control-tower",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "h0140",
        "moduleId": "control-tower",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "h0141",
        "moduleId": "control-tower",
        "shape": "window",
        "color": "#79c7d8"
      },
      {
        "id": "h0142",
        "moduleId": "pump-a",
        "shape": "cylinder",
        "color": "#e8792e"
      },
      {
        "id": "h0143",
        "moduleId": "pump-a",
        "shape": "gear",
        "color": "#26323b"
      },
      {
        "id": "h0144",
        "moduleId": "pump-a",
        "shape": "gear",
        "color": "#26323b"
      },
      {
        "id": "h0145",
        "moduleId": "pump-a",
        "shape": "gear",
        "color": "#26323b"
      },
      {
        "id": "h0146",
        "moduleId": "pump-a",
        "shape": "gear",
        "color": "#26323b"
      },
      {
        "id": "h0147",
        "moduleId": "pump-a",
        "shape": "gear",
        "color": "#26323b"
      },
      {
        "id": "h0148",
        "moduleId": "pump-a",
        "shape": "gear",
        "color": "#26323b"
      },
      {
        "id": "h0149",
        "moduleId": "pump-a",
        "shape": "gear",
        "color": "#26323b"
      },
      {
        "id": "h0150",
        "moduleId": "pump-a",
        "shape": "gear",
        "color": "#26323b"
      },
      {
        "id": "h0151",
        "moduleId": "pump-b",
        "shape": "cylinder",
        "color": "#e8792e"
      },
      {
        "id": "h0152",
        "moduleId": "pump-b",
        "shape": "gear",
        "color": "#26323b"
      },
      {
        "id": "h0153",
        "moduleId": "pump-b",
        "shape": "gear",
        "color": "#26323b"
      },
      {
        "id": "h0154",
        "moduleId": "pump-b",
        "shape": "gear",
        "color": "#26323b"
      },
      {
        "id": "h0155",
        "moduleId": "pump-b",
        "shape": "gear",
        "color": "#26323b"
      },
      {
        "id": "h0156",
        "moduleId": "pump-b",
        "shape": "gear",
        "color": "#26323b"
      },
      {
        "id": "h0157",
        "moduleId": "pump-b",
        "shape": "gear",
        "color": "#26323b"
      },
      {
        "id": "h0158",
        "moduleId": "pump-b",
        "shape": "gear",
        "color": "#26323b"
      },
      {
        "id": "h0159",
        "moduleId": "pump-b",
        "shape": "gear",
        "color": "#26323b"
      },
      {
        "id": "h0160",
        "moduleId": "gantry",
        "shape": "brick",
        "color": "#f2bf3c"
      },
      {
        "id": "h0161",
        "moduleId": "gantry",
        "shape": "brick",
        "color": "#f2bf3c"
      },
      {
        "id": "h0162",
        "moduleId": "gantry",
        "shape": "brick",
        "color": "#f2bf3c"
      },
      {
        "id": "h0163",
        "moduleId": "gantry",
        "shape": "brick",
        "color": "#f2bf3c"
      },
      {
        "id": "h0164",
        "moduleId": "gantry",
        "shape": "brick",
        "color": "#f2bf3c"
      },
      {
        "id": "h0165",
        "moduleId": "gantry",
        "shape": "brick",
        "color": "#f2bf3c"
      },
      {
        "id": "h0166",
        "moduleId": "gantry",
        "shape": "brick",
        "color": "#f2bf3c"
      },
      {
        "id": "h0167",
        "moduleId": "gantry",
        "shape": "brick",
        "color": "#f2bf3c"
      },
      {
        "id": "h0168",
        "moduleId": "gantry",
        "shape": "brick",
        "color": "#f2bf3c"
      },
      {
        "id": "h0169",
        "moduleId": "gantry",
        "shape": "brick",
        "color": "#f2bf3c"
      },
      {
        "id": "h0170",
        "moduleId": "gantry",
        "shape": "brick",
        "color": "#f2bf3c"
      },
      {
        "id": "h0171",
        "moduleId": "gantry",
        "shape": "brick",
        "color": "#f2bf3c"
      },
      {
        "id": "h0172",
        "moduleId": "gantry",
        "shape": "brick",
        "color": "#f2bf3c"
      },
      {
        "id": "h0173",
        "moduleId": "gantry",
        "shape": "brick",
        "color": "#f2bf3c"
      },
      {
        "id": "h0174",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0175",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0176",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0177",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0178",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0179",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0180",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0181",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0182",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0183",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0184",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0185",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0186",
        "moduleId": "gantry-trolley",
        "shape": "plate",
        "color": "#d43a32"
      },
      {
        "id": "h0187",
        "moduleId": "gantry-trolley",
        "shape": "plate",
        "color": "#d43a32"
      },
      {
        "id": "h0188",
        "moduleId": "gantry-trolley",
        "shape": "plate",
        "color": "#d43a32"
      },
      {
        "id": "h0189",
        "moduleId": "gantry-trolley",
        "shape": "plate",
        "color": "#d43a32"
      },
      {
        "id": "h0190",
        "moduleId": "gantry-trolley",
        "shape": "plate",
        "color": "#d43a32"
      },
      {
        "id": "h0191",
        "moduleId": "gantry-trolley",
        "shape": "plate",
        "color": "#d43a32"
      },
      {
        "id": "h0192",
        "moduleId": "sensor-north",
        "shape": "brick",
        "color": "#26323b"
      },
      {
        "id": "h0193",
        "moduleId": "sensor-north",
        "shape": "brick",
        "color": "#26323b"
      },
      {
        "id": "h0194",
        "moduleId": "sensor-north",
        "shape": "brick",
        "color": "#26323b"
      },
      {
        "id": "h0195",
        "moduleId": "sensor-north",
        "shape": "sphere",
        "color": "#79c7d8"
      },
      {
        "id": "h0196",
        "moduleId": "sensor-south",
        "shape": "brick",
        "color": "#26323b"
      },
      {
        "id": "h0197",
        "moduleId": "sensor-south",
        "shape": "brick",
        "color": "#26323b"
      },
      {
        "id": "h0198",
        "moduleId": "sensor-south",
        "shape": "brick",
        "color": "#26323b"
      },
      {
        "id": "h0199",
        "moduleId": "sensor-south",
        "shape": "sphere",
        "color": "#79c7d8"
      },
      {
        "id": "h0200",
        "moduleId": "service-barge",
        "shape": "plate",
        "color": "#3f8a61"
      },
      {
        "id": "h0201",
        "moduleId": "service-barge",
        "shape": "plate",
        "color": "#3f8a61"
      },
      {
        "id": "h0202",
        "moduleId": "service-barge",
        "shape": "plate",
        "color": "#3f8a61"
      },
      {
        "id": "h0203",
        "moduleId": "service-barge",
        "shape": "plate",
        "color": "#3f8a61"
      },
      {
        "id": "h0204",
        "moduleId": "service-barge",
        "shape": "plate",
        "color": "#3f8a61"
      },
      {
        "id": "h0205",
        "moduleId": "service-barge",
        "shape": "plate",
        "color": "#3f8a61"
      },
      {
        "id": "h0206",
        "moduleId": "service-barge",
        "shape": "plate",
        "color": "#3f8a61"
      },
      {
        "id": "h0207",
        "moduleId": "service-barge",
        "shape": "plate",
        "color": "#3f8a61"
      },
      {
        "id": "h0208",
        "moduleId": "service-barge",
        "shape": "plate",
        "color": "#3f8a61"
      },
      {
        "id": "h0209",
        "moduleId": "service-barge",
        "shape": "plate",
        "color": "#3f8a61"
      },
      {
        "id": "h0210",
        "moduleId": "service-barge",
        "shape": "plate",
        "color": "#3f8a61"
      },
      {
        "id": "h0211",
        "moduleId": "service-barge",
        "shape": "plate",
        "color": "#3f8a61"
      },
      {
        "id": "h0212",
        "moduleId": "service-barge",
        "shape": "plate",
        "color": "#3f8a61"
      },
      {
        "id": "h0213",
        "moduleId": "service-barge",
        "shape": "plate",
        "color": "#3f8a61"
      },
      {
        "id": "h0214",
        "moduleId": "service-barge",
        "shape": "plate",
        "color": "#3f8a61"
      }
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 颜色识别（h3-flood-response-lock-color）

零件 h0142 的颜色值是什么？

能力：颜色识别；形式：single-choice；证据：model-state。

- A：#f2bf3c
- B：#e8792e
- C：#2878b8
- D：#d43a32

```json
{
  "input": {
    "part": {
      "id": "h0142",
      "moduleId": "pump-a",
      "shape": "cylinder",
      "size": [
        2.2,
        1.8,
        2.2
      ],
      "position": [
        0,
        -0.23749999999999982,
        0
      ],
      "rotation": [
        0,
        0,
        0,
        1
      ],
      "color": "#e8792e"
    }
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 三维位置（h3-flood-response-lock-position）

模块 pump-a 的世界包围盒中心是什么？

能力：三维位置；形式：single-choice；证据：model-state。

- A：[0.5,0.2,0.5]
- B：[0,1.6,-3]
- C：[0,1.6,3]
- D：[-5.1,1.5874999999999997,2.8]

```json
{
  "input": {
    "centers": {
      "basin": [
        0.5,
        0.2,
        0.5
      ],
      "gate-north": [
        0,
        1.6,
        -3
      ],
      "gate-south": [
        0,
        1.6,
        3
      ],
      "control-tower": [
        -3.5,
        2.9125,
        -3.0749999999999997
      ],
      "pump-a": [
        -5.1,
        1.5874999999999997,
        2.8
      ],
      "pump-b": [
        5.1,
        1.5874999999999997,
        2.8
      ],
      "gantry": [
        0,
        3.4,
        0
      ],
      "gantry-trolley": [
        0,
        6.3999999999999995,
        0
      ],
      "sensor-north": [
        0,
        1.9625,
        -4
      ],
      "sensor-south": [
        0,
        1.9625,
        4
      ],
      "service-barge": [
        0,
        0.6499999999999999,
        0.19999999999999996
      ]
    }
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 关节类型（h3-flood-response-lock-joint-type）

gantry-slide 采用什么约束类型？

能力：关节类型；形式：single-choice；证据：model-state。

- A：spring
- B：prismatic
- C：fixed
- D：revolute

```json
{
  "input": {
    "joint": {
      "id": "gantry-slide",
      "name": "gantry slide",
      "type": "prismatic",
      "parent": "gantry",
      "child": "gantry-trolley",
      "anchorParent": [
        0,
        2.8000000000000003,
        0
      ],
      "anchorChild": [
        0,
        -0.1999999999999993,
        0
      ],
      "axis": [
        1,
        0,
        0
      ],
      "limits": [
        -4,
        4
      ]
    }
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 直接连接（h3-flood-response-lock-parent）

pump-a 的直接父模块集合是什么？

能力：直接连接；形式：single-choice；证据：model-state。

- A：["pump-a"]
- B：[]
- C：["basin","gate-north","gate-south","control-tower","pump-a","pump-b","gantry","gantry-trolley","sensor-north","sensor-south","service-barge"]
- D：["basin"]

```json
{
  "input": {
    "joints": [
      {
        "id": "north-gate-hinge",
        "name": "north gate hinge",
        "type": "revolute",
        "parent": "basin",
        "child": "gate-north",
        "anchorParent": [
          -3.5,
          0.8,
          -3.5
        ],
        "anchorChild": [
          -3,
          -0.6000000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          0,
          1.2
        ]
      },
      {
        "id": "south-gate-hinge",
        "name": "south gate hinge",
        "type": "revolute",
        "parent": "basin",
        "child": "gate-south",
        "anchorParent": [
          2.5,
          0.8,
          2.5
        ],
        "anchorChild": [
          3,
          -0.6000000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -1.2,
          0
        ]
      },
      {
        "id": "tower-foundation",
        "name": "tower foundation",
        "type": "fixed",
        "parent": "basin",
        "child": "control-tower",
        "anchorParent": [
          -4,
          0.3,
          -4
        ],
        "anchorChild": [
          0,
          -2.4125,
          -0.42500000000000027
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "pump-a-lock",
        "name": "pump a lock",
        "type": "fixed",
        "parent": "basin",
        "child": "pump-a",
        "anchorParent": [
          -5.6,
          0.45,
          2.3
        ],
        "anchorChild": [
          0,
          -0.9374999999999998,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "pump-b-lock",
        "name": "pump b lock",
        "type": "fixed",
        "parent": "basin",
        "child": "pump-b",
        "anchorParent": [
          4.6,
          0.45,
          2.3
        ],
        "anchorChild": [
          0,
          -0.9374999999999998,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "gantry-feet",
        "name": "gantry feet",
        "type": "fixed",
        "parent": "basin",
        "child": "gantry",
        "anchorParent": [
          -0.5,
          0.3,
          -0.5
        ],
        "anchorChild": [
          0,
          -2.9,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "gantry-slide",
        "name": "gantry slide",
        "type": "prismatic",
        "parent": "gantry",
        "child": "gantry-trolley",
        "anchorParent": [
          0,
          2.8000000000000003,
          0
        ],
        "anchorChild": [
          0,
          -0.1999999999999993,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -4,
          4
        ]
      },
      {
        "id": "north-sensor-link",
        "name": "north sensor link",
        "type": "fixed",
        "parent": "control-tower",
        "child": "sensor-north",
        "anchorParent": [
          3.5,
          -0.9125000000000001,
          -0.9250000000000003
        ],
        "anchorChild": [
          0,
          0.03750000000000009,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "south-sensor-link",
        "name": "south sensor link",
        "type": "fixed",
        "parent": "control-tower",
        "child": "sensor-south",
        "anchorParent": [
          3.5,
          -0.9125000000000001,
          7.074999999999999
        ],
        "anchorChild": [
          0,
          0.03750000000000009,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "barge-mooring",
        "name": "barge mooring",
        "type": "spring",
        "parent": "basin",
        "child": "service-barge",
        "anchorParent": [
          -0.5,
          0.39999999999999997,
          -0.5
        ],
        "anchorChild": [
          0,
          -0.04999999999999993,
          -0.19999999999999996
        ],
        "axis": [
          0,
          1,
          0
        ],
        "stiffness": 4000,
        "damping": 160
      },
      {
        "id": "barge-mooring-2",
        "name": "Separated elastic mooring",
        "type": "spring",
        "parent": "basin",
        "child": "service-barge",
        "anchorParent": [
          1.5,
          0.39999999999999997,
          -0.5
        ],
        "anchorChild": [
          2,
          -0.04999999999999993,
          -0.19999999999999996
        ],
        "restLength": 0,
        "stiffness": 4000,
        "damping": 160
      },
      {
        "id": "barge-mooring-3",
        "name": "Separated elastic mooring",
        "type": "spring",
        "parent": "basin",
        "child": "service-barge",
        "anchorParent": [
          -2.5,
          0.39999999999999997,
          0.5
        ],
        "anchorChild": [
          -2,
          -0.04999999999999993,
          0.8
        ],
        "restLength": 0,
        "stiffness": 4000,
        "damping": 160
      }
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 基座识别（h3-flood-response-lock-anchor）

哪些模块被声明为固定基座？

能力：基座识别；形式：single-choice；证据：model-state。

- A：["basin"]
- B：[]
- C：["basin","gate-north","gate-south","control-tower","pump-a","pump-b","gantry","gantry-trolley","sensor-north","sensor-south","service-barge"]
- D：["pump-a"]

```json
{
  "input": {
    "modules": [
      {
        "id": "basin",
        "name": "Flood lock basin",
        "role": "foundation",
        "anchored": true,
        "mass": 60,
        "position": [
          0.5,
          0.2,
          0.5
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "gate-north",
        "name": "North sector gate",
        "role": "barrier",
        "anchored": false,
        "mass": 14,
        "position": [
          0,
          1.6,
          -3
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "gate-south",
        "name": "South sector gate",
        "role": "barrier",
        "anchored": false,
        "mass": 14,
        "position": [
          0,
          1.6,
          3
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "control-tower",
        "name": "Flood control tower",
        "role": "control",
        "anchored": false,
        "mass": 12,
        "position": [
          -3.5,
          2.9125,
          -3.0749999999999997
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "pump-a",
        "name": "West emergency pump",
        "role": "service-module",
        "anchored": false,
        "mass": 5,
        "position": [
          -5.1,
          1.5874999999999997,
          2.8
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "pump-b",
        "name": "East emergency pump",
        "role": "service-module",
        "anchored": false,
        "mass": 5,
        "position": [
          5.1,
          1.5874999999999997,
          2.8
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "gantry",
        "name": "Emergency service gantry",
        "role": "support",
        "anchored": false,
        "mass": 10,
        "position": [
          0,
          3.4,
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
        "id": "gantry-trolley",
        "name": "Gantry maintenance trolley",
        "role": "actuator",
        "anchored": false,
        "mass": 3,
        "position": [
          0,
          6.3999999999999995,
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
        "id": "sensor-north",
        "name": "North level sensor",
        "role": "sensor",
        "anchored": false,
        "mass": 1,
        "position": [
          0,
          1.9625,
          -4
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "sensor-south",
        "name": "South level sensor",
        "role": "sensor",
        "anchored": false,
        "mass": 1,
        "position": [
          0,
          1.9625,
          4
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "service-barge",
        "name": "Emergency service barge",
        "role": "payload",
        "anchored": false,
        "mass": 8,
        "position": [
          0,
          0.6499999999999999,
          0.19999999999999996
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
    "choiceId": "A"
  }
}
```

### 接口计数（h3-flood-response-lock-degree）

pump-a 连接几个声明关节？平行关节分别计数。

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
        "id": "north-gate-hinge",
        "name": "north gate hinge",
        "type": "revolute",
        "parent": "basin",
        "child": "gate-north",
        "anchorParent": [
          -3.5,
          0.8,
          -3.5
        ],
        "anchorChild": [
          -3,
          -0.6000000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          0,
          1.2
        ]
      },
      {
        "id": "south-gate-hinge",
        "name": "south gate hinge",
        "type": "revolute",
        "parent": "basin",
        "child": "gate-south",
        "anchorParent": [
          2.5,
          0.8,
          2.5
        ],
        "anchorChild": [
          3,
          -0.6000000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -1.2,
          0
        ]
      },
      {
        "id": "tower-foundation",
        "name": "tower foundation",
        "type": "fixed",
        "parent": "basin",
        "child": "control-tower",
        "anchorParent": [
          -4,
          0.3,
          -4
        ],
        "anchorChild": [
          0,
          -2.4125,
          -0.42500000000000027
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "pump-a-lock",
        "name": "pump a lock",
        "type": "fixed",
        "parent": "basin",
        "child": "pump-a",
        "anchorParent": [
          -5.6,
          0.45,
          2.3
        ],
        "anchorChild": [
          0,
          -0.9374999999999998,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "pump-b-lock",
        "name": "pump b lock",
        "type": "fixed",
        "parent": "basin",
        "child": "pump-b",
        "anchorParent": [
          4.6,
          0.45,
          2.3
        ],
        "anchorChild": [
          0,
          -0.9374999999999998,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "gantry-feet",
        "name": "gantry feet",
        "type": "fixed",
        "parent": "basin",
        "child": "gantry",
        "anchorParent": [
          -0.5,
          0.3,
          -0.5
        ],
        "anchorChild": [
          0,
          -2.9,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "gantry-slide",
        "name": "gantry slide",
        "type": "prismatic",
        "parent": "gantry",
        "child": "gantry-trolley",
        "anchorParent": [
          0,
          2.8000000000000003,
          0
        ],
        "anchorChild": [
          0,
          -0.1999999999999993,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -4,
          4
        ]
      },
      {
        "id": "north-sensor-link",
        "name": "north sensor link",
        "type": "fixed",
        "parent": "control-tower",
        "child": "sensor-north",
        "anchorParent": [
          3.5,
          -0.9125000000000001,
          -0.9250000000000003
        ],
        "anchorChild": [
          0,
          0.03750000000000009,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "south-sensor-link",
        "name": "south sensor link",
        "type": "fixed",
        "parent": "control-tower",
        "child": "sensor-south",
        "anchorParent": [
          3.5,
          -0.9125000000000001,
          7.074999999999999
        ],
        "anchorChild": [
          0,
          0.03750000000000009,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "barge-mooring",
        "name": "barge mooring",
        "type": "spring",
        "parent": "basin",
        "child": "service-barge",
        "anchorParent": [
          -0.5,
          0.39999999999999997,
          -0.5
        ],
        "anchorChild": [
          0,
          -0.04999999999999993,
          -0.19999999999999996
        ],
        "axis": [
          0,
          1,
          0
        ],
        "stiffness": 4000,
        "damping": 160
      },
      {
        "id": "barge-mooring-2",
        "name": "Separated elastic mooring",
        "type": "spring",
        "parent": "basin",
        "child": "service-barge",
        "anchorParent": [
          1.5,
          0.39999999999999997,
          -0.5
        ],
        "anchorChild": [
          2,
          -0.04999999999999993,
          -0.19999999999999996
        ],
        "restLength": 0,
        "stiffness": 4000,
        "damping": 160
      },
      {
        "id": "barge-mooring-3",
        "name": "Separated elastic mooring",
        "type": "spring",
        "parent": "basin",
        "child": "service-barge",
        "anchorParent": [
          -2.5,
          0.39999999999999997,
          0.5
        ],
        "anchorChild": [
          -2,
          -0.04999999999999993,
          0.8
        ],
        "restLength": 0,
        "stiffness": 4000,
        "damping": 160
      }
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 局部改色（h3-flood-response-lock-recolor）

仅将 h0142 改成 #e8792e，其他零件不变。选择正确补丁。

能力：局部改色；形式：single-choice；证据：model-state。

- A：{"id":"*","color":"#e8792e"}
- B：{"id":"h0142","color":"#e8792e"}
- C：{"id":"h0143","color":"#e8792e"}
- D：{"id":"h0142","color":"#2878b8"}

```json
{
  "input": {
    "part": {
      "id": "h0142",
      "moduleId": "pump-a",
      "shape": "cylinder",
      "size": [
        2.2,
        1.8,
        2.2
      ],
      "position": [
        0,
        -0.23749999999999982,
        0
      ],
      "rotation": [
        0,
        0,
        0,
        1
      ],
      "color": "#e8792e"
    }
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 补装部件（h3-flood-response-lock-add）

模块 pump-a 缺失零件 h0142。选择与目标清单一致的补装描述。

能力：补装部件；形式：single-choice；证据：model-state。

- A：{"id":"h0142","moduleId":"pump-a","shape":"cylinder","size":[2.2,1.8,2.2],"position":[0,-0.23749999999999982,0],"rotation":[0,0,0,1],"color":"#000000"}
- B：{"id":"h0142","moduleId":"pump-a","shape":"cylinder","size":[2.2,1.8,2.2],"position":[0,-0.23749999999999982,0],"rotation":[0,0,0,1],"color":"#e8792e"}
- C：{"id":"h0142","moduleId":"basin","shape":"cylinder","size":[2.2,1.8,2.2],"position":[0,-0.23749999999999982,0],"rotation":[0,0,0,1],"color":"#e8792e"}
- D：{"id":"h0142","moduleId":"pump-a","shape":"cylinder","size":[3,3,3],"position":[0,-0.23749999999999982,0],"rotation":[0,0,0,1],"color":"#e8792e"}

```json
{
  "input": {
    "targetPart": {
      "id": "h0142",
      "moduleId": "pump-a",
      "shape": "cylinder",
      "size": [
        2.2,
        1.8,
        2.2
      ],
      "position": [
        0,
        -0.23749999999999982,
        0
      ],
      "rotation": [
        0,
        0,
        0,
        1
      ],
      "color": "#e8792e"
    },
    "existingIds": [
      "h0001",
      "h0002",
      "h0003",
      "h0004",
      "h0005",
      "h0006",
      "h0007",
      "h0008",
      "h0009",
      "h0010",
      "h0011",
      "h0012",
      "h0013",
      "h0014",
      "h0015",
      "h0016",
      "h0017",
      "h0018",
      "h0019",
      "h0020",
      "h0021",
      "h0022",
      "h0023",
      "h0024",
      "h0025",
      "h0026",
      "h0027",
      "h0028",
      "h0029",
      "h0030",
      "h0031",
      "h0032",
      "h0033",
      "h0034",
      "h0035",
      "h0036",
      "h0037",
      "h0038",
      "h0039",
      "h0040",
      "h0041",
      "h0042",
      "h0043",
      "h0044",
      "h0045",
      "h0046",
      "h0047",
      "h0048",
      "h0049",
      "h0050",
      "h0051",
      "h0052",
      "h0053",
      "h0054",
      "h0055",
      "h0056",
      "h0057",
      "h0058",
      "h0059",
      "h0060",
      "h0061",
      "h0062",
      "h0063",
      "h0064",
      "h0065",
      "h0066",
      "h0067",
      "h0068",
      "h0069",
      "h0070",
      "h0071",
      "h0072",
      "h0073",
      "h0074",
      "h0075",
      "h0076",
      "h0077",
      "h0078",
      "h0079",
      "h0080",
      "h0081",
      "h0082",
      "h0083",
      "h0084",
      "h0085",
      "h0086",
      "h0087",
      "h0088",
      "h0089",
      "h0090",
      "h0091",
      "h0092",
      "h0093",
      "h0094",
      "h0095",
      "h0096",
      "h0097",
      "h0098",
      "h0099",
      "h0100",
      "h0101",
      "h0102",
      "h0103",
      "h0104",
      "h0105",
      "h0106",
      "h0107",
      "h0108",
      "h0109",
      "h0110",
      "h0111",
      "h0112",
      "h0113",
      "h0114",
      "h0115",
      "h0116",
      "h0117",
      "h0118",
      "h0119",
      "h0120",
      "h0121",
      "h0122",
      "h0123",
      "h0124",
      "h0125",
      "h0126",
      "h0127",
      "h0128",
      "h0129",
      "h0130",
      "h0131",
      "h0132",
      "h0133",
      "h0134",
      "h0135",
      "h0136",
      "h0137",
      "h0138",
      "h0139",
      "h0140",
      "h0141",
      "h0143",
      "h0144",
      "h0145",
      "h0146",
      "h0147",
      "h0148",
      "h0149",
      "h0150",
      "h0151",
      "h0152",
      "h0153",
      "h0154",
      "h0155",
      "h0156",
      "h0157",
      "h0158",
      "h0159",
      "h0160",
      "h0161",
      "h0162",
      "h0163",
      "h0164",
      "h0165",
      "h0166",
      "h0167",
      "h0168",
      "h0169",
      "h0170",
      "h0171",
      "h0172",
      "h0173",
      "h0174",
      "h0175",
      "h0176",
      "h0177",
      "h0178",
      "h0179",
      "h0180",
      "h0181",
      "h0182",
      "h0183",
      "h0184",
      "h0185",
      "h0186",
      "h0187",
      "h0188",
      "h0189",
      "h0190",
      "h0191",
      "h0192",
      "h0193",
      "h0194",
      "h0195",
      "h0196",
      "h0197",
      "h0198",
      "h0199",
      "h0200",
      "h0201",
      "h0202",
      "h0203",
      "h0204",
      "h0205",
      "h0206",
      "h0207",
      "h0208",
      "h0209",
      "h0210",
      "h0211",
      "h0212",
      "h0213",
      "h0214"
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 安全拆除（h3-flood-response-lock-remove）

按声明依赖图，当前可以先拆哪些叶模块？

能力：安全拆除；形式：single-choice；证据：model-state。

- A：["gantry-trolley","gate-north","gate-south","pump-a","pump-b","sensor-north","sensor-south","service-barge"]
- B：["basin"]
- C：[]
- D：["basin","gate-north","gate-south","control-tower","pump-a","pump-b","gantry","gantry-trolley","sensor-north","sensor-south","service-barge"]

```json
{
  "input": {
    "joints": [
      {
        "id": "north-gate-hinge",
        "name": "north gate hinge",
        "type": "revolute",
        "parent": "basin",
        "child": "gate-north",
        "anchorParent": [
          -3.5,
          0.8,
          -3.5
        ],
        "anchorChild": [
          -3,
          -0.6000000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          0,
          1.2
        ]
      },
      {
        "id": "south-gate-hinge",
        "name": "south gate hinge",
        "type": "revolute",
        "parent": "basin",
        "child": "gate-south",
        "anchorParent": [
          2.5,
          0.8,
          2.5
        ],
        "anchorChild": [
          3,
          -0.6000000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -1.2,
          0
        ]
      },
      {
        "id": "tower-foundation",
        "name": "tower foundation",
        "type": "fixed",
        "parent": "basin",
        "child": "control-tower",
        "anchorParent": [
          -4,
          0.3,
          -4
        ],
        "anchorChild": [
          0,
          -2.4125,
          -0.42500000000000027
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "pump-a-lock",
        "name": "pump a lock",
        "type": "fixed",
        "parent": "basin",
        "child": "pump-a",
        "anchorParent": [
          -5.6,
          0.45,
          2.3
        ],
        "anchorChild": [
          0,
          -0.9374999999999998,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "pump-b-lock",
        "name": "pump b lock",
        "type": "fixed",
        "parent": "basin",
        "child": "pump-b",
        "anchorParent": [
          4.6,
          0.45,
          2.3
        ],
        "anchorChild": [
          0,
          -0.9374999999999998,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "gantry-feet",
        "name": "gantry feet",
        "type": "fixed",
        "parent": "basin",
        "child": "gantry",
        "anchorParent": [
          -0.5,
          0.3,
          -0.5
        ],
        "anchorChild": [
          0,
          -2.9,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "gantry-slide",
        "name": "gantry slide",
        "type": "prismatic",
        "parent": "gantry",
        "child": "gantry-trolley",
        "anchorParent": [
          0,
          2.8000000000000003,
          0
        ],
        "anchorChild": [
          0,
          -0.1999999999999993,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -4,
          4
        ]
      },
      {
        "id": "north-sensor-link",
        "name": "north sensor link",
        "type": "fixed",
        "parent": "control-tower",
        "child": "sensor-north",
        "anchorParent": [
          3.5,
          -0.9125000000000001,
          -0.9250000000000003
        ],
        "anchorChild": [
          0,
          0.03750000000000009,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "south-sensor-link",
        "name": "south sensor link",
        "type": "fixed",
        "parent": "control-tower",
        "child": "sensor-south",
        "anchorParent": [
          3.5,
          -0.9125000000000001,
          7.074999999999999
        ],
        "anchorChild": [
          0,
          0.03750000000000009,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "barge-mooring",
        "name": "barge mooring",
        "type": "spring",
        "parent": "basin",
        "child": "service-barge",
        "anchorParent": [
          -0.5,
          0.39999999999999997,
          -0.5
        ],
        "anchorChild": [
          0,
          -0.04999999999999993,
          -0.19999999999999996
        ],
        "axis": [
          0,
          1,
          0
        ],
        "stiffness": 4000,
        "damping": 160
      },
      {
        "id": "barge-mooring-2",
        "name": "Separated elastic mooring",
        "type": "spring",
        "parent": "basin",
        "child": "service-barge",
        "anchorParent": [
          1.5,
          0.39999999999999997,
          -0.5
        ],
        "anchorChild": [
          2,
          -0.04999999999999993,
          -0.19999999999999996
        ],
        "restLength": 0,
        "stiffness": 4000,
        "damping": 160
      },
      {
        "id": "barge-mooring-3",
        "name": "Separated elastic mooring",
        "type": "spring",
        "parent": "basin",
        "child": "service-barge",
        "anchorParent": [
          -2.5,
          0.39999999999999997,
          0.5
        ],
        "anchorChild": [
          -2,
          -0.04999999999999993,
          0.8
        ],
        "restLength": 0,
        "stiffness": 4000,
        "damping": 160
      }
    ],
    "modules": [
      "basin",
      "gate-north",
      "gate-south",
      "control-tower",
      "pump-a",
      "pump-b",
      "gantry",
      "gantry-trolley",
      "sensor-north",
      "sensor-south",
      "service-barge"
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 替换选择（h3-flood-response-lock-replace）

在成本上限内选择刚度最大的替换件；并列选成本低者，再并列选ID字典序最小者。

能力：替换选择；形式：single-choice；证据：model-state。

- A：stock-2
- B：stock-3
- C：stock-0
- D：stock-1

```json
{
  "input": {
    "alternatives": [
      {
        "id": "stock-0",
        "cost": 7,
        "stiffness": 9,
        "mass": 0.9
      },
      {
        "id": "stock-1",
        "cost": 8,
        "stiffness": 9,
        "mass": 1.5
      },
      {
        "id": "stock-2",
        "cost": 7,
        "stiffness": 4,
        "mass": 1.4
      },
      {
        "id": "stock-3",
        "cost": 5,
        "stiffness": 9,
        "mass": 0.5
      }
    ],
    "maxCost": 6
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 平移纠偏（h3-flood-response-lock-translate）

观察到相对目标的平移误差 delta，选择补偿平移。

能力：平移纠偏；形式：single-choice；证据：model-state。

- A：[4,0,-2]
- B：[0,0,0]
- C：[0,2,0]
- D：[-4,0,2]

```json
{
  "input": {
    "delta": [
      4,
      0,
      -2
    ],
    "target": "pump-a"
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 姿态纠偏（h3-flood-response-lock-rotate）

选择从当前yaw到目标yaw的最短有符号旋转；恰好180°时使用-180°。

能力：姿态纠偏；形式：single-choice；证据：model-state。

- A：-180
- B：0
- C：90
- D：-90

```json
{
  "input": {
    "module": "pump-a",
    "currentYaw": 225,
    "targetYaw": 225
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 下一步放置（h3-flood-response-lock-next-module）

已完成给定前缀，选择所有前置依赖已满足的下一模块集合。

能力：下一步放置；形式：single-choice；证据：model-state。

- A：["basin","control-tower","gantry","gantry-trolley","pump-a","pump-b"]
- B：["basin"]
- C：["gate-north","gate-south","sensor-north","sensor-south","service-barge"]
- D：[]

```json
{
  "input": {
    "prefix": [
      "basin",
      "control-tower",
      "gantry",
      "gantry-trolley",
      "pump-a",
      "pump-b"
    ],
    "joints": [
      {
        "id": "north-gate-hinge",
        "name": "north gate hinge",
        "type": "revolute",
        "parent": "basin",
        "child": "gate-north",
        "anchorParent": [
          -3.5,
          0.8,
          -3.5
        ],
        "anchorChild": [
          -3,
          -0.6000000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          0,
          1.2
        ]
      },
      {
        "id": "south-gate-hinge",
        "name": "south gate hinge",
        "type": "revolute",
        "parent": "basin",
        "child": "gate-south",
        "anchorParent": [
          2.5,
          0.8,
          2.5
        ],
        "anchorChild": [
          3,
          -0.6000000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -1.2,
          0
        ]
      },
      {
        "id": "tower-foundation",
        "name": "tower foundation",
        "type": "fixed",
        "parent": "basin",
        "child": "control-tower",
        "anchorParent": [
          -4,
          0.3,
          -4
        ],
        "anchorChild": [
          0,
          -2.4125,
          -0.42500000000000027
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "pump-a-lock",
        "name": "pump a lock",
        "type": "fixed",
        "parent": "basin",
        "child": "pump-a",
        "anchorParent": [
          -5.6,
          0.45,
          2.3
        ],
        "anchorChild": [
          0,
          -0.9374999999999998,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "pump-b-lock",
        "name": "pump b lock",
        "type": "fixed",
        "parent": "basin",
        "child": "pump-b",
        "anchorParent": [
          4.6,
          0.45,
          2.3
        ],
        "anchorChild": [
          0,
          -0.9374999999999998,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "gantry-feet",
        "name": "gantry feet",
        "type": "fixed",
        "parent": "basin",
        "child": "gantry",
        "anchorParent": [
          -0.5,
          0.3,
          -0.5
        ],
        "anchorChild": [
          0,
          -2.9,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "gantry-slide",
        "name": "gantry slide",
        "type": "prismatic",
        "parent": "gantry",
        "child": "gantry-trolley",
        "anchorParent": [
          0,
          2.8000000000000003,
          0
        ],
        "anchorChild": [
          0,
          -0.1999999999999993,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -4,
          4
        ]
      },
      {
        "id": "north-sensor-link",
        "name": "north sensor link",
        "type": "fixed",
        "parent": "control-tower",
        "child": "sensor-north",
        "anchorParent": [
          3.5,
          -0.9125000000000001,
          -0.9250000000000003
        ],
        "anchorChild": [
          0,
          0.03750000000000009,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "south-sensor-link",
        "name": "south sensor link",
        "type": "fixed",
        "parent": "control-tower",
        "child": "sensor-south",
        "anchorParent": [
          3.5,
          -0.9125000000000001,
          7.074999999999999
        ],
        "anchorChild": [
          0,
          0.03750000000000009,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "barge-mooring",
        "name": "barge mooring",
        "type": "spring",
        "parent": "basin",
        "child": "service-barge",
        "anchorParent": [
          -0.5,
          0.39999999999999997,
          -0.5
        ],
        "anchorChild": [
          0,
          -0.04999999999999993,
          -0.19999999999999996
        ],
        "axis": [
          0,
          1,
          0
        ],
        "stiffness": 4000,
        "damping": 160
      },
      {
        "id": "barge-mooring-2",
        "name": "Separated elastic mooring",
        "type": "spring",
        "parent": "basin",
        "child": "service-barge",
        "anchorParent": [
          1.5,
          0.39999999999999997,
          -0.5
        ],
        "anchorChild": [
          2,
          -0.04999999999999993,
          -0.19999999999999996
        ],
        "restLength": 0,
        "stiffness": 4000,
        "damping": 160
      },
      {
        "id": "barge-mooring-3",
        "name": "Separated elastic mooring",
        "type": "spring",
        "parent": "basin",
        "child": "service-barge",
        "anchorParent": [
          -2.5,
          0.39999999999999997,
          0.5
        ],
        "anchorChild": [
          -2,
          -0.04999999999999993,
          0.8
        ],
        "restLength": 0,
        "stiffness": 4000,
        "damping": 160
      }
    ],
    "modules": [
      "basin",
      "gate-north",
      "gate-south",
      "control-tower",
      "pump-a",
      "pump-b",
      "gantry",
      "gantry-trolley",
      "sensor-north",
      "sensor-south",
      "service-barge"
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 库存核算（h3-flood-response-lock-inventory）

备件库有 9 件，替换模块需 9 件，还剩多少？

能力：库存核算；形式：single-choice；证据：model-state。

- A：1
- B：3
- C：0

```json
{
  "input": {
    "available": 9,
    "required": 9
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 子装配边界（h3-flood-response-lock-boundary）

隔离 pump-a 需要断开哪些边界关节？

能力：子装配边界；形式：single-choice；证据：model-state。

- A：[]
- B：["north-gate-hinge","south-gate-hinge","tower-foundation","pump-a-lock","pump-b-lock","gantry-feet","gantry-slide","north-sensor-link","south-sensor-link","barge-mooring","barge-mooring-2","barge-mooring-3"]
- C：["gantry-slide"]
- D：["pump-a-lock"]

```json
{
  "input": {
    "joints": [
      {
        "id": "north-gate-hinge",
        "name": "north gate hinge",
        "type": "revolute",
        "parent": "basin",
        "child": "gate-north",
        "anchorParent": [
          -3.5,
          0.8,
          -3.5
        ],
        "anchorChild": [
          -3,
          -0.6000000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          0,
          1.2
        ]
      },
      {
        "id": "south-gate-hinge",
        "name": "south gate hinge",
        "type": "revolute",
        "parent": "basin",
        "child": "gate-south",
        "anchorParent": [
          2.5,
          0.8,
          2.5
        ],
        "anchorChild": [
          3,
          -0.6000000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -1.2,
          0
        ]
      },
      {
        "id": "tower-foundation",
        "name": "tower foundation",
        "type": "fixed",
        "parent": "basin",
        "child": "control-tower",
        "anchorParent": [
          -4,
          0.3,
          -4
        ],
        "anchorChild": [
          0,
          -2.4125,
          -0.42500000000000027
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "pump-a-lock",
        "name": "pump a lock",
        "type": "fixed",
        "parent": "basin",
        "child": "pump-a",
        "anchorParent": [
          -5.6,
          0.45,
          2.3
        ],
        "anchorChild": [
          0,
          -0.9374999999999998,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "pump-b-lock",
        "name": "pump b lock",
        "type": "fixed",
        "parent": "basin",
        "child": "pump-b",
        "anchorParent": [
          4.6,
          0.45,
          2.3
        ],
        "anchorChild": [
          0,
          -0.9374999999999998,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "gantry-feet",
        "name": "gantry feet",
        "type": "fixed",
        "parent": "basin",
        "child": "gantry",
        "anchorParent": [
          -0.5,
          0.3,
          -0.5
        ],
        "anchorChild": [
          0,
          -2.9,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "gantry-slide",
        "name": "gantry slide",
        "type": "prismatic",
        "parent": "gantry",
        "child": "gantry-trolley",
        "anchorParent": [
          0,
          2.8000000000000003,
          0
        ],
        "anchorChild": [
          0,
          -0.1999999999999993,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -4,
          4
        ]
      },
      {
        "id": "north-sensor-link",
        "name": "north sensor link",
        "type": "fixed",
        "parent": "control-tower",
        "child": "sensor-north",
        "anchorParent": [
          3.5,
          -0.9125000000000001,
          -0.9250000000000003
        ],
        "anchorChild": [
          0,
          0.03750000000000009,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "south-sensor-link",
        "name": "south sensor link",
        "type": "fixed",
        "parent": "control-tower",
        "child": "sensor-south",
        "anchorParent": [
          3.5,
          -0.9125000000000001,
          7.074999999999999
        ],
        "anchorChild": [
          0,
          0.03750000000000009,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "barge-mooring",
        "name": "barge mooring",
        "type": "spring",
        "parent": "basin",
        "child": "service-barge",
        "anchorParent": [
          -0.5,
          0.39999999999999997,
          -0.5
        ],
        "anchorChild": [
          0,
          -0.04999999999999993,
          -0.19999999999999996
        ],
        "axis": [
          0,
          1,
          0
        ],
        "stiffness": 4000,
        "damping": 160
      },
      {
        "id": "barge-mooring-2",
        "name": "Separated elastic mooring",
        "type": "spring",
        "parent": "basin",
        "child": "service-barge",
        "anchorParent": [
          1.5,
          0.39999999999999997,
          -0.5
        ],
        "anchorChild": [
          2,
          -0.04999999999999993,
          -0.19999999999999996
        ],
        "restLength": 0,
        "stiffness": 4000,
        "damping": 160
      },
      {
        "id": "barge-mooring-3",
        "name": "Separated elastic mooring",
        "type": "spring",
        "parent": "basin",
        "child": "service-barge",
        "anchorParent": [
          -2.5,
          0.39999999999999997,
          0.5
        ],
        "anchorChild": [
          -2,
          -0.04999999999999993,
          0.8
        ],
        "restLength": 0,
        "stiffness": 4000,
        "damping": 160
      }
    ],
    "target": "pump-a"
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 最小干预（h3-flood-response-lock-no-op）

当前模块颜色已满足指令，且无需改变位姿。最少需要几次编辑？

能力：最小干预；形式：single-choice；证据：model-state。

- A：9
- B：0
- C：1
- D：2

```json
{
  "input": {
    "module": "pump-a"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 全过程依赖（h3-flood-response-lock-prefix）

给定候选顺序，首次违反前置依赖的步骤是？从 0 编号，-1 表示没有违反。

能力：全过程依赖；形式：single-choice；证据：support-graph。

- A：0
- B：-1
- C：1
- D：10

```json
{
  "input": {
    "order": [
      "gantry",
      "basin",
      "control-tower",
      "gantry-trolley",
      "pump-a",
      "pump-b",
      "sensor-north",
      "sensor-south",
      "gate-north",
      "gate-south",
      "service-barge"
    ],
    "joints": [
      {
        "id": "north-gate-hinge",
        "name": "north gate hinge",
        "type": "revolute",
        "parent": "basin",
        "child": "gate-north",
        "anchorParent": [
          -3.5,
          0.8,
          -3.5
        ],
        "anchorChild": [
          -3,
          -0.6000000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          0,
          1.2
        ]
      },
      {
        "id": "south-gate-hinge",
        "name": "south gate hinge",
        "type": "revolute",
        "parent": "basin",
        "child": "gate-south",
        "anchorParent": [
          2.5,
          0.8,
          2.5
        ],
        "anchorChild": [
          3,
          -0.6000000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -1.2,
          0
        ]
      },
      {
        "id": "tower-foundation",
        "name": "tower foundation",
        "type": "fixed",
        "parent": "basin",
        "child": "control-tower",
        "anchorParent": [
          -4,
          0.3,
          -4
        ],
        "anchorChild": [
          0,
          -2.4125,
          -0.42500000000000027
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "pump-a-lock",
        "name": "pump a lock",
        "type": "fixed",
        "parent": "basin",
        "child": "pump-a",
        "anchorParent": [
          -5.6,
          0.45,
          2.3
        ],
        "anchorChild": [
          0,
          -0.9374999999999998,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "pump-b-lock",
        "name": "pump b lock",
        "type": "fixed",
        "parent": "basin",
        "child": "pump-b",
        "anchorParent": [
          4.6,
          0.45,
          2.3
        ],
        "anchorChild": [
          0,
          -0.9374999999999998,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "gantry-feet",
        "name": "gantry feet",
        "type": "fixed",
        "parent": "basin",
        "child": "gantry",
        "anchorParent": [
          -0.5,
          0.3,
          -0.5
        ],
        "anchorChild": [
          0,
          -2.9,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "gantry-slide",
        "name": "gantry slide",
        "type": "prismatic",
        "parent": "gantry",
        "child": "gantry-trolley",
        "anchorParent": [
          0,
          2.8000000000000003,
          0
        ],
        "anchorChild": [
          0,
          -0.1999999999999993,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -4,
          4
        ]
      },
      {
        "id": "north-sensor-link",
        "name": "north sensor link",
        "type": "fixed",
        "parent": "control-tower",
        "child": "sensor-north",
        "anchorParent": [
          3.5,
          -0.9125000000000001,
          -0.9250000000000003
        ],
        "anchorChild": [
          0,
          0.03750000000000009,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "south-sensor-link",
        "name": "south sensor link",
        "type": "fixed",
        "parent": "control-tower",
        "child": "sensor-south",
        "anchorParent": [
          3.5,
          -0.9125000000000001,
          7.074999999999999
        ],
        "anchorChild": [
          0,
          0.03750000000000009,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "barge-mooring",
        "name": "barge mooring",
        "type": "spring",
        "parent": "basin",
        "child": "service-barge",
        "anchorParent": [
          -0.5,
          0.39999999999999997,
          -0.5
        ],
        "anchorChild": [
          0,
          -0.04999999999999993,
          -0.19999999999999996
        ],
        "axis": [
          0,
          1,
          0
        ],
        "stiffness": 4000,
        "damping": 160
      },
      {
        "id": "barge-mooring-2",
        "name": "Separated elastic mooring",
        "type": "spring",
        "parent": "basin",
        "child": "service-barge",
        "anchorParent": [
          1.5,
          0.39999999999999997,
          -0.5
        ],
        "anchorChild": [
          2,
          -0.04999999999999993,
          -0.19999999999999996
        ],
        "restLength": 0,
        "stiffness": 4000,
        "damping": 160
      },
      {
        "id": "barge-mooring-3",
        "name": "Separated elastic mooring",
        "type": "spring",
        "parent": "basin",
        "child": "service-barge",
        "anchorParent": [
          -2.5,
          0.39999999999999997,
          0.5
        ],
        "anchorChild": [
          -2,
          -0.04999999999999993,
          0.8
        ],
        "restLength": 0,
        "stiffness": 4000,
        "damping": 160
      }
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 连续维修路径（h3-flood-response-lock-access）

根据实际 Rapier shape cast 记录，选择全部无碰撞路径。

能力：连续维修路径；形式：multiple-choice；证据：Rapier。

- A：path-0
- B：path-1
- C：path-2

```json
{
  "input": {
    "paths": [
      {
        "id": "path-0",
        "start": [
          10.96,
          1.5874999999999997,
          2.8
        ],
        "end": [
          -5.1,
          1.5874999999999997,
          2.8
        ],
        "halfExtents": [
          0.18,
          0.18,
          0.18
        ],
        "clear": false,
        "timeOfImpact": 0.28518059849739075
      },
      {
        "id": "path-1",
        "start": [
          -5.1,
          10.575,
          2.8
        ],
        "end": [
          -5.1,
          1.5874999999999997,
          2.8
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
          -5.1,
          1.5874999999999997,
          10.46
        ],
        "end": [
          -5.1,
          1.5874999999999997,
          2.8
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

### 支撑反事实（h3-flood-response-lock-counterfactual）

移除指定模块后，哪些其余模块失去到任一基座的关节路径？不包含被移除模块本身。

能力：支撑反事实；形式：single-choice；证据：support-graph。

- A：[]
- B：["basin","gate-north","gate-south","control-tower","pump-a","pump-b","gantry","gantry-trolley","sensor-north","sensor-south","service-barge"]
- C：["sensor-north","sensor-south"]
- D：["control-tower"]

```json
{
  "input": {
    "removed": "control-tower",
    "roots": [
      "basin"
    ],
    "joints": [
      {
        "id": "north-gate-hinge",
        "name": "north gate hinge",
        "type": "revolute",
        "parent": "basin",
        "child": "gate-north",
        "anchorParent": [
          -3.5,
          0.8,
          -3.5
        ],
        "anchorChild": [
          -3,
          -0.6000000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          0,
          1.2
        ]
      },
      {
        "id": "south-gate-hinge",
        "name": "south gate hinge",
        "type": "revolute",
        "parent": "basin",
        "child": "gate-south",
        "anchorParent": [
          2.5,
          0.8,
          2.5
        ],
        "anchorChild": [
          3,
          -0.6000000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -1.2,
          0
        ]
      },
      {
        "id": "tower-foundation",
        "name": "tower foundation",
        "type": "fixed",
        "parent": "basin",
        "child": "control-tower",
        "anchorParent": [
          -4,
          0.3,
          -4
        ],
        "anchorChild": [
          0,
          -2.4125,
          -0.42500000000000027
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "pump-a-lock",
        "name": "pump a lock",
        "type": "fixed",
        "parent": "basin",
        "child": "pump-a",
        "anchorParent": [
          -5.6,
          0.45,
          2.3
        ],
        "anchorChild": [
          0,
          -0.9374999999999998,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "pump-b-lock",
        "name": "pump b lock",
        "type": "fixed",
        "parent": "basin",
        "child": "pump-b",
        "anchorParent": [
          4.6,
          0.45,
          2.3
        ],
        "anchorChild": [
          0,
          -0.9374999999999998,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "gantry-feet",
        "name": "gantry feet",
        "type": "fixed",
        "parent": "basin",
        "child": "gantry",
        "anchorParent": [
          -0.5,
          0.3,
          -0.5
        ],
        "anchorChild": [
          0,
          -2.9,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "gantry-slide",
        "name": "gantry slide",
        "type": "prismatic",
        "parent": "gantry",
        "child": "gantry-trolley",
        "anchorParent": [
          0,
          2.8000000000000003,
          0
        ],
        "anchorChild": [
          0,
          -0.1999999999999993,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -4,
          4
        ]
      },
      {
        "id": "north-sensor-link",
        "name": "north sensor link",
        "type": "fixed",
        "parent": "control-tower",
        "child": "sensor-north",
        "anchorParent": [
          3.5,
          -0.9125000000000001,
          -0.9250000000000003
        ],
        "anchorChild": [
          0,
          0.03750000000000009,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "south-sensor-link",
        "name": "south sensor link",
        "type": "fixed",
        "parent": "control-tower",
        "child": "sensor-south",
        "anchorParent": [
          3.5,
          -0.9125000000000001,
          7.074999999999999
        ],
        "anchorChild": [
          0,
          0.03750000000000009,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "barge-mooring",
        "name": "barge mooring",
        "type": "spring",
        "parent": "basin",
        "child": "service-barge",
        "anchorParent": [
          -0.5,
          0.39999999999999997,
          -0.5
        ],
        "anchorChild": [
          0,
          -0.04999999999999993,
          -0.19999999999999996
        ],
        "axis": [
          0,
          1,
          0
        ],
        "stiffness": 4000,
        "damping": 160
      },
      {
        "id": "barge-mooring-2",
        "name": "Separated elastic mooring",
        "type": "spring",
        "parent": "basin",
        "child": "service-barge",
        "anchorParent": [
          1.5,
          0.39999999999999997,
          -0.5
        ],
        "anchorChild": [
          2,
          -0.04999999999999993,
          -0.19999999999999996
        ],
        "restLength": 0,
        "stiffness": 4000,
        "damping": 160
      },
      {
        "id": "barge-mooring-3",
        "name": "Separated elastic mooring",
        "type": "spring",
        "parent": "basin",
        "child": "service-barge",
        "anchorParent": [
          -2.5,
          0.39999999999999997,
          0.5
        ],
        "anchorChild": [
          -2,
          -0.04999999999999993,
          0.8
        ],
        "restLength": 0,
        "stiffness": 4000,
        "damping": 160
      }
    ],
    "modules": [
      "basin",
      "gate-north",
      "gate-south",
      "control-tower",
      "pump-a",
      "pump-b",
      "gantry",
      "gantry-trolley",
      "sensor-north",
      "sensor-south",
      "service-barge"
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 冲击响应读数（h3-flood-response-lock-dynamic）

Rapier 实际采样轨迹中的最大平移位移是多少？按四位小数报告。

能力：冲击响应读数；形式：single-choice；证据：Rapier。

- A：0
- B：0.2
- C：1

```json
{
  "input": {
    "trace": [
      {
        "time": 0.008333333333333333,
        "displacement": 3.2860292265013413e-10
      },
      {
        "time": 0.10833333333333334,
        "displacement": 3.2860292265013413e-10
      },
      {
        "time": 0.20833333333333334,
        "displacement": 3.2860292265013413e-10
      },
      {
        "time": 0.30833333333333335,
        "displacement": 3.2860292265013413e-10
      },
      {
        "time": 0.4083333333333333,
        "displacement": 3.2860292265013413e-10
      },
      {
        "time": 0.5083333333333333,
        "displacement": 3.2860292265013413e-10
      },
      {
        "time": 0.6083333333333333,
        "displacement": 3.2860292265013413e-10
      },
      {
        "time": 0.7083333333333334,
        "displacement": 3.2860292265013413e-10
      },
      {
        "time": 0.8083333333333333,
        "displacement": 3.2860292265013413e-10
      },
      {
        "time": 0.9083333333333333,
        "displacement": 3.2860292265013413e-10
      },
      {
        "time": 1,
        "displacement": 3.2860292265013413e-10
      }
    ],
    "impulse": [
      10,
      1.8,
      3.5
    ],
    "nominalDrift": 0.00897079765991242,
    "scope": "采样轨迹极值，非连续时间极值；不代表实物安全阈值"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 关节限位推理（h3-flood-response-lock-kinematic）

下列目标位置/角度中哪些在关节声明限位内（含边界）？

能力：关节限位推理；形式：multiple-choice；证据：model-state。

- A：-4
- B：0
- C：-4.5
- D：4.5

```json
{
  "input": {
    "joint": "gantry-slide",
    "limits": [
      -4,
      4
    ],
    "units": "scene units"
  },
  "answer": {
    "choiceIds": [
      "A",
      "B"
    ]
  }
}
```

### 约束故障诊断（h3-flood-response-lock-diagnosis）

已检测到端点和约束类型如下，选择匹配的全部关节。

能力：约束故障诊断；形式：multiple-choice；证据：model-state。

- A：tower-foundation
- B：pump-a-lock
- C：north-gate-hinge
- D：south-gate-hinge

```json
{
  "input": {
    "endpoints": [
      "basin",
      "gate-north"
    ],
    "type": "revolute",
    "joints": [
      {
        "id": "north-gate-hinge",
        "name": "north gate hinge",
        "type": "revolute",
        "parent": "basin",
        "child": "gate-north",
        "anchorParent": [
          -3.5,
          0.8,
          -3.5
        ],
        "anchorChild": [
          -3,
          -0.6000000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          0,
          1.2
        ]
      },
      {
        "id": "south-gate-hinge",
        "name": "south gate hinge",
        "type": "revolute",
        "parent": "basin",
        "child": "gate-south",
        "anchorParent": [
          2.5,
          0.8,
          2.5
        ],
        "anchorChild": [
          3,
          -0.6000000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -1.2,
          0
        ]
      },
      {
        "id": "tower-foundation",
        "name": "tower foundation",
        "type": "fixed",
        "parent": "basin",
        "child": "control-tower",
        "anchorParent": [
          -4,
          0.3,
          -4
        ],
        "anchorChild": [
          0,
          -2.4125,
          -0.42500000000000027
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "pump-a-lock",
        "name": "pump a lock",
        "type": "fixed",
        "parent": "basin",
        "child": "pump-a",
        "anchorParent": [
          -5.6,
          0.45,
          2.3
        ],
        "anchorChild": [
          0,
          -0.9374999999999998,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "pump-b-lock",
        "name": "pump b lock",
        "type": "fixed",
        "parent": "basin",
        "child": "pump-b",
        "anchorParent": [
          4.6,
          0.45,
          2.3
        ],
        "anchorChild": [
          0,
          -0.9374999999999998,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "gantry-feet",
        "name": "gantry feet",
        "type": "fixed",
        "parent": "basin",
        "child": "gantry",
        "anchorParent": [
          -0.5,
          0.3,
          -0.5
        ],
        "anchorChild": [
          0,
          -2.9,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "gantry-slide",
        "name": "gantry slide",
        "type": "prismatic",
        "parent": "gantry",
        "child": "gantry-trolley",
        "anchorParent": [
          0,
          2.8000000000000003,
          0
        ],
        "anchorChild": [
          0,
          -0.1999999999999993,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -4,
          4
        ]
      },
      {
        "id": "north-sensor-link",
        "name": "north sensor link",
        "type": "fixed",
        "parent": "control-tower",
        "child": "sensor-north",
        "anchorParent": [
          3.5,
          -0.9125000000000001,
          -0.9250000000000003
        ],
        "anchorChild": [
          0,
          0.03750000000000009,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "south-sensor-link",
        "name": "south sensor link",
        "type": "fixed",
        "parent": "control-tower",
        "child": "sensor-south",
        "anchorParent": [
          3.5,
          -0.9125000000000001,
          7.074999999999999
        ],
        "anchorChild": [
          0,
          0.03750000000000009,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "barge-mooring",
        "name": "barge mooring",
        "type": "spring",
        "parent": "basin",
        "child": "service-barge",
        "anchorParent": [
          -0.5,
          0.39999999999999997,
          -0.5
        ],
        "anchorChild": [
          0,
          -0.04999999999999993,
          -0.19999999999999996
        ],
        "axis": [
          0,
          1,
          0
        ],
        "stiffness": 4000,
        "damping": 160
      },
      {
        "id": "barge-mooring-2",
        "name": "Separated elastic mooring",
        "type": "spring",
        "parent": "basin",
        "child": "service-barge",
        "anchorParent": [
          1.5,
          0.39999999999999997,
          -0.5
        ],
        "anchorChild": [
          2,
          -0.04999999999999993,
          -0.19999999999999996
        ],
        "restLength": 0,
        "stiffness": 4000,
        "damping": 160
      },
      {
        "id": "barge-mooring-3",
        "name": "Separated elastic mooring",
        "type": "spring",
        "parent": "basin",
        "child": "service-barge",
        "anchorParent": [
          -2.5,
          0.39999999999999997,
          0.5
        ],
        "anchorChild": [
          -2,
          -0.04999999999999993,
          0.8
        ],
        "restLength": 0,
        "stiffness": 4000,
        "damping": 160
      }
    ]
  },
  "answer": {
    "choiceIds": [
      "C"
    ]
  }
}
```

### 主动检查收益（h3-flood-response-lock-information-gain）

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
    "module": "pump-a",
    "worlds": [
      "normal",
      "jammed",
      "reversed",
      "loose"
    ]
  },
  "answer": {
    "choiceIds": [
      "A",
      "B"
    ]
  }
}
```

### 不确定性与弃答（h3-flood-response-lock-abstention）

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

### 观测后信念更新（h3-flood-response-lock-posterior）

均匀先验，得到给定观测后，jammed 世界的后验概率是多少？

能力：观测后信念更新；形式：single-choice；证据：finite-world。

- A：1
- B：0
- C：0.25
- D：0.3333333333333333

```json
{
  "input": {
    "module": "pump-a",
    "worlds": [
      "normal",
      "jammed",
      "reversed",
      "loose"
    ],
    "observationByWorld": [
      "positive",
      "negative",
      "positive",
      "positive"
    ],
    "observed": "negative"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 多目标工程权衡（h3-flood-response-lock-pareto）

最小成本、最小质量、最大刚度，选择完整非支配集合。

能力：多目标工程权衡；形式：multiple-choice；证据：model-state。

- A：stock-1
- B：stock-2
- C：stock-3
- D：stock-0

```json
{
  "input": {
    "alternatives": [
      {
        "id": "stock-0",
        "cost": 7,
        "stiffness": 9,
        "mass": 0.9
      },
      {
        "id": "stock-1",
        "cost": 8,
        "stiffness": 9,
        "mass": 1.5
      },
      {
        "id": "stock-2",
        "cost": 7,
        "stiffness": 4,
        "mass": 1.4
      },
      {
        "id": "stock-3",
        "cost": 5,
        "stiffness": 9,
        "mass": 0.5
      }
    ]
  },
  "answer": {
    "choiceIds": [
      "C"
    ]
  }
}
```

### 依赖装配（h3-flood-response-lock-assembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖装配；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [],
    "initialModules": [],
    "actions": [
      {
        "id": "place:sensor-north",
        "label": "安装 sensor-north",
        "requires": [
          "present:control-tower"
        ],
        "forbids": [
          "present:sensor-north"
        ],
        "adds": [
          "present:sensor-north"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-north",
          "visible": true
        }
      },
      {
        "id": "place:pump-b",
        "label": "安装 pump-b",
        "requires": [
          "present:basin"
        ],
        "forbids": [
          "present:pump-b"
        ],
        "adds": [
          "present:pump-b"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "pump-b",
          "visible": true
        }
      },
      {
        "id": "place:sensor-south",
        "label": "安装 sensor-south",
        "requires": [
          "present:control-tower"
        ],
        "forbids": [
          "present:sensor-south"
        ],
        "adds": [
          "present:sensor-south"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-south",
          "visible": true
        }
      },
      {
        "id": "place:gantry",
        "label": "安装 gantry",
        "requires": [
          "present:basin"
        ],
        "forbids": [
          "present:gantry"
        ],
        "adds": [
          "present:gantry"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "gantry",
          "visible": true
        }
      },
      {
        "id": "place:pump-a",
        "label": "安装 pump-a",
        "requires": [
          "present:basin"
        ],
        "forbids": [
          "present:pump-a"
        ],
        "adds": [
          "present:pump-a"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "pump-a",
          "visible": true
        }
      },
      {
        "id": "place:gate-north",
        "label": "安装 gate-north",
        "requires": [
          "present:basin"
        ],
        "forbids": [
          "present:gate-north"
        ],
        "adds": [
          "present:gate-north"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "gate-north",
          "visible": true
        }
      },
      {
        "id": "place:service-barge",
        "label": "安装 service-barge",
        "requires": [
          "present:basin",
          "present:basin",
          "present:basin"
        ],
        "forbids": [
          "present:service-barge"
        ],
        "adds": [
          "present:service-barge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-barge",
          "visible": true
        }
      },
      {
        "id": "place:gate-south",
        "label": "安装 gate-south",
        "requires": [
          "present:basin"
        ],
        "forbids": [
          "present:gate-south"
        ],
        "adds": [
          "present:gate-south"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "gate-south",
          "visible": true
        }
      },
      {
        "id": "place:control-tower",
        "label": "安装 control-tower",
        "requires": [
          "present:basin"
        ],
        "forbids": [
          "present:control-tower"
        ],
        "adds": [
          "present:control-tower"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "control-tower",
          "visible": true
        }
      },
      {
        "id": "place:gantry-trolley",
        "label": "安装 gantry-trolley",
        "requires": [
          "present:gantry"
        ],
        "forbids": [
          "present:gantry-trolley"
        ],
        "adds": [
          "present:gantry-trolley"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "gantry-trolley",
          "visible": true
        }
      },
      {
        "id": "place:basin",
        "label": "安装 basin",
        "requires": [],
        "forbids": [
          "present:basin"
        ],
        "adds": [
          "present:basin"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "basin",
          "visible": true
        }
      }
    ],
    "goalFacts": [
      "present:basin",
      "present:control-tower",
      "present:gantry",
      "present:gantry-trolley",
      "present:pump-a",
      "present:pump-b",
      "present:sensor-north",
      "present:sensor-south",
      "present:gate-north",
      "present:gate-south",
      "present:service-barge"
    ],
    "budget": 11,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "place:basin",
      "place:pump-b",
      "place:gantry",
      "place:pump-a",
      "place:gate-north",
      "place:service-barge",
      "place:gate-south",
      "place:control-tower",
      "place:sensor-north",
      "place:sensor-south",
      "place:gantry-trolley"
    ]
  }
}
```

### 依赖拆解（h3-flood-response-lock-disassembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖拆解；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "present:basin",
      "present:gate-north",
      "present:gate-south",
      "present:control-tower",
      "present:pump-a",
      "present:pump-b",
      "present:gantry",
      "present:gantry-trolley",
      "present:sensor-north",
      "present:sensor-south",
      "present:service-barge"
    ],
    "initialModules": [
      "basin",
      "gate-north",
      "gate-south",
      "control-tower",
      "pump-a",
      "pump-b",
      "gantry",
      "gantry-trolley",
      "sensor-north",
      "sensor-south",
      "service-barge"
    ],
    "actions": [
      {
        "id": "remove:gantry",
        "label": "拆除 gantry",
        "requires": [
          "present:gantry"
        ],
        "forbids": [
          "present:gantry-trolley"
        ],
        "adds": [
          "removed:gantry"
        ],
        "deletes": [
          "present:gantry"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "gantry",
          "visible": false
        }
      },
      {
        "id": "remove:gate-south",
        "label": "拆除 gate-south",
        "requires": [
          "present:gate-south"
        ],
        "forbids": [],
        "adds": [
          "removed:gate-south"
        ],
        "deletes": [
          "present:gate-south"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "gate-south",
          "visible": false
        }
      },
      {
        "id": "remove:gate-north",
        "label": "拆除 gate-north",
        "requires": [
          "present:gate-north"
        ],
        "forbids": [],
        "adds": [
          "removed:gate-north"
        ],
        "deletes": [
          "present:gate-north"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "gate-north",
          "visible": false
        }
      },
      {
        "id": "remove:sensor-north",
        "label": "拆除 sensor-north",
        "requires": [
          "present:sensor-north"
        ],
        "forbids": [],
        "adds": [
          "removed:sensor-north"
        ],
        "deletes": [
          "present:sensor-north"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-north",
          "visible": false
        }
      },
      {
        "id": "remove:pump-b",
        "label": "拆除 pump-b",
        "requires": [
          "present:pump-b"
        ],
        "forbids": [],
        "adds": [
          "removed:pump-b"
        ],
        "deletes": [
          "present:pump-b"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "pump-b",
          "visible": false
        }
      },
      {
        "id": "remove:control-tower",
        "label": "拆除 control-tower",
        "requires": [
          "present:control-tower"
        ],
        "forbids": [
          "present:sensor-north",
          "present:sensor-south"
        ],
        "adds": [
          "removed:control-tower"
        ],
        "deletes": [
          "present:control-tower"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "control-tower",
          "visible": false
        }
      },
      {
        "id": "remove:basin",
        "label": "拆除 basin",
        "requires": [
          "present:basin"
        ],
        "forbids": [
          "present:gate-north",
          "present:gate-south",
          "present:control-tower",
          "present:pump-a",
          "present:pump-b",
          "present:gantry",
          "present:service-barge",
          "present:service-barge",
          "present:service-barge"
        ],
        "adds": [
          "removed:basin"
        ],
        "deletes": [
          "present:basin"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "basin",
          "visible": false
        }
      },
      {
        "id": "remove:service-barge",
        "label": "拆除 service-barge",
        "requires": [
          "present:service-barge"
        ],
        "forbids": [],
        "adds": [
          "removed:service-barge"
        ],
        "deletes": [
          "present:service-barge"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "service-barge",
          "visible": false
        }
      },
      {
        "id": "remove:pump-a",
        "label": "拆除 pump-a",
        "requires": [
          "present:pump-a"
        ],
        "forbids": [],
        "adds": [
          "removed:pump-a"
        ],
        "deletes": [
          "present:pump-a"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "pump-a",
          "visible": false
        }
      },
      {
        "id": "remove:sensor-south",
        "label": "拆除 sensor-south",
        "requires": [
          "present:sensor-south"
        ],
        "forbids": [],
        "adds": [
          "removed:sensor-south"
        ],
        "deletes": [
          "present:sensor-south"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-south",
          "visible": false
        }
      },
      {
        "id": "remove:gantry-trolley",
        "label": "拆除 gantry-trolley",
        "requires": [
          "present:gantry-trolley"
        ],
        "forbids": [],
        "adds": [
          "removed:gantry-trolley"
        ],
        "deletes": [
          "present:gantry-trolley"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "gantry-trolley",
          "visible": false
        }
      }
    ],
    "goalFacts": [
      "removed:service-barge",
      "removed:gate-south",
      "removed:gate-north",
      "removed:sensor-south",
      "removed:sensor-north",
      "removed:pump-b",
      "removed:pump-a",
      "removed:gantry-trolley",
      "removed:gantry",
      "removed:control-tower",
      "removed:basin"
    ],
    "budget": 11,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "remove:gate-south",
      "remove:gate-north",
      "remove:sensor-north",
      "remove:pump-b",
      "remove:service-barge",
      "remove:pump-a",
      "remove:sensor-south",
      "remove:control-tower",
      "remove:gantry-trolley",
      "remove:gantry",
      "remove:basin"
    ]
  }
}
```

### 承载维修（h3-flood-response-lock-service-repair）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：承载维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:pump-a",
      "closed:pump-a"
    ],
    "initialModules": [
      "basin",
      "gate-north",
      "gate-south",
      "control-tower",
      "pump-a",
      "pump-b",
      "gantry",
      "gantry-trolley",
      "sensor-north",
      "sensor-south",
      "service-barge"
    ],
    "actions": [
      {
        "id": "verify:pump-a",
        "label": "verify pump-a",
        "requires": [
          "done:replace:pump-a"
        ],
        "forbids": [
          "done:verify:pump-a"
        ],
        "adds": [
          "done:verify:pump-a"
        ],
        "deletes": [
          "fault:pump-a"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "pump-a"
        }
      },
      {
        "id": "open:pump-a",
        "label": "open pump-a",
        "requires": [
          "done:support:pump-a"
        ],
        "forbids": [
          "done:open:pump-a"
        ],
        "adds": [
          "done:open:pump-a"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "pump-a"
        }
      },
      {
        "id": "release:pump-a",
        "label": "release pump-a",
        "requires": [
          "done:close:pump-a"
        ],
        "forbids": [
          "done:release:pump-a"
        ],
        "adds": [
          "done:release:pump-a",
          "repaired:pump-a"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "pump-a"
        }
      },
      {
        "id": "replace:pump-a",
        "label": "replace pump-a",
        "requires": [
          "done:remove:pump-a"
        ],
        "forbids": [
          "done:replace:pump-a"
        ],
        "adds": [
          "done:replace:pump-a"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "pump-a",
          "visible": true
        }
      },
      {
        "id": "support:pump-a",
        "label": "support pump-a",
        "requires": [
          "fault:pump-a"
        ],
        "forbids": [
          "done:support:pump-a"
        ],
        "adds": [
          "done:support:pump-a"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "pump-a"
        }
      },
      {
        "id": "remove:pump-a",
        "label": "remove pump-a",
        "requires": [
          "done:open:pump-a"
        ],
        "forbids": [
          "done:remove:pump-a"
        ],
        "adds": [
          "done:remove:pump-a"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "pump-a",
          "visible": false
        }
      },
      {
        "id": "close:pump-a",
        "label": "close pump-a",
        "requires": [
          "done:verify:pump-a"
        ],
        "forbids": [
          "done:close:pump-a"
        ],
        "adds": [
          "done:close:pump-a"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "pump-a"
        }
      }
    ],
    "goalFacts": [
      "repaired:pump-a"
    ],
    "budget": 7,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:pump-a",
      "open:pump-a",
      "remove:pump-a",
      "replace:pump-a",
      "verify:pump-a",
      "close:pump-a",
      "release:pump-a"
    ]
  }
}
```

### 复合编辑验证（h3-flood-response-lock-compound-edit）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：复合编辑验证；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:pump-a",
      "closed:pump-a"
    ],
    "initialModules": [
      "basin",
      "gate-north",
      "gate-south",
      "control-tower",
      "pump-a",
      "pump-b",
      "gantry",
      "gantry-trolley",
      "sensor-north",
      "sensor-south",
      "service-barge"
    ],
    "actions": [
      {
        "id": "verify:pump-a",
        "label": "verify pump-a",
        "requires": [
          "done:recolor:pump-a"
        ],
        "forbids": [
          "done:verify:pump-a"
        ],
        "adds": [
          "done:verify:pump-a"
        ],
        "deletes": [
          "fault:pump-a"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "pump-a"
        }
      },
      {
        "id": "recolor:pump-a",
        "label": "recolor pump-a",
        "requires": [
          "done:open:pump-a"
        ],
        "forbids": [
          "done:recolor:pump-a"
        ],
        "adds": [
          "done:recolor:pump-a"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "pump-a",
          "color": "#ea7635"
        }
      },
      {
        "id": "open:pump-a",
        "label": "open pump-a",
        "requires": [
          "done:support:pump-a"
        ],
        "forbids": [
          "done:open:pump-a"
        ],
        "adds": [
          "done:open:pump-a"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "pump-a"
        }
      },
      {
        "id": "release:pump-a",
        "label": "release pump-a",
        "requires": [
          "done:close:pump-a"
        ],
        "forbids": [
          "done:release:pump-a"
        ],
        "adds": [
          "done:release:pump-a",
          "repaired:pump-a"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "pump-a"
        }
      },
      {
        "id": "support:pump-a",
        "label": "support pump-a",
        "requires": [
          "fault:pump-a"
        ],
        "forbids": [
          "done:support:pump-a"
        ],
        "adds": [
          "done:support:pump-a"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "pump-a"
        }
      },
      {
        "id": "close:pump-a",
        "label": "close pump-a",
        "requires": [
          "done:verify:pump-a"
        ],
        "forbids": [
          "done:close:pump-a"
        ],
        "adds": [
          "done:close:pump-a"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "pump-a"
        }
      }
    ],
    "goalFacts": [
      "repaired:pump-a"
    ],
    "budget": 6,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:pump-a",
      "open:pump-a",
      "recolor:pump-a",
      "verify:pump-a",
      "close:pump-a",
      "release:pump-a"
    ]
  }
}
```

### 跨区域联合维修（h3-flood-response-lock-multi-fault）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：跨区域联合维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:gantry-trolley",
      "closed:gantry-trolley",
      "fault:sensor-north",
      "closed:sensor-north",
      "fault:sensor-south",
      "closed:sensor-south",
      "fault:service-barge",
      "closed:service-barge"
    ],
    "initialModules": [
      "basin",
      "gate-north",
      "gate-south",
      "control-tower",
      "pump-a",
      "pump-b",
      "gantry",
      "gantry-trolley",
      "sensor-north",
      "sensor-south",
      "service-barge"
    ],
    "actions": [
      {
        "id": "replace:gantry-trolley",
        "label": "replace gantry-trolley",
        "requires": [
          "done:remove:gantry-trolley"
        ],
        "forbids": [
          "done:replace:gantry-trolley"
        ],
        "adds": [
          "done:replace:gantry-trolley"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "gantry-trolley",
          "visible": true
        }
      },
      {
        "id": "remove:sensor-north",
        "label": "remove sensor-north",
        "requires": [
          "done:open:sensor-north"
        ],
        "forbids": [
          "done:remove:sensor-north"
        ],
        "adds": [
          "done:remove:sensor-north"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-north",
          "visible": false
        }
      },
      {
        "id": "close:sensor-north",
        "label": "close sensor-north",
        "requires": [
          "done:verify:sensor-north"
        ],
        "forbids": [
          "done:close:sensor-north"
        ],
        "adds": [
          "done:close:sensor-north"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-north"
        }
      },
      {
        "id": "verify:service-barge",
        "label": "verify service-barge",
        "requires": [
          "done:replace:service-barge"
        ],
        "forbids": [
          "done:verify:service-barge"
        ],
        "adds": [
          "done:verify:service-barge"
        ],
        "deletes": [
          "fault:service-barge"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "service-barge"
        }
      },
      {
        "id": "replace:sensor-north",
        "label": "replace sensor-north",
        "requires": [
          "done:remove:sensor-north"
        ],
        "forbids": [
          "done:replace:sensor-north"
        ],
        "adds": [
          "done:replace:sensor-north"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-north",
          "visible": true
        }
      },
      {
        "id": "verify:sensor-north",
        "label": "verify sensor-north",
        "requires": [
          "done:replace:sensor-north"
        ],
        "forbids": [
          "done:verify:sensor-north"
        ],
        "adds": [
          "done:verify:sensor-north"
        ],
        "deletes": [
          "fault:sensor-north"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-north"
        }
      },
      {
        "id": "open:gantry-trolley",
        "label": "open gantry-trolley",
        "requires": [
          "done:support:gantry-trolley"
        ],
        "forbids": [
          "done:open:gantry-trolley"
        ],
        "adds": [
          "done:open:gantry-trolley"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "gantry-trolley"
        }
      },
      {
        "id": "close:service-barge",
        "label": "close service-barge",
        "requires": [
          "done:verify:service-barge"
        ],
        "forbids": [
          "done:close:service-barge"
        ],
        "adds": [
          "done:close:service-barge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-barge"
        }
      },
      {
        "id": "release:gantry-trolley",
        "label": "release gantry-trolley",
        "requires": [
          "done:close:gantry-trolley"
        ],
        "forbids": [
          "done:release:gantry-trolley"
        ],
        "adds": [
          "done:release:gantry-trolley",
          "repaired:gantry-trolley"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "gantry-trolley"
        }
      },
      {
        "id": "release:service-barge",
        "label": "release service-barge",
        "requires": [
          "done:close:service-barge"
        ],
        "forbids": [
          "done:release:service-barge"
        ],
        "adds": [
          "done:release:service-barge",
          "repaired:service-barge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-barge"
        }
      },
      {
        "id": "support:service-barge",
        "label": "support service-barge",
        "requires": [
          "fault:service-barge"
        ],
        "forbids": [
          "done:support:service-barge"
        ],
        "adds": [
          "done:support:service-barge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-barge"
        }
      },
      {
        "id": "replace:service-barge",
        "label": "replace service-barge",
        "requires": [
          "done:remove:service-barge"
        ],
        "forbids": [
          "done:replace:service-barge"
        ],
        "adds": [
          "done:replace:service-barge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-barge",
          "visible": true
        }
      },
      {
        "id": "close:sensor-south",
        "label": "close sensor-south",
        "requires": [
          "done:verify:sensor-south"
        ],
        "forbids": [
          "done:close:sensor-south"
        ],
        "adds": [
          "done:close:sensor-south"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-south"
        }
      },
      {
        "id": "verify:sensor-south",
        "label": "verify sensor-south",
        "requires": [
          "done:replace:sensor-south"
        ],
        "forbids": [
          "done:verify:sensor-south"
        ],
        "adds": [
          "done:verify:sensor-south"
        ],
        "deletes": [
          "fault:sensor-south"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-south"
        }
      },
      {
        "id": "remove:service-barge",
        "label": "remove service-barge",
        "requires": [
          "done:open:service-barge"
        ],
        "forbids": [
          "done:remove:service-barge"
        ],
        "adds": [
          "done:remove:service-barge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-barge",
          "visible": false
        }
      },
      {
        "id": "release:sensor-north",
        "label": "release sensor-north",
        "requires": [
          "done:close:sensor-north"
        ],
        "forbids": [
          "done:release:sensor-north"
        ],
        "adds": [
          "done:release:sensor-north",
          "repaired:sensor-north"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-north"
        }
      },
      {
        "id": "replace:sensor-south",
        "label": "replace sensor-south",
        "requires": [
          "done:remove:sensor-south"
        ],
        "forbids": [
          "done:replace:sensor-south"
        ],
        "adds": [
          "done:replace:sensor-south"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-south",
          "visible": true
        }
      },
      {
        "id": "close:gantry-trolley",
        "label": "close gantry-trolley",
        "requires": [
          "done:verify:gantry-trolley"
        ],
        "forbids": [
          "done:close:gantry-trolley"
        ],
        "adds": [
          "done:close:gantry-trolley"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "gantry-trolley"
        }
      },
      {
        "id": "support:sensor-south",
        "label": "support sensor-south",
        "requires": [
          "fault:sensor-south"
        ],
        "forbids": [
          "done:support:sensor-south"
        ],
        "adds": [
          "done:support:sensor-south"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-south"
        }
      },
      {
        "id": "support:sensor-north",
        "label": "support sensor-north",
        "requires": [
          "fault:sensor-north"
        ],
        "forbids": [
          "done:support:sensor-north"
        ],
        "adds": [
          "done:support:sensor-north"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-north"
        }
      },
      {
        "id": "release:sensor-south",
        "label": "release sensor-south",
        "requires": [
          "done:close:sensor-south"
        ],
        "forbids": [
          "done:release:sensor-south"
        ],
        "adds": [
          "done:release:sensor-south",
          "repaired:sensor-south"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-south"
        }
      },
      {
        "id": "remove:sensor-south",
        "label": "remove sensor-south",
        "requires": [
          "done:open:sensor-south"
        ],
        "forbids": [
          "done:remove:sensor-south"
        ],
        "adds": [
          "done:remove:sensor-south"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-south",
          "visible": false
        }
      },
      {
        "id": "remove:gantry-trolley",
        "label": "remove gantry-trolley",
        "requires": [
          "done:open:gantry-trolley"
        ],
        "forbids": [
          "done:remove:gantry-trolley"
        ],
        "adds": [
          "done:remove:gantry-trolley"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "gantry-trolley",
          "visible": false
        }
      },
      {
        "id": "verify:gantry-trolley",
        "label": "verify gantry-trolley",
        "requires": [
          "done:replace:gantry-trolley"
        ],
        "forbids": [
          "done:verify:gantry-trolley"
        ],
        "adds": [
          "done:verify:gantry-trolley"
        ],
        "deletes": [
          "fault:gantry-trolley"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "gantry-trolley"
        }
      },
      {
        "id": "open:service-barge",
        "label": "open service-barge",
        "requires": [
          "done:support:service-barge"
        ],
        "forbids": [
          "done:open:service-barge"
        ],
        "adds": [
          "done:open:service-barge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-barge"
        }
      },
      {
        "id": "open:sensor-north",
        "label": "open sensor-north",
        "requires": [
          "done:support:sensor-north"
        ],
        "forbids": [
          "done:open:sensor-north"
        ],
        "adds": [
          "done:open:sensor-north"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-north"
        }
      },
      {
        "id": "open:sensor-south",
        "label": "open sensor-south",
        "requires": [
          "done:support:sensor-south"
        ],
        "forbids": [
          "done:open:sensor-south"
        ],
        "adds": [
          "done:open:sensor-south"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-south"
        }
      },
      {
        "id": "support:gantry-trolley",
        "label": "support gantry-trolley",
        "requires": [
          "fault:gantry-trolley"
        ],
        "forbids": [
          "done:support:gantry-trolley"
        ],
        "adds": [
          "done:support:gantry-trolley"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "gantry-trolley"
        }
      }
    ],
    "goalFacts": [
      "repaired:gantry-trolley",
      "repaired:sensor-north",
      "repaired:sensor-south",
      "repaired:service-barge"
    ],
    "budget": 28,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:service-barge",
      "support:sensor-south",
      "support:sensor-north",
      "open:service-barge",
      "remove:service-barge",
      "replace:service-barge",
      "verify:service-barge",
      "close:service-barge",
      "release:service-barge",
      "open:sensor-north",
      "remove:sensor-north",
      "replace:sensor-north",
      "verify:sensor-north",
      "close:sensor-north",
      "release:sensor-north",
      "open:sensor-south",
      "remove:sensor-south",
      "replace:sensor-south",
      "verify:sensor-south",
      "close:sensor-south",
      "release:sensor-south",
      "support:gantry-trolley",
      "open:gantry-trolley",
      "remove:gantry-trolley",
      "replace:gantry-trolley",
      "verify:gantry-trolley",
      "close:gantry-trolley",
      "release:gantry-trolley"
    ]
  }
}
```

### 多工位资源调度（h3-flood-response-lock-scheduling）

为所有工单提交整数 starts，满足先后关系、独占工位及截止时间。

能力：多工位资源调度；形式：schedule；证据：resource-schedule。


```json
{
  "input": {
    "jobs": [
      {
        "id": "job-0",
        "module": "basin",
        "duration": 1,
        "resource": "test-bench",
        "after": []
      },
      {
        "id": "job-1",
        "module": "gate-north",
        "duration": 1,
        "resource": "technician",
        "after": []
      },
      {
        "id": "job-2",
        "module": "gate-south",
        "duration": 1,
        "resource": "test-bench",
        "after": [
          "job-0"
        ]
      },
      {
        "id": "job-3",
        "module": "control-tower",
        "duration": 1,
        "resource": "technician",
        "after": [
          "job-1"
        ]
      },
      {
        "id": "job-4",
        "module": "pump-a",
        "duration": 2,
        "resource": "test-bench",
        "after": [
          "job-2"
        ]
      },
      {
        "id": "job-5",
        "module": "pump-b",
        "duration": 3,
        "resource": "technician",
        "after": [
          "job-3"
        ]
      },
      {
        "id": "job-6",
        "module": "gantry",
        "duration": 2,
        "resource": "test-bench",
        "after": [
          "job-4"
        ]
      },
      {
        "id": "job-7",
        "module": "gantry-trolley",
        "duration": 2,
        "resource": "technician",
        "after": [
          "job-5"
        ]
      },
      {
        "id": "job-8",
        "module": "sensor-north",
        "duration": 3,
        "resource": "test-bench",
        "after": [
          "job-6"
        ]
      },
      {
        "id": "job-9",
        "module": "sensor-south",
        "duration": 2,
        "resource": "technician",
        "after": [
          "job-7"
        ]
      }
    ],
    "deadline": 9
  },
  "answer": {
    "starts": {
      "job-0": 0,
      "job-1": 0,
      "job-2": 1,
      "job-3": 1,
      "job-4": 2,
      "job-5": 2,
      "job-6": 4,
      "job-7": 5,
      "job-8": 6,
      "job-9": 7
    }
  }
}
```

### 检查后条件策略（h3-flood-response-lock-policy）

提交一个检查及 observation→action 决策表，在所有相容世界中采取正确动作。

能力：检查后条件策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "pump-a",
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

### 局部坐标变换（h3-flood-response-lock-local-frame）

将模块局部点通过给定四元数与平移转换为世界点，保留五位小数。

能力：局部坐标变换；形式：single-choice；证据：model-state。

- A：[-5.1,1.35,1.8]
- B：[1,-0.2375,0]
- C：[-4.1,1.35,2.8]
- D：[-4.1,2.35,2.8]

```json
{
  "input": {
    "localPoint": [
      1,
      -0.23749999999999982,
      0
    ],
    "rotationXYZW": [
      0,
      0.7071067811865475,
      0,
      0.7071067811865476
    ],
    "translation": [
      -5.1,
      1.5874999999999997,
      2.8
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 正交视图投影（h3-flood-response-lock-projection）

按公开视图坐标约定，选择该世界点投影后的二维坐标。

能力：正交视图投影；形式：single-choice；证据：model-state。

- A：[5,6]
- B：[0,0]
- C：[5,11]
- D：[11,5]

```json
{
  "input": {
    "view": "front",
    "point": [
      5,
      11,
      -6
    ],
    "convention": "front=(x,y), side=(z,y), top=(x,z)"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 空间相对关系（h3-flood-response-lock-relative-order）

比较B相对A在指定世界轴上的模块原点坐标。

能力：空间相对关系；形式：single-choice；证据：model-state。

- A：greater
- B：equal
- C：less

```json
{
  "input": {
    "A": {
      "id": "basin",
      "position": [
        0.5,
        0.2,
        0.5
      ]
    },
    "B": {
      "id": "service-barge",
      "position": [
        0,
        0.6499999999999999,
        0.19999999999999996
      ]
    },
    "axis": "x"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 约束自由度（h3-flood-response-lock-joint-axis）

仅考虑这一声明约束，不计闭环、马达与限位激活，保留多少相对运动自由度？弹簧仅施力、不消除自由度。

能力：约束自由度；形式：single-choice；证据：model-state。

- A：3
- B：6
- C：0
- D：1

```json
{
  "input": {
    "joint": {
      "id": "barge-mooring",
      "name": "barge mooring",
      "type": "spring",
      "parent": "basin",
      "child": "service-barge",
      "anchorParent": [
        -0.5,
        0.39999999999999997,
        -0.5
      ],
      "anchorChild": [
        0,
        -0.04999999999999993,
        -0.19999999999999996
      ],
      "axis": [
        0,
        1,
        0
      ],
      "stiffness": 4000,
      "damping": 160
    }
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 维修间隙预算（h3-flood-response-lock-clearance-margin）

给定理想直槽净宽、工具宽度、单侧安全余量，工具是否满足横向间隙要求？

能力：维修间隙预算；形式：single-choice；证据：model-state。

- A：feasible
- B：blocked

```json
{
  "input": {
    "module": "pump-a",
    "aperture": 0.6900000000000001,
    "toolWidth": 0.65,
    "eachSideMargin": 0
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 载荷力矩（h3-flood-response-lock-load-moment）

绕给定原点的载荷力矩r×F是多少？采用右手系，忽略其他力。

能力：载荷力矩；形式：single-choice；证据：model-state。

- A：[0,0,0]
- B：[0,-4,0]
- C：[0,0,-12]
- D：[0,0,12]

```json
{
  "input": {
    "module": "pump-a",
    "lever": [
      4,
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
    "choiceId": "C"
  }
}
```

### 非均匀先验更新（h3-flood-response-lock-weighted-posterior）

先验权重未归一化，观测只保留normal和jammed，求jammed后验概率。

能力：非均匀先验更新；形式：single-choice；证据：finite-world。

- A：0.6666666666666666
- B：0.36363636363636365
- C：0
- D：1

```json
{
  "input": {
    "module": "pump-a",
    "worlds": [
      "normal",
      "jammed",
      "loose"
    ],
    "weights": [
      2,
      4,
      5
    ],
    "compatible": [
      "normal",
      "jammed"
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 风险最小决策（h3-flood-response-lock-expected-loss）

继续运行期望损失=p×failureLoss，预防维修损失=repairCost，选择损失较低者；并列选继续。

能力：风险最小决策；形式：single-choice；证据：finite-world。

- A：continue
- B：repair

```json
{
  "input": {
    "faultProbability": 0.6,
    "repairCost": 2,
    "failureLoss": 16,
    "module": "pump-a"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 轨迹阈值判定（h3-flood-response-lock-trace-threshold）

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
        "displacement": 3.2860292265013413e-10
      },
      {
        "time": 0.10833333333333334,
        "displacement": 3.2860292265013413e-10
      },
      {
        "time": 0.20833333333333334,
        "displacement": 3.2860292265013413e-10
      },
      {
        "time": 0.30833333333333335,
        "displacement": 3.2860292265013413e-10
      },
      {
        "time": 0.4083333333333333,
        "displacement": 3.2860292265013413e-10
      },
      {
        "time": 0.5083333333333333,
        "displacement": 3.2860292265013413e-10
      },
      {
        "time": 0.6083333333333333,
        "displacement": 3.2860292265013413e-10
      },
      {
        "time": 0.7083333333333334,
        "displacement": 3.2860292265013413e-10
      },
      {
        "time": 0.8083333333333333,
        "displacement": 3.2860292265013413e-10
      },
      {
        "time": 0.9083333333333333,
        "displacement": 3.2860292265013413e-10
      },
      {
        "time": 1,
        "displacement": 3.2860292265013413e-10
      }
    ],
    "threshold": 3.9432350718016095e-10
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 安全联锁维修（h3-flood-response-lock-guarded-repair）

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
        "id": "release:pump-a",
        "label": "release pump-a",
        "requires": [
          "done:relock:pump-a"
        ],
        "forbids": [
          "done:release:pump-a"
        ],
        "adds": [
          "done:release:pump-a",
          "ready:pump-a",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "pump-a"
        }
      },
      {
        "id": "relock:pump-a",
        "label": "relock pump-a",
        "requires": [
          "done:verify:pump-a"
        ],
        "forbids": [
          "done:relock:pump-a"
        ],
        "adds": [
          "done:relock:pump-a"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "pump-a"
        }
      },
      {
        "id": "verify:pump-a",
        "label": "verify pump-a",
        "requires": [
          "done:replace:pump-a"
        ],
        "forbids": [
          "done:verify:pump-a"
        ],
        "adds": [
          "done:verify:pump-a"
        ],
        "deletes": [
          "fault:pump-a",
          "misaligned:pump-a"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "pump-a"
        }
      },
      {
        "id": "replace:pump-a",
        "label": "replace pump-a",
        "requires": [
          "done:unlock:pump-a"
        ],
        "forbids": [
          "done:replace:pump-a"
        ],
        "adds": [
          "done:replace:pump-a"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "pump-a"
        }
      },
      {
        "id": "unlock:pump-a",
        "label": "unlock pump-a",
        "requires": [
          "done:support:pump-a"
        ],
        "forbids": [
          "done:unlock:pump-a"
        ],
        "adds": [
          "done:unlock:pump-a"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "pump-a"
        }
      },
      {
        "id": "support:pump-a",
        "label": "support pump-a",
        "requires": [
          "done:isolate:pump-a"
        ],
        "forbids": [
          "done:support:pump-a"
        ],
        "adds": [
          "done:support:pump-a"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "pump-a"
        }
      },
      {
        "id": "isolate:pump-a",
        "label": "isolate pump-a",
        "requires": [
          "tool:free",
          "fault:pump-a"
        ],
        "forbids": [
          "done:isolate:pump-a"
        ],
        "adds": [
          "done:isolate:pump-a"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "pump-a"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:pump-a"
    ],
    "initialModules": [
      "basin",
      "gate-north",
      "gate-south",
      "control-tower",
      "pump-a",
      "pump-b",
      "gantry",
      "gantry-trolley",
      "sensor-north",
      "sensor-south",
      "service-barge"
    ],
    "goalFacts": [
      "ready:pump-a"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 8
  },
  "answer": {
    "actionIds": [
      "isolate:pump-a",
      "support:pump-a",
      "unlock:pump-a",
      "replace:pump-a",
      "verify:pump-a",
      "relock:pump-a",
      "release:pump-a"
    ]
  }
}
```

### 失败状态回退（h3-flood-response-lock-rollback）

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
        "id": "resume:pump-a",
        "label": "resume pump-a",
        "requires": [
          "done:verify:pump-a"
        ],
        "forbids": [
          "done:resume:pump-a"
        ],
        "adds": [
          "done:resume:pump-a",
          "ready:pump-a",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "pump-a"
        }
      },
      {
        "id": "verify:pump-a",
        "label": "verify pump-a",
        "requires": [
          "done:align:pump-a"
        ],
        "forbids": [
          "done:verify:pump-a"
        ],
        "adds": [
          "done:verify:pump-a"
        ],
        "deletes": [
          "fault:pump-a",
          "misaligned:pump-a"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "pump-a"
        }
      },
      {
        "id": "align:pump-a",
        "label": "align pump-a",
        "requires": [
          "done:undo:pump-a"
        ],
        "forbids": [
          "done:align:pump-a"
        ],
        "adds": [
          "done:align:pump-a"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "pump-a",
          "visible": true
        }
      },
      {
        "id": "undo:pump-a",
        "label": "undo pump-a",
        "requires": [
          "done:isolate:pump-a"
        ],
        "forbids": [
          "done:undo:pump-a"
        ],
        "adds": [
          "done:undo:pump-a"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "pump-a",
          "visible": false
        }
      },
      {
        "id": "isolate:pump-a",
        "label": "isolate pump-a",
        "requires": [
          "tool:free",
          "fault:pump-a"
        ],
        "forbids": [
          "done:isolate:pump-a"
        ],
        "adds": [
          "done:isolate:pump-a"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "pump-a"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:pump-a",
      "misaligned:pump-a"
    ],
    "initialModules": [
      "basin",
      "gate-north",
      "gate-south",
      "control-tower",
      "pump-a",
      "pump-b",
      "gantry",
      "gantry-trolley",
      "sensor-north",
      "sensor-south",
      "service-barge"
    ],
    "goalFacts": [
      "ready:pump-a"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 5
  },
  "answer": {
    "actionIds": [
      "isolate:pump-a",
      "undo:pump-a",
      "align:pump-a",
      "verify:pump-a",
      "resume:pump-a"
    ]
  }
}
```

### 共享工具协同维修（h3-flood-response-lock-resource-repair）

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
        "id": "release:service-barge",
        "label": "release service-barge",
        "requires": [
          "done:relock:service-barge"
        ],
        "forbids": [
          "done:release:service-barge"
        ],
        "adds": [
          "done:release:service-barge",
          "ready:service-barge",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-barge"
        }
      },
      {
        "id": "relock:service-barge",
        "label": "relock service-barge",
        "requires": [
          "done:verify:service-barge"
        ],
        "forbids": [
          "done:relock:service-barge"
        ],
        "adds": [
          "done:relock:service-barge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-barge"
        }
      },
      {
        "id": "verify:service-barge",
        "label": "verify service-barge",
        "requires": [
          "done:replace:service-barge"
        ],
        "forbids": [
          "done:verify:service-barge"
        ],
        "adds": [
          "done:verify:service-barge"
        ],
        "deletes": [
          "fault:service-barge",
          "misaligned:service-barge"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "service-barge"
        }
      },
      {
        "id": "replace:service-barge",
        "label": "replace service-barge",
        "requires": [
          "done:unlock:service-barge"
        ],
        "forbids": [
          "done:replace:service-barge"
        ],
        "adds": [
          "done:replace:service-barge"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "service-barge"
        }
      },
      {
        "id": "unlock:service-barge",
        "label": "unlock service-barge",
        "requires": [
          "done:support:service-barge"
        ],
        "forbids": [
          "done:unlock:service-barge"
        ],
        "adds": [
          "done:unlock:service-barge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-barge"
        }
      },
      {
        "id": "support:service-barge",
        "label": "support service-barge",
        "requires": [
          "done:isolate:service-barge"
        ],
        "forbids": [
          "done:support:service-barge"
        ],
        "adds": [
          "done:support:service-barge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-barge"
        }
      },
      {
        "id": "isolate:service-barge",
        "label": "isolate service-barge",
        "requires": [
          "tool:free",
          "fault:service-barge"
        ],
        "forbids": [
          "done:isolate:service-barge"
        ],
        "adds": [
          "done:isolate:service-barge"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "service-barge"
        }
      },
      {
        "id": "release:sensor-south",
        "label": "release sensor-south",
        "requires": [
          "done:relock:sensor-south"
        ],
        "forbids": [
          "done:release:sensor-south"
        ],
        "adds": [
          "done:release:sensor-south",
          "ready:sensor-south",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-south"
        }
      },
      {
        "id": "relock:sensor-south",
        "label": "relock sensor-south",
        "requires": [
          "done:verify:sensor-south"
        ],
        "forbids": [
          "done:relock:sensor-south"
        ],
        "adds": [
          "done:relock:sensor-south"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-south"
        }
      },
      {
        "id": "verify:sensor-south",
        "label": "verify sensor-south",
        "requires": [
          "done:replace:sensor-south"
        ],
        "forbids": [
          "done:verify:sensor-south"
        ],
        "adds": [
          "done:verify:sensor-south"
        ],
        "deletes": [
          "fault:sensor-south",
          "misaligned:sensor-south"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-south"
        }
      },
      {
        "id": "replace:sensor-south",
        "label": "replace sensor-south",
        "requires": [
          "done:unlock:sensor-south"
        ],
        "forbids": [
          "done:replace:sensor-south"
        ],
        "adds": [
          "done:replace:sensor-south"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "sensor-south"
        }
      },
      {
        "id": "unlock:sensor-south",
        "label": "unlock sensor-south",
        "requires": [
          "done:support:sensor-south"
        ],
        "forbids": [
          "done:unlock:sensor-south"
        ],
        "adds": [
          "done:unlock:sensor-south"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-south"
        }
      },
      {
        "id": "support:sensor-south",
        "label": "support sensor-south",
        "requires": [
          "done:isolate:sensor-south"
        ],
        "forbids": [
          "done:support:sensor-south"
        ],
        "adds": [
          "done:support:sensor-south"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-south"
        }
      },
      {
        "id": "isolate:sensor-south",
        "label": "isolate sensor-south",
        "requires": [
          "tool:free",
          "fault:sensor-south"
        ],
        "forbids": [
          "done:isolate:sensor-south"
        ],
        "adds": [
          "done:isolate:sensor-south"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-south"
        }
      },
      {
        "id": "release:sensor-north",
        "label": "release sensor-north",
        "requires": [
          "done:relock:sensor-north"
        ],
        "forbids": [
          "done:release:sensor-north"
        ],
        "adds": [
          "done:release:sensor-north",
          "ready:sensor-north",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-north"
        }
      },
      {
        "id": "relock:sensor-north",
        "label": "relock sensor-north",
        "requires": [
          "done:verify:sensor-north"
        ],
        "forbids": [
          "done:relock:sensor-north"
        ],
        "adds": [
          "done:relock:sensor-north"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-north"
        }
      },
      {
        "id": "verify:sensor-north",
        "label": "verify sensor-north",
        "requires": [
          "done:replace:sensor-north"
        ],
        "forbids": [
          "done:verify:sensor-north"
        ],
        "adds": [
          "done:verify:sensor-north"
        ],
        "deletes": [
          "fault:sensor-north",
          "misaligned:sensor-north"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-north"
        }
      },
      {
        "id": "replace:sensor-north",
        "label": "replace sensor-north",
        "requires": [
          "done:unlock:sensor-north"
        ],
        "forbids": [
          "done:replace:sensor-north"
        ],
        "adds": [
          "done:replace:sensor-north"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "sensor-north"
        }
      },
      {
        "id": "unlock:sensor-north",
        "label": "unlock sensor-north",
        "requires": [
          "done:support:sensor-north"
        ],
        "forbids": [
          "done:unlock:sensor-north"
        ],
        "adds": [
          "done:unlock:sensor-north"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-north"
        }
      },
      {
        "id": "support:sensor-north",
        "label": "support sensor-north",
        "requires": [
          "done:isolate:sensor-north"
        ],
        "forbids": [
          "done:support:sensor-north"
        ],
        "adds": [
          "done:support:sensor-north"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-north"
        }
      },
      {
        "id": "isolate:sensor-north",
        "label": "isolate sensor-north",
        "requires": [
          "tool:free",
          "fault:sensor-north"
        ],
        "forbids": [
          "done:isolate:sensor-north"
        ],
        "adds": [
          "done:isolate:sensor-north"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-north"
        }
      },
      {
        "id": "release:gantry-trolley",
        "label": "release gantry-trolley",
        "requires": [
          "done:relock:gantry-trolley"
        ],
        "forbids": [
          "done:release:gantry-trolley"
        ],
        "adds": [
          "done:release:gantry-trolley",
          "ready:gantry-trolley",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "gantry-trolley"
        }
      },
      {
        "id": "relock:gantry-trolley",
        "label": "relock gantry-trolley",
        "requires": [
          "done:verify:gantry-trolley"
        ],
        "forbids": [
          "done:relock:gantry-trolley"
        ],
        "adds": [
          "done:relock:gantry-trolley"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "gantry-trolley"
        }
      },
      {
        "id": "verify:gantry-trolley",
        "label": "verify gantry-trolley",
        "requires": [
          "done:replace:gantry-trolley"
        ],
        "forbids": [
          "done:verify:gantry-trolley"
        ],
        "adds": [
          "done:verify:gantry-trolley"
        ],
        "deletes": [
          "fault:gantry-trolley",
          "misaligned:gantry-trolley"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "gantry-trolley"
        }
      },
      {
        "id": "replace:gantry-trolley",
        "label": "replace gantry-trolley",
        "requires": [
          "done:unlock:gantry-trolley"
        ],
        "forbids": [
          "done:replace:gantry-trolley"
        ],
        "adds": [
          "done:replace:gantry-trolley"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "gantry-trolley"
        }
      },
      {
        "id": "unlock:gantry-trolley",
        "label": "unlock gantry-trolley",
        "requires": [
          "done:support:gantry-trolley"
        ],
        "forbids": [
          "done:unlock:gantry-trolley"
        ],
        "adds": [
          "done:unlock:gantry-trolley"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "gantry-trolley"
        }
      },
      {
        "id": "support:gantry-trolley",
        "label": "support gantry-trolley",
        "requires": [
          "done:isolate:gantry-trolley"
        ],
        "forbids": [
          "done:support:gantry-trolley"
        ],
        "adds": [
          "done:support:gantry-trolley"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "gantry-trolley"
        }
      },
      {
        "id": "isolate:gantry-trolley",
        "label": "isolate gantry-trolley",
        "requires": [
          "tool:free",
          "fault:gantry-trolley"
        ],
        "forbids": [
          "done:isolate:gantry-trolley"
        ],
        "adds": [
          "done:isolate:gantry-trolley"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "gantry-trolley"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:gantry-trolley",
      "fault:sensor-north",
      "fault:sensor-south",
      "fault:service-barge"
    ],
    "initialModules": [
      "basin",
      "gate-north",
      "gate-south",
      "control-tower",
      "pump-a",
      "pump-b",
      "gantry",
      "gantry-trolley",
      "sensor-north",
      "sensor-south",
      "service-barge"
    ],
    "goalFacts": [
      "ready:gantry-trolley",
      "ready:sensor-north",
      "ready:sensor-south",
      "ready:service-barge"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 32
  },
  "answer": {
    "actionIds": [
      "isolate:service-barge",
      "support:service-barge",
      "unlock:service-barge",
      "replace:service-barge",
      "verify:service-barge",
      "relock:service-barge",
      "release:service-barge",
      "isolate:sensor-south",
      "support:sensor-south",
      "unlock:sensor-south",
      "replace:sensor-south",
      "verify:sensor-south",
      "relock:sensor-south",
      "release:sensor-south",
      "isolate:sensor-north",
      "support:sensor-north",
      "unlock:sensor-north",
      "replace:sensor-north",
      "verify:sensor-north",
      "relock:sensor-north",
      "release:sensor-north",
      "isolate:gantry-trolley",
      "support:gantry-trolley",
      "unlock:gantry-trolley",
      "replace:gantry-trolley",
      "verify:gantry-trolley",
      "relock:gantry-trolley",
      "release:gantry-trolley"
    ]
  }
}
```

### 预算约束检查策略（h3-flood-response-lock-budget-policy）

提交预算内、对所有相容世界均正确的检查决策表。

能力：预算约束检查策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "pump-a",
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
        "cost": 0,
        "returns": {
          "nominal": "clear",
          "fault": "clear"
        }
      },
      {
        "id": "probe",
        "cost": 2,
        "returns": {
          "nominal": "clear",
          "fault": "alert"
        }
      },
      {
        "id": "thermal",
        "cost": 1,
        "returns": {
          "nominal": "clear",
          "fault": "alert"
        }
      }
    ],
    "budget": 1
  },
  "answer": {
    "queryId": "thermal",
    "decisions": {
      "clear": "continue",
      "alert": "replace"
    }
  }
}
```
