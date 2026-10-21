# 全部 benchmark 模型与题目清单

这次论文覆盖之前的静态配置、动态完整物件和局部结构，以及后来增加的社区模块。12 个社区模块不是整个 bench。

| 部分 | 配置/结构 | 题目 |
|---|---:|---:|
| S：白底板静态 | 160 | 3,292 |
| D：动态（42 个完整物件 + 26 个机制结构） | 68 | 1,872 |
| M：社区模块 | 12 | 96（静态 48 + 动态 48） |
| 合计 | 240 个分轨配置条目，不当成 240 个独立模型 | 5,260 条当前题目记录 |

原来的 127 种静态配置已包含在 160 种里；原来的 30 个动态结构全部保留在 68 个里，包含最初的椅子、桌子、小汽车、吊机。旧版题量不能再累加一次。静态、动态以及社区模块也可能来自同一个原始套装，因此按来源分组比较。

## 静态：全部 160 种配置

| 编号 | 模型/配置 | 名称 | 目标件数 | 题数 | 正常题 | 错误与数量 |
|---|---|---|---:|---:|---:|---|
| S001 | `10001` | Metroliner | 11 | 72 | 1 | compound: 8；control: 1；height_layer: 1；missing: 4；offset: 2；repair_state: 49；rotation: 2；wrong_color: 3；wrong_size: 1；wrong_type: 1 |
| S002 | `10001--deep` | Metroliner · 深层相连结构 | 16 | 48 | 1 | compound: 8；control: 1；missing: 4；repair_state: 32；wrong_color: 3 |
| S003 | `10014` | Caboose | 11 | 33 | 1 | compound: 8；control: 1；missing: 4；offset: 2；repair_state: 13；rotation: 2；wrong_color: 3 |
| S004 | `10036` | Pizza To Go | 11 | 73 | 1 | compound: 8；control: 1；height_layer: 1；missing: 4；offset: 2；repair_state: 51；rotation: 2；wrong_color: 3；wrong_type: 1 |
| S005 | `10036--alt1` | Pizza To Go · 原模型另一处相连结构 | 11 | 28 | 1 | compound: 8；control: 1；extra: 1；missing: 10；offset: 1；rotation: 1；wrong_color: 4；wrong_size: 1；wrong_type: 1 |
| S006 | `10128` | Train Level Crossing | 11 | 24 | 1 | compound: 3；control: 1；height_layer: 1；missing: 4；offset: 2；repair_state: 6；rotation: 2；wrong_color: 3；wrong_size: 1；wrong_type: 1 |
| S007 | `10156` | LEGO Truck | 11 | 68 | 1 | compound: 8；control: 1；height_layer: 1；missing: 4；offset: 2；repair_state: 46；rotation: 2；wrong_color: 3；wrong_type: 1 |
| S008 | `10156--alt1` | LEGO Truck · 原模型另一处相连结构 | 11 | 20 | 1 | compound: 8；control: 1；extra: 1；missing: 4；rotation: 1；wrong_color: 4；wrong_type: 1 |
| S009 | `10159` | City Airport | 11 | 23 | 1 | compound: 3；control: 1；height_layer: 1；missing: 4；offset: 2；repair_state: 6；rotation: 2；wrong_color: 3；wrong_size: 1 |
| S010 | `10213` | Shuttle Adventure | 11 | 62 | 1 | compound: 8；control: 1；missing: 4；offset: 2；repair_state: 41；rotation: 2；wrong_color: 3；wrong_type: 1 |
| S011 | `10214` | Tower Bridge | 11 | 21 | 1 | compound: 3；control: 1；height_layer: 1；missing: 4；offset: 2；repair_state: 3；rotation: 2；wrong_color: 3；wrong_size: 1；wrong_type: 1 |
| S012 | `10220` | Volkswagen T1 Camper Van | 11 | 28 | 1 | compound: 8；control: 1；height_layer: 1；missing: 4；offset: 2；repair_state: 6；rotation: 2；wrong_color: 3；wrong_type: 1 |
| S013 | `31009` | Small Cottage | 11 | 18 | 1 | compound: 3；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_size: 1；wrong_type: 1 |
| S014 | `31027` | Blue Racer | 11 | 22 | 1 | compound: 8；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_type: 1 |
| S015 | `31027--alt1` | Blue Racer · 原模型另一处相连结构 | 11 | 26 | 1 | compound: 8；control: 1；missing: 8；offset: 1；rotation: 1；swapped_positions: 2；wrong_color: 4；wrong_type: 1 |
| S016 | `31027-kart` | Kart | 11 | 22 | 1 | compound: 8；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_type: 1 |
| S017 | `31028` | Sea Plane | 11 | 6 | 1 | control: 1；missing: 2；offset: 1；rotation: 2 |
| S018 | `31028--alt1` | Sea Plane · 原模型另一处相连结构 | 11 | 25 | 1 | compound: 8；control: 1；extra: 1；missing: 8；offset: 1；rotation: 1；wrong_color: 4；wrong_type: 1 |
| S019 | `31028-sailboat` | Sailboat | 11 | 25 | 1 | compound: 8；control: 1；height_layer: 1；missing: 4；offset: 2；repair_state: 3；rotation: 2；wrong_color: 3；wrong_type: 1 |
| S020 | `5867` | Super Speedster | 11 | 22 | 1 | compound: 8；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_size: 1 |
| S021 | `omr-10242` | MINI Cooper | 11 | 16 | 1 | compound: 3；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 1；wrong_color: 3；wrong_type: 1 |
| S022 | `omr-10265` | Ford Mustang | 11 | 9 | 1 | compound: 1；control: 1；missing: 3；offset: 2；wrong_color: 2 |
| S023 | `omr-10269` | Harley-Davidson Fat Boy | 11 | 3 | 1 | control: 1；height_layer: 1；missing: 1 |
| S024 | `omr-21309` | NASA Apollo Saturn V | 11 | 19 | 1 | compound: 8；control: 1；missing: 4；rotation: 2；wrong_color: 3；wrong_size: 1 |
| S025 | `omr-31031` | Rainforest Animals | 11 | 20 | 1 | compound: 8；control: 1；missing: 4；offset: 1；rotation: 2；wrong_color: 3；wrong_type: 1 |
| S026 | `omr-31088` | Deep Sea Creatures | 11 | 6 | 1 | control: 1；missing: 2；rotation: 1；wrong_color: 2 |
| S027 | `omr-42004` | Mini Backhoe Loader | 11 | 18 | 1 | compound: 8；control: 1；missing: 4；offset: 2；wrong_color: 3 |
| S028 | `omr-42020` | Twin-Rotor Helicopter | 11 | 18 | 1 | compound: 8；control: 1；missing: 4；offset: 2；wrong_color: 3 |
| S029 | `omr-42020--alt1` | Twin-Rotor Helicopter · 原模型另一处相连结构 | 11 | 17 | 1 | compound: 8；control: 1；missing: 4；wrong_color: 4 |
| S030 | `omr-42054` | CLAAS XERION 5000 TRAC VC | 11 | 18 | 1 | compound: 8；control: 1；missing: 4；offset: 2；wrong_color: 3 |
| S031 | `omr-42061` | Telehandler | 11 | 18 | 1 | compound: 8；control: 1；missing: 4；offset: 2；wrong_color: 3 |
| S032 | `omr-42066` | Air Race Jet | 11 | 7 | 1 | control: 1；missing: 3；wrong_color: 3 |
| S033 | `omr-42102` | Mini CLAAS XERION | 11 | 17 | 1 | compound: 8；control: 1；missing: 4；offset: 1；wrong_color: 3 |
| S034 | `omr-42102--alt1` | Mini CLAAS XERION · 原模型另一处相连结构 | 11 | 9 | 1 | compound: 2；control: 1；missing: 3；wrong_color: 3 |
| S035 | `v23-10037` | Breezeway Cafe | 11 | 15 | 1 | compound: 3；control: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3 |
| S036 | `v23-10124` | Wright Flyer | 11 | 22 | 1 | compound: 8；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_type: 1 |
| S037 | `v23-10158` | High Speed Train Car | 11 | 29 | 1 | compound: 8；control: 1；height_layer: 1；missing: 4；offset: 2；repair_state: 6；rotation: 2；wrong_color: 3；wrong_type: 2 |
| S038 | `v23-10184` | Town Plan | 11 | 17 | 1 | compound: 3；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_type: 1 |
| S039 | `v23-10194` | Emerald Night | 11 | 17 | 1 | compound: 3；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_type: 1 |
| S040 | `v23-10226` | Sopwith Camel | 11 | 24 | 1 | compound: 8；control: 1；missing: 4；offset: 2；repair_state: 3；rotation: 2；wrong_color: 3；wrong_type: 1 |
| S041 | `v23-10233` | Horizon Express | 11 | 23 | 1 | compound: 8；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_size: 1；wrong_type: 1 |
| S042 | `v23-10241` | Maersk Line Triple-E | 11 | 18 | 1 | compound: 3；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_type: 2 |
| S043 | `v23-10248` | Ferrari F40 | 11 | 25 | 1 | compound: 8；control: 1；height_layer: 1；missing: 4；offset: 2；repair_state: 2；rotation: 2；wrong_color: 3；wrong_type: 2 |
| S044 | `v23-10258` | London Bus | 11 | 18 | 1 | compound: 3；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_type: 2 |
| S045 | `v23-10261` | Roller Coaster | 11 | 17 | 1 | compound: 3；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_type: 1 |
| S046 | `v23-10262` | James Bond Aston Martin DB5 | 11 | 22 | 1 | compound: 8；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_size: 1 |
| S047 | `v23-10267` | Gingerbread House | 11 | 18 | 1 | compound: 3；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_type: 2 |
| S048 | `v23-10271` | Fiat 500 | 11 | 21 | 1 | compound: 8；control: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_type: 1 |
| S049 | `v23-1472` | Holiday Home | 11 | 18 | 1 | compound: 3；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_size: 1；wrong_type: 1 |
| S050 | `v23-1484` | Weetabix Town House | 11 | 16 | 1 | compound: 3；control: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_size: 1 |
| S051 | `v23-1489` | Mobile Car Crane | 11 | 23 | 1 | compound: 8；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_type: 2 |
| S052 | `v23-1490` | Town Bank | 11 | 16 | 1 | compound: 3；control: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_size: 1 |
| S053 | `v23-1490--alt1` | Town Bank · 原模型另一处相连结构 | 11 | 27 | 1 | compound: 8；control: 1；extra: 1；missing: 9；offset: 1；rotation: 1；swapped_positions: 1；wrong_color: 4；wrong_size: 1 |
| S054 | `v23-1572` | Super Tow Truck | 11 | 22 | 1 | compound: 8；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_size: 1 |
| S055 | `v23-1572--alt1` | Super Tow Truck · 原模型另一处相连结构 | 11 | 23 | 1 | compound: 8；control: 1；extra: 1；missing: 6；offset: 1；rotation: 1；wrong_color: 4；wrong_type: 1 |
| S056 | `v23-1632` | Motor Boat | 11 | 19 | 1 | compound: 8；control: 1；height_layer: 1；missing: 3；offset: 1；rotation: 1；wrong_color: 3；wrong_type: 1 |
| S057 | `v23-1633` | Loader Tractor | 11 | 23 | 1 | compound: 8；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_type: 2 |
| S058 | `v23-1682` | Space Shuttle | 11 | 16 | 1 | compound: 3；control: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_size: 1 |
| S059 | `v23-1775` | Jet | 11 | 16 | 1 | compound: 3；control: 1；height_layer: 1；missing: 4；offset: 1；rotation: 2；wrong_color: 3；wrong_type: 1 |
| S060 | `v23-1775--alt1` | Jet · 原模型另一处相连结构 | 10 | 21 | 1 | compound: 8；control: 1；extra: 1；missing: 4；swapped_positions: 1；wrong_color: 4；wrong_size: 1；wrong_type: 1 |
| S061 | `v23-1792` | Pleasure Cruiser | 11 | 22 | 1 | compound: 8；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_type: 1 |
| S062 | `v23-1808` | Light Aircraft and Ground Support | 11 | 22 | 1 | compound: 8；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_type: 1 |
| S063 | `v23-1808--alt1` | Light Aircraft and Ground Support · 原模型另一处相连结构 | 11 | 21 | 1 | compound: 8；control: 1；extra: 1；missing: 4；offset: 1；rotation: 1；swapped_positions: 1；wrong_color: 4 |
| S064 | `v23-1854` | House with Roof-Windows ( Velux ) | 11 | 18 | 1 | compound: 3；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_size: 2 |
| S065 | `v23-1854--alt1` | House with Roof-Windows ( Velux ) · 原模型另一处相连结构 | 11 | 25 | 1 | compound: 8；control: 1；missing: 8；offset: 1；swapped_positions: 1；wrong_color: 4；wrong_size: 1；wrong_type: 1 |
| S066 | `v23-20015` | Alligator | 11 | 21 | 1 | compound: 8；control: 1；missing: 4；offset: 2；rotation: 1；wrong_color: 3；wrong_type: 2 |
| S067 | `v23-20015--alt1` | Alligator · 原模型另一处相连结构 | 11 | 25 | 1 | compound: 8；control: 1；missing: 9；offset: 1；rotation: 1；wrong_color: 4；wrong_type: 1 |
| S068 | `v23-21004` | Solomon R. Guggenheim Museum | 11 | 14 | 1 | compound: 3；control: 1；missing: 4；offset: 2；rotation: 1；wrong_color: 3 |
| S069 | `v23-21005` | Fallingwater | 11 | 17 | 1 | compound: 3；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_type: 1 |
| S070 | `v23-21006` | The White House | 11 | 22 | 1 | compound: 8；control: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_size: 1；wrong_type: 1 |
| S071 | `v23-21007` | Rockefeller Center | 11 | 18 | 1 | compound: 3；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_size: 1；wrong_type: 1 |
| S072 | `v23-21009` | Farnsworth House | 11 | 14 | 1 | compound: 3；control: 1；height_layer: 1；missing: 4；offset: 2；wrong_color: 3 |
| S073 | `v23-21010` | Robie House | 11 | 22 | 1 | compound: 8；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_size: 1 |
| S074 | `v23-21011` | Brandenburg Gate | 11 | 21 | 1 | compound: 8；control: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_size: 1 |
| S075 | `v23-21012` | Sydney Opera House | 11 | 22 | 1 | compound: 8；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_size: 1 |
| S076 | `v23-21014` | Villa Savoye | 11 | 22 | 1 | compound: 8；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_type: 1 |
| S077 | `v23-21016` | Sungnyemun | 11 | 18 | 1 | compound: 3；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_size: 1；wrong_type: 1 |
| S078 | `v23-21017` | Imperial Hotel | 11 | 22 | 1 | compound: 8；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_type: 1 |
| S079 | `v23-21018` | United Nations Headquarters | 11 | 22 | 1 | compound: 8；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_type: 1 |
| S080 | `v23-21020` | The Trevi Fountain | 11 | 17 | 1 | compound: 3；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_type: 1 |
| S081 | `v23-21021` | Marina Bay Sands | 11 | 22 | 1 | compound: 8；control: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_type: 2 |
| S082 | `v23-21022` | Lincoln Memorial | 11 | 22 | 1 | compound: 8；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_type: 1 |
| S083 | `v23-21024` | Louvre | 11 | 22 | 1 | compound: 8；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_size: 1 |
| S084 | `v23-21029` | Buckingham Palace | 11 | 22 | 1 | compound: 8；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_size: 1 |
| S085 | `v23-21030` | United States Capitol Building | 11 | 22 | 1 | compound: 8；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_size: 1 |
| S086 | `v23-21037` | LEGO House | 11 | 22 | 1 | compound: 8；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_size: 1 |
| S087 | `v23-21045` | Trafalgar Square | 11 | 22 | 1 | compound: 8；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_type: 1 |
| S088 | `v23-21302` | The Big Bang Theory | 11 | 17 | 1 | compound: 3；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_size: 1 |
| S089 | `v23-21303` | WALL•E [Original Version] | 11 | 21 | 1 | compound: 8；control: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_size: 1 |
| S090 | `v23-21318` | Tree House | 11 | 22 | 1 | compound: 8；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_size: 1 |
| S091 | `v23-21319` | Central Perk | 11 | 23 | 1 | compound: 8；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_size: 1；wrong_type: 1 |
| S092 | `v23-21321` | International Space Station | 11 | 17 | 1 | compound: 8；control: 1；missing: 4；offset: 1；wrong_color: 3 |
| S093 | `v23-21325` | Medieval Blacksmith | 11 | 21 | 1 | compound: 8；control: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_type: 1 |
| S094 | `v23-30022` | Bee | 7 | 1 | 1 | control: 1 |
| S095 | `v23-30023` | Lighthouse | 7 | 20 | 1 | compound: 8；control: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3 |
| S096 | `v23-30025` | Clown Fish | 11 | 11 | 1 | control: 1；height_layer: 1；missing: 3；offset: 2；rotation: 1；wrong_color: 2；wrong_type: 1 |
| S097 | `v23-30025--alt1` | Clown Fish · 原模型另一处相连结构 | 11 | 20 | 1 | compound: 8；control: 1；missing: 6；rotation: 1；wrong_color: 4 |
| S098 | `v23-30026` | Panda | 11 | 21 | 1 | compound: 8；control: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_type: 1 |
| S099 | `v23-30026--alt1` | Panda · 原模型另一处相连结构 | 11 | 20 | 1 | compound: 8；control: 1；missing: 5；offset: 1；wrong_color: 4；wrong_type: 1 |
| S100 | `v23-30027` | Reindeer | 11 | 8 | 1 | control: 1；height_layer: 1；missing: 3；offset: 1；wrong_color: 1；wrong_size: 1 |
| S101 | `v23-30027--alt1` | Reindeer · 原模型另一处相连结构 | 11 | 6 | 1 | control: 1；missing: 2；rotation: 1；wrong_color: 2 |
| S102 | `v23-30029` | Pudsey Bear | 11 | 22 | 1 | compound: 8；control: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_size: 1；wrong_type: 1 |
| S103 | `v23-30029--alt1` | Pudsey Bear · 原模型另一处相连结构 | 11 | 22 | 1 | compound: 8；control: 1；extra: 1；missing: 6；offset: 1；wrong_color: 4；wrong_type: 1 |
| S104 | `v23-30181` | Helicopter | 11 | 22 | 1 | compound: 8；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_size: 1 |
| S105 | `v23-30181--alt1` | Helicopter · 原模型另一处相连结构 | 11 | 7 | 1 | control: 1；missing: 6 |
| S106 | `v23-30285` | Tiger | 11 | 3 | 1 | control: 1；missing: 2 |
| S107 | `v23-30311` | Swamp Police Helicopter | 11 | 22 | 1 | compound: 8；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_type: 1 |
| S108 | `v23-30311--alt1` | Swamp Police Helicopter · 原模型另一处相连结构 | 11 | 24 | 1 | compound: 8；control: 1；missing: 7；offset: 1；swapped_positions: 2；wrong_color: 4；wrong_size: 1 |
| S109 | `v23-30312` | Demolition Driller | 11 | 21 | 1 | compound: 8；control: 1；height_layer: 1；missing: 4；offset: 1；rotation: 2；wrong_color: 3；wrong_type: 1 |
| S110 | `v23-30472` | Parrot | 11 | 15 | 1 | compound: 3；control: 1；missing: 3；offset: 2；rotation: 2；wrong_color: 3；wrong_type: 1 |
| S111 | `v23-30472--alt1` | Parrot · 原模型另一处相连结构 | 11 | 24 | 1 | compound: 8；control: 1；missing: 8；offset: 1；swapped_positions: 1；wrong_color: 4；wrong_type: 1 |
| S112 | `v23-30542` | Cute Pug | 11 | 12 | 1 | compound: 3；control: 1；missing: 2；offset: 2；rotation: 1；wrong_color: 3 |
| S113 | `v23-30542--alt1` | Cute Pug · 原模型另一处相连结构 | 11 | 20 | 1 | compound: 8；control: 1；missing: 6；wrong_color: 4；wrong_type: 1 |
| S114 | `v23-30571` | Pelican | 11 | 22 | 1 | compound: 8；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_type: 1 |
| S115 | `v23-30571--alt1` | Pelican · 原模型另一处相连结构 | 11 | 25 | 1 | compound: 8；control: 1；extra: 1；missing: 9；offset: 1；rotation: 1；wrong_color: 4 |
| S116 | `v23-30571--deep` | Pelican · 深层相连结构 | 16 | 16 | 1 | compound: 8；control: 1；missing: 4；wrong_color: 3 |
| S117 | `v23-31025` | Mountain Hut | 11 | 17 | 1 | compound: 3；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_size: 1 |
| S118 | `v23-31037` | Adventure Vehicles | 11 | 18 | 1 | compound: 3；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_type: 2 |
| S119 | `v23-31038` | Changing Seasons | 11 | 17 | 1 | compound: 3；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_type: 1 |
| S120 | `v23-31039` | Blue Power Jet | 11 | 23 | 1 | compound: 8；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_type: 2 |
| S121 | `v23-31040` | Desert Racers | 11 | 5 | 1 | control: 1；height_layer: 1；missing: 2；wrong_color: 1 |
| S122 | `v23-31040--alt1` | Desert Racers · 原模型另一处相连结构 | 11 | 26 | 1 | compound: 8；control: 1；missing: 9；offset: 1；swapped_positions: 2；wrong_color: 4；wrong_type: 1 |
| S123 | `v23-31045` | Ocean Explorer | 11 | 17 | 1 | compound: 3；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_size: 1 |
| S124 | `v23-31048` | Lakeside Lodge | 11 | 22 | 1 | compound: 8；control: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_size: 1；wrong_type: 1 |
| S125 | `v23-31049` | Twin Spin Helicopter | 11 | 7 | 1 | control: 1；missing: 3；offset: 1；rotation: 1；wrong_type: 1 |
| S126 | `v23-31063` | Beachside Vacation | 11 | 23 | 1 | compound: 8；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_type: 2 |
| S127 | `v23-31066` | Space Shuttle Explorer | 11 | 23 | 1 | compound: 8；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_type: 2 |
| S128 | `v23-31070` | Turbo Track Racer | 11 | 8 | 1 | control: 1；height_layer: 1；missing: 3；rotation: 1；wrong_color: 1；wrong_type: 1 |
| S129 | `v23-31072` | Extreme Engines | 11 | 22 | 1 | compound: 8；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_type: 1 |
| S130 | `v23-31072--alt1` | Extreme Engines · 原模型另一处相连结构 | 11 | 22 | 1 | compound: 8；control: 1；missing: 7；offset: 1；wrong_color: 4；wrong_type: 1 |
| S131 | `v23-31084` | Pirate Roller Coaster | 11 | 22 | 1 | compound: 8；control: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_size: 1；wrong_type: 1 |
| S132 | `v23-31092` | Helicopter Adventure | 11 | 11 | 1 | control: 1；height_layer: 1；missing: 3；offset: 2；rotation: 2；wrong_color: 2 |
| S133 | `v23-31092--alt1` | Helicopter Adventure · 原模型另一处相连结构 | 11 | 22 | 1 | compound: 8；control: 1；missing: 7；offset: 1；wrong_color: 4；wrong_type: 1 |
| S134 | `v23-3178` | Seaplane | 11 | 18 | 1 | compound: 5；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 1；wrong_color: 3；wrong_size: 1 |
| S135 | `v23-3178--alt1` | Seaplane · 原模型另一处相连结构 | 11 | 22 | 1 | compound: 8；control: 1；extra: 1；missing: 4；offset: 1；rotation: 1；swapped_positions: 1；wrong_color: 4；wrong_type: 1 |
| S136 | `v23-3179` | Repair Truck | 11 | 5 | 1 | control: 1；missing: 3；wrong_color: 1 |
| S137 | `v23-3179--alt1` | Repair Truck · 原模型另一处相连结构 | 11 | 26 | 1 | compound: 8；control: 1；extra: 1；missing: 9；offset: 1；wrong_color: 4；wrong_size: 1；wrong_type: 1 |
| S138 | `v23-3181` | Passenger Plane | 11 | 18 | 1 | compound: 8；control: 1；missing: 4；rotation: 1；wrong_color: 3；wrong_size: 1 |
| S139 | `v23-3221` | LEGO Truck | 11 | 23 | 1 | compound: 8；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_type: 2 |
| S140 | `v23-3223` | Orange Fish | 11 | 22 | 1 | compound: 8；control: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_size: 1；wrong_type: 1 |
| S141 | `v23-3223--alt1` | Orange Fish · 原模型另一处相连结构 | 8 | 18 | 1 | compound: 8；control: 1；extra: 1；missing: 2；rotation: 1；wrong_color: 4；wrong_type: 1 |
| S142 | `v23-3223--deep` | Orange Fish · 深层相连结构 | 16 | 27 | 1 | compound: 10；control: 1；missing: 4；offset: 1；rotation: 2；swapped_positions: 4；wrong_color: 3；wrong_size: 1；wrong_type: 1 |
| S143 | `v23-4018` | Ship | 9 | 21 | 1 | compound: 8；control: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_size: 1 |
| S144 | `v23-6678` | Pneumatic Crane | 11 | 22 | 1 | compound: 8；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_type: 1 |
| S145 | `v23-6678--deep` | Pneumatic Crane · 深层相连结构 | 16 | 23 | 1 | compound: 10；control: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_type: 1 |
| S146 | `v23-6679` | Dark Shark | 11 | 16 | 1 | compound: 3；control: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_type: 1 |
| S147 | `v23-6682` | Cement Mixer | 11 | 22 | 1 | compound: 8；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_type: 1 |
| S148 | `v23-6682--alt1` | Cement Mixer · 原模型另一处相连结构 | 11 | 21 | 1 | compound: 6；control: 1；extra: 1；missing: 7；offset: 1；rotation: 1；swapped_positions: 1；wrong_color: 2；wrong_type: 1 |
| S149 | `v23-6683` | Burger Stand | 11 | 22 | 1 | compound: 8；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_size: 1 |
| S150 | `v23-6683--alt1` | Burger Stand · 原模型另一处相连结构 | 8 | 18 | 1 | compound: 8；control: 1；missing: 1；offset: 1；swapped_positions: 2；wrong_color: 4；wrong_size: 1 |
| S151 | `v23-6689` | Post-Station | 11 | 23 | 1 | compound: 8；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_size: 2 |
| S152 | `v23-6689--alt1` | Post-Station · 原模型另一处相连结构 | 11 | 25 | 1 | compound: 8；control: 1；extra: 1；missing: 7；offset: 1；rotation: 1；wrong_color: 4；wrong_size: 1；wrong_type: 1 |
| S153 | `v23-6690` | Snorkel Pumper | 11 | 22 | 1 | compound: 8；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_type: 1 |
| S154 | `v23-6690--alt1` | Snorkel Pumper · 原模型另一处相连结构 | 11 | 8 | 1 | control: 1；extra: 1；missing: 5；swapped_positions: 1 |
| S155 | `v23-6698` | RV with Speedboat | 11 | 10 | 1 | control: 1；missing: 3；offset: 2；rotation: 1；wrong_color: 2；wrong_type: 1 |
| S156 | `v23-6698--alt1` | RV with Speedboat · 原模型另一处相连结构 | 11 | 24 | 1 | compound: 8；control: 1；missing: 6；offset: 1；swapped_positions: 2；wrong_color: 4；wrong_size: 1；wrong_type: 1 |
| S157 | `v23-6699` | Cycle Fix-It Shop | 11 | 17 | 1 | compound: 3；control: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_size: 1；wrong_type: 1 |
| S158 | `v23-6699--alt1` | Cycle Fix-It Shop · 原模型另一处相连结构 | 11 | 18 | 1 | compound: 8；control: 1；extra: 1；missing: 3；offset: 1；wrong_color: 3；wrong_size: 1 |
| S159 | `v23-6745` | Propellor Power | 11 | 22 | 1 | compound: 8；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_type: 1 |
| S160 | `v23-6753` | Highway Transport | 11 | 23 | 1 | compound: 8；control: 1；height_layer: 1；missing: 4；offset: 2；rotation: 2；wrong_color: 3；wrong_type: 2 |

## 动态：全部 68 种结构

| 编号 | 模型/配置 | 名称 | 目标件数 | 题数 | 正常题 | 错误与数量 |
|---|---|---|---:|---:|---:|---|
| D001 | `10001` | 10001 | 11 | 13 | 2 | cascade_removal: 2；early_cover: 2；extra_layer: 1；none: 2；removed_piece: 2；rotated_piece: 1；shifted_piece: 1；wrong_color: 2 |
| D002 | `10213` | 10213 | 11 | 15 | 2 | cascade_removal: 2；early_cover: 2；extra_layer: 1；none: 2；removed_piece: 2；rotated_piece: 2；shifted_piece: 2；wrong_color: 2 |
| D003 | `31027-kart` | 31027-kart | 11 | 12 | 2 | cascade_removal: 2；extra_layer: 2；none: 2；removed_piece: 2；shifted_piece: 2；wrong_color: 2 |
| D004 | `31028-sailboat` | 31028-sailboat | 11 | 10 | 2 | cascade_removal: 2；early_cover: 1；extra_layer: 1；none: 2；removed_piece: 2；shifted_piece: 2 |
| D005 | `obj-airplane` | 飞机 | 8 | 44 | 3 | buried_wrong_color: 5；cascade_removal: 3；compound_fault: 4；early_cover: 1；extra_layer: 5；none: 3；removed_piece: 4；rotated_piece: 4；shifted_piece: 6；wrong_color: 4；wrong_part: 3；wrong_size: 2 |
| D006 | `obj-ambulance` | 救护车 | 10 | 30 | 3 | buried_wrong_color: 6；cascade_removal: 3；extra_layer: 3；none: 3；removed_piece: 3；rotated_piece: 1；shifted_piece: 6；wrong_color: 4；wrong_size: 1 |
| D007 | `obj-bed` | 单人床 | 9 | 44 | 3 | buried_wrong_color: 2；cascade_removal: 3；compound_fault: 6；early_cover: 1；extra_layer: 4；none: 3；removed_piece: 6；rotated_piece: 2；shifted_piece: 6；swapped_positions: 1；wrong_color: 6；wrong_part: 2；wrong_size: 2 |
| D008 | `obj-bench` | 长椅 | 11 | 39 | 3 | buried_wrong_color: 4；cascade_removal: 3；compound_fault: 4；early_cover: 2；extra_layer: 4；none: 3；removed_piece: 5；rotated_piece: 2；shifted_piece: 6；wrong_color: 5；wrong_part: 1 |
| D009 | `obj-bookshelf` | 双层书架 | 11 | 52 | 3 | buried_wrong_color: 6；cascade_removal: 3；compound_fault: 4；extra_layer: 4；none: 3；removed_piece: 5；rotated_piece: 6；shifted_piece: 6；wrong_color: 5；wrong_part: 5；wrong_size: 5 |
| D010 | `obj-bridge` | 小桥 | 15 | 33 | 3 | buried_wrong_color: 6；cascade_removal: 3；compound_fault: 2；extra_layer: 4；none: 3；removed_piece: 4；rotated_piece: 2；shifted_piece: 4；wrong_color: 4；wrong_part: 1 |
| D011 | `obj-bunk-bed` | 上下铺 | 11 | 28 | 3 | buried_wrong_color: 6；cascade_removal: 3；compound_fault: 2；extra_layer: 4；none: 3；removed_piece: 4；shifted_piece: 2；wrong_color: 4 |
| D012 | `obj-bus` | 公共汽车 | 8 | 35 | 3 | buried_wrong_color: 6；cascade_removal: 3；early_cover: 1；extra_layer: 3；none: 3；removed_piece: 3；rotated_piece: 3；shifted_piece: 6；wrong_color: 4；wrong_part: 1；wrong_size: 2 |
| D013 | `obj-cabinet` | 矮柜 | 8 | 52 | 3 | buried_wrong_color: 6；cascade_removal: 3；compound_fault: 4；early_cover: 1；extra_layer: 4；none: 3；removed_piece: 5；rotated_piece: 6；shifted_piece: 6；swapped_positions: 1；wrong_color: 5；wrong_part: 5；wrong_size: 3 |
| D014 | `obj-cargo-truck` | 货车 | 10 | 47 | 3 | buried_wrong_color: 6；cascade_removal: 3；compound_fault: 4；early_cover: 1；extra_layer: 5；none: 3；removed_piece: 4；rotated_piece: 4；shifted_piece: 6；wrong_color: 5；wrong_part: 3；wrong_size: 3 |
| D015 | `obj-cash-register` | 收银机 | 6 | 26 | 2 | buried_wrong_color: 4；cascade_removal: 2；compound_fault: 2；extra_layer: 2；none: 2；removed_piece: 3；rotated_piece: 2；shifted_piece: 4；wrong_color: 3；wrong_part: 1；wrong_size: 1 |
| D016 | `obj-chair` | 餐椅 | 7 | 24 | 2 | buried_wrong_color: 2；cascade_removal: 2；compound_fault: 2；early_cover: 1；extra_layer: 2；none: 2；removed_piece: 3；rotated_piece: 2；shifted_piece: 4；wrong_color: 3；wrong_part: 1 |
| D017 | `obj-city-car` | 小汽车 | 6 | 24 | 2 | buried_wrong_color: 4；cascade_removal: 2；compound_fault: 2；extra_layer: 3；none: 2；removed_piece: 2；rotated_piece: 1；shifted_piece: 4；wrong_color: 2；wrong_part: 2 |
| D018 | `obj-clock-tower` | 钟楼 | 13 | 51 | 3 | buried_wrong_color: 6；cascade_removal: 3；compound_fault: 4；extra_layer: 3；none: 3；removed_piece: 5；rotated_piece: 6；shifted_piece: 6；wrong_color: 5；wrong_part: 5；wrong_size: 5 |
| D019 | `obj-coffee-machine` | 咖啡机 | 9 | 34 | 3 | buried_wrong_color: 6；cascade_removal: 3；compound_fault: 4；early_cover: 1；extra_layer: 3；none: 3；removed_piece: 5；shifted_piece: 4；wrong_color: 5 |
| D020 | `obj-crane` | 小吊机 | 9 | 28 | 3 | buried_wrong_color: 6；cascade_removal: 3；compound_fault: 2；extra_layer: 3；none: 3；removed_piece: 4；shifted_piece: 2；wrong_color: 5 |
| D021 | `obj-desk` | 书桌 | 13 | 46 | 3 | buried_wrong_color: 5；cascade_removal: 3；compound_fault: 4；early_cover: 1；extra_layer: 4；none: 3；removed_piece: 5；rotated_piece: 4；shifted_piece: 6；wrong_color: 5；wrong_part: 3；wrong_size: 3 |
| D022 | `obj-fire-engine` | 消防车 | 10 | 41 | 3 | buried_wrong_color: 6；cascade_removal: 3；compound_fault: 4；early_cover: 1；extra_layer: 5；none: 3；removed_piece: 4；rotated_piece: 2；shifted_piece: 6；wrong_color: 5；wrong_part: 1；wrong_size: 1 |
| D023 | `obj-forklift` | 叉车 | 15 | 44 | 3 | buried_wrong_color: 4；cascade_removal: 3；compound_fault: 4；extra_layer: 4；none: 3；removed_piece: 5；rotated_piece: 2；shifted_piece: 6；swapped_positions: 2；wrong_color: 6；wrong_part: 3；wrong_size: 2 |
| D024 | `obj-fountain` | 喷泉 | 8 | 37 | 3 | buried_wrong_color: 5；cascade_removal: 3；compound_fault: 4；extra_layer: 4；none: 3；removed_piece: 4；rotated_piece: 2；shifted_piece: 4；wrong_color: 4；wrong_part: 2；wrong_size: 2 |
| D025 | `obj-gateway` | 门楼 | 15 | 41 | 3 | buried_wrong_color: 6；cascade_removal: 3；compound_fault: 2；extra_layer: 3；none: 3；removed_piece: 4；rotated_piece: 4；shifted_piece: 6；wrong_color: 4；wrong_part: 3；wrong_size: 3 |
| D026 | `obj-helicopter` | 直升机 | 6 | 20 | 2 | buried_wrong_color: 4；cascade_removal: 2；extra_layer: 2；none: 2；removed_piece: 2；rotated_piece: 1；shifted_piece: 4；wrong_color: 2；wrong_part: 1 |
| D027 | `obj-house` | 小房子 | 11 | 46 | 3 | buried_wrong_color: 6；cascade_removal: 3；compound_fault: 4；extra_layer: 4；none: 3；removed_piece: 5；rotated_piece: 4；shifted_piece: 6；swapped_positions: 1；wrong_color: 5；wrong_part: 4；wrong_size: 1 |
| D028 | `obj-lamp` | 台灯 | 7 | 17 | 2 | buried_wrong_color: 4；cascade_removal: 2；extra_layer: 2；none: 2；removed_piece: 2；shifted_piece: 2；wrong_color: 3 |
| D029 | `obj-locomotive` | 火车头 | 11 | 43 | 3 | buried_wrong_color: 6；cascade_removal: 3；compound_fault: 4；extra_layer: 5；none: 3；removed_piece: 4；rotated_piece: 2；shifted_piece: 6；wrong_color: 5；wrong_part: 3；wrong_size: 2 |
| D030 | `obj-monitor` | 电脑显示器 | 7 | 23 | 2 | buried_wrong_color: 4；cascade_removal: 2；extra_layer: 2；none: 2；removed_piece: 2；rotated_piece: 3；shifted_piece: 4；wrong_color: 2；wrong_part: 2 |
| D031 | `obj-motorboat` | 小艇 | 10 | 34 | 3 | buried_wrong_color: 5；cascade_removal: 3；compound_fault: 2；extra_layer: 3；none: 3；removed_piece: 4；rotated_piece: 2；shifted_piece: 4；wrong_color: 4；wrong_part: 2；wrong_size: 2 |
| D032 | `obj-piano` | 立式钢琴 | 10 | 46 | 3 | buried_wrong_color: 6；cascade_removal: 3；compound_fault: 4；extra_layer: 3；none: 3；removed_piece: 5；rotated_piece: 5；shifted_piece: 6；swapped_positions: 1；wrong_color: 5；wrong_part: 4；wrong_size: 1 |
| D033 | `obj-pickup` | 皮卡车 | 9 | 44 | 3 | buried_wrong_color: 4；cascade_removal: 3；compound_fault: 2；extra_layer: 4；none: 3；removed_piece: 4；rotated_piece: 4；shifted_piece: 6；swapped_positions: 2；wrong_color: 5；wrong_part: 4；wrong_size: 3 |
| D034 | `obj-press` | 压力机 | 10 | 50 | 3 | buried_wrong_color: 5；cascade_removal: 3；compound_fault: 6；extra_layer: 3；none: 3；removed_piece: 6；rotated_piece: 6；shifted_piece: 6；wrong_color: 6；wrong_part: 3；wrong_size: 3 |
| D035 | `obj-rail-wagon` | 敞篷车厢 | 9 | 42 | 3 | buried_wrong_color: 4；cascade_removal: 3；compound_fault: 2；extra_layer: 4；none: 3；removed_piece: 4；rotated_piece: 4；shifted_piece: 6；wrong_color: 5；wrong_part: 4；wrong_size: 3 |
| D036 | `obj-refrigerator` | 冰箱 | 14 | 51 | 3 | buried_wrong_color: 6；cascade_removal: 3；compound_fault: 4；extra_layer: 4；none: 3；removed_piece: 5；rotated_piece: 6；shifted_piece: 6；swapped_positions: 1；wrong_color: 5；wrong_part: 5；wrong_size: 3 |
| D037 | `obj-robot` | 机器人 | 10 | 43 | 3 | buried_wrong_color: 5；cascade_removal: 3；compound_fault: 4；extra_layer: 4；none: 3；removed_piece: 5；rotated_piece: 3；shifted_piece: 6；wrong_color: 5；wrong_part: 3；wrong_size: 2 |
| D038 | `obj-rocket` | 火箭 | 12 | 62 | 3 | buried_wrong_color: 5；cascade_removal: 3；compound_fault: 6；extra_layer: 5；none: 3；removed_piece: 6；rotated_piece: 6；shifted_piece: 6；swapped_positions: 4；wrong_color: 6；wrong_part: 6；wrong_size: 6 |
| D039 | `obj-sofa` | 双人沙发 | 7 | 25 | 2 | buried_wrong_color: 3；cascade_removal: 2；compound_fault: 2；extra_layer: 3；none: 2；removed_piece: 3；rotated_piece: 2；shifted_piece: 4；wrong_color: 3；wrong_part: 1 |
| D040 | `obj-staircase` | 楼梯 | 11 | 45 | 3 | buried_wrong_color: 6；cascade_removal: 3；compound_fault: 2；extra_layer: 3；none: 3；removed_piece: 4；rotated_piece: 6；shifted_piece: 6；wrong_color: 4；wrong_part: 4；wrong_size: 4 |
| D041 | `obj-stool` | 小方凳 | 6 | 21 | 2 | buried_wrong_color: 2；cascade_removal: 2；compound_fault: 2；early_cover: 1；extra_layer: 2；none: 2；removed_piece: 3；shifted_piece: 4；wrong_color: 3 |
| D042 | `obj-streetlight` | 路灯 | 7 | 16 | 2 | buried_wrong_color: 4；cascade_removal: 2；extra_layer: 2；none: 2；removed_piece: 2；shifted_piece: 1；wrong_color: 3 |
| D043 | `obj-table` | 方桌 | 9 | 37 | 3 | buried_wrong_color: 5；cascade_removal: 3；compound_fault: 6；early_cover: 1；extra_layer: 5；none: 3；removed_piece: 6；shifted_piece: 2；wrong_color: 6 |
| D044 | `obj-tractor` | 拖拉机 | 11 | 40 | 3 | buried_wrong_color: 6；cascade_removal: 3；compound_fault: 4；extra_layer: 5；none: 3；removed_piece: 4；rotated_piece: 2；shifted_piece: 5；wrong_color: 5；wrong_part: 2；wrong_size: 1 |
| D045 | `obj-traffic-light` | 红绿灯 | 8 | 28 | 3 | buried_wrong_color: 6；cascade_removal: 3；extra_layer: 3；none: 3；removed_piece: 3；rotated_piece: 2；shifted_piece: 2；wrong_color: 4；wrong_part: 1；wrong_size: 1 |
| D046 | `obj-washing-machine` | 洗衣机 | 10 | 55 | 3 | buried_wrong_color: 6；cascade_removal: 3；compound_fault: 4；extra_layer: 5；none: 3；removed_piece: 5；rotated_piece: 6；shifted_piece: 6；swapped_positions: 3；wrong_color: 5；wrong_part: 5；wrong_size: 4 |
| D047 | `omr-21309` | omr-21309 | 11 | 15 | 2 | cascade_removal: 2；early_cover: 2；extra_layer: 1；none: 2；removed_piece: 2；rotated_piece: 2；shifted_piece: 2；wrong_color: 2 |
| D048 | `sr4-alternative-release` | sr4-alternative-release | 9 | 11 | 2 | cascade_removal: 2；early_cover: 1；extra_layer: 2；none: 2；removed_piece: 2；shifted_piece: 2 |
| D049 | `sr4-buried-1` | sr4-buried-1 | 4 | 9 | 1 | cascade_removal: 1；extra_layer: 1；none: 1；removed_piece: 1；rotated_piece: 1；shifted_piece: 1；swapped_positions: 1；wrong_color: 1；wrong_size: 1 |
| D050 | `sr4-buried-3` | sr4-buried-3 | 6 | 9 | 1 | cascade_removal: 1；extra_layer: 1；none: 1；removed_piece: 1；rotated_piece: 1；shifted_piece: 1；swapped_positions: 1；wrong_color: 1；wrong_size: 1 |
| D051 | `sr4-equivalence` | sr4-equivalence | 4 | 6 | 1 | cascade_removal: 1；extra_layer: 1；none: 1；removed_piece: 1；shifted_piece: 1；wrong_size: 1 |
| D052 | `sr4-independent-1` | sr4-independent-1 | 5 | 6 | 1 | cascade_removal: 1；extra_layer: 1；none: 1；removed_piece: 1；shifted_piece: 1；wrong_size: 1 |
| D053 | `sr4-shared-1` | sr4-shared-1 | 4 | 8 | 1 | cascade_removal: 1；extra_layer: 1；none: 1；removed_piece: 1；shifted_piece: 1；swapped_positions: 1；wrong_color: 1；wrong_size: 1 |
| D054 | `sr4-shared-2` | sr4-shared-2 | 5 | 8 | 1 | cascade_removal: 1；extra_layer: 1；none: 1；removed_piece: 1；shifted_piece: 1；swapped_positions: 1；wrong_color: 1；wrong_size: 1 |
| D055 | `sr4-shared-3` | sr4-shared-3 | 6 | 8 | 1 | cascade_removal: 1；extra_layer: 1；none: 1；removed_piece: 1；shifted_piece: 1；swapped_positions: 1；wrong_color: 1；wrong_size: 1 |
| D056 | `sr4-suspended` | sr4-suspended | 8 | 11 | 2 | cascade_removal: 2；early_cover: 1；extra_layer: 2；none: 2；removed_piece: 2；shifted_piece: 2 |
| D057 | `sr4-triple-2` | sr4-triple-2 | 6 | 9 | 1 | cascade_removal: 1；early_cover: 1；extra_layer: 1；none: 1；removed_piece: 1；shifted_piece: 1；swapped_positions: 1；wrong_color: 1；wrong_size: 1 |
| D058 | `sr4-triple-6` | sr4-triple-6 | 10 | 13 | 2 | cascade_removal: 2；early_cover: 1；extra_layer: 1；none: 2；removed_piece: 2；shifted_piece: 2；swapped_positions: 1；wrong_color: 1；wrong_size: 1 |
| D059 | `v23-10158` | v23-10158 | 11 | 14 | 2 | cascade_removal: 2；early_cover: 2；extra_layer: 1；none: 2；removed_piece: 2；rotated_piece: 1；shifted_piece: 2；wrong_color: 2 |
| D060 | `v23-10233` | v23-10233 | 11 | 11 | 2 | cascade_removal: 2；extra_layer: 1；none: 2；removed_piece: 2；shifted_piece: 2；wrong_color: 2 |
| D061 | `v23-1854` | v23-1854 | 11 | 12 | 2 | cascade_removal: 2；extra_layer: 2；none: 2；removed_piece: 2；shifted_piece: 2；wrong_color: 2 |
| D062 | `v23-21006` | v23-21006 | 11 | 15 | 2 | cascade_removal: 2；early_cover: 2；extra_layer: 1；none: 2；removed_piece: 2；rotated_piece: 2；shifted_piece: 2；wrong_color: 2 |
| D063 | `v23-21303` | v23-21303 | 11 | 11 | 2 | cascade_removal: 2；extra_layer: 1；none: 2；removed_piece: 2；shifted_piece: 2；wrong_color: 2 |
| D064 | `v23-30023` | v23-30023 | 7 | 6 | 1 | cascade_removal: 1；extra_layer: 1；none: 1；removed_piece: 1；shifted_piece: 1；wrong_color: 1 |
| D065 | `v23-31039` | v23-31039 | 11 | 15 | 2 | cascade_removal: 2；early_cover: 1；extra_layer: 1；none: 2；removed_piece: 2；rotated_piece: 2；shifted_piece: 2；wrong_color: 2；wrong_part: 1 |
| D066 | `v23-3223` | v23-3223 | 11 | 12 | 2 | cascade_removal: 2；early_cover: 1；extra_layer: 1；none: 2；removed_piece: 2；shifted_piece: 2；wrong_color: 2 |
| D067 | `v23-4018` | v23-4018 | 9 | 12 | 2 | cascade_removal: 2；early_cover: 1；extra_layer: 1；none: 2；removed_piece: 2；shifted_piece: 2；wrong_color: 2 |
| D068 | `v23-6753` | v23-6753 | 11 | 13 | 2 | cascade_removal: 2；extra_layer: 1；none: 2；removed_piece: 2；rotated_piece: 1；shifted_piece: 2；wrong_color: 2；wrong_part: 1 |

## 社区：全部 12 个模块

| 编号 | 模型/配置 | 名称 | 目标件数 | 题数 | 正常题 | 错误与数量 |
|---|---|---|---:|---:|---:|---|
| M001 | `cottage-roof` | 小屋：补完屋顶 | 6 | 8 | 2 | control: 2；extra-layer: 2；missing: 2；wrong-color: 2 |
| M002 | `racer-top` | 赛车：补完车身上半部 | 11 | 8 | 2 | control: 2；extra-layer: 2；missing: 2；wrong-color: 2 |
| M003 | `seaplane-tail` | 水上飞机：补完尾翼 | 7 | 8 | 2 | control: 2；extra-layer: 2；missing: 2；wrong-color: 2 |
| M004 | `museum-roof` | 博物馆：补完长楼屋面 | 12 | 8 | 2 | control: 2；extra-layer: 2；missing: 2；wrong-color: 2 |
| M005 | `repair-truck-cab` | 维修卡车：补车顶灯架 | 5 | 8 | 2 | control: 2；extra-layer: 2；missing: 2；wrong-color: 2 |
| M006 | `orange-helicopter-tail` | 橙色直升机：补尾部 | 7 | 8 | 2 | control: 2；extra-layer: 2；missing: 2；wrong-color: 2 |
| M007 | `police-helicopter-top` | 警用直升机：补机顶与尾鳍 | 10 | 8 | 2 | control: 2；extra-layer: 2；missing: 2；wrong-color: 2 |
| M008 | `panda-head` | 熊猫：补脸部与耳朵 | 6 | 8 | 2 | control: 2；extra-layer: 2；missing: 2；wrong-color: 2 |
| M009 | `burger-stand-roof` | 汉堡店：补屋顶与招牌 | 7 | 8 | 2 | control: 2；extra-layer: 2；missing: 2；wrong-color: 2 |
| M010 | `white-house-roof` | 白宫：补烟囱与屋脊 | 10 | 8 | 2 | control: 2；extra-layer: 2；missing: 2；wrong-color: 2 |
| M011 | `rockefeller-crown` | 洛克菲勒中心：补主塔顶部 | 8 | 8 | 2 | control: 2；extra-layer: 2；missing: 2；wrong-color: 2 |
| M012 | `brandenburg-top` | 勃兰登堡门：补顶部装饰 | 10 | 8 | 2 | control: 2；extra-layer: 2；missing: 2；wrong-color: 2 |
