# YFX Exporter

[![GitHub license](https://img.shields.io/github/license/yuufyu/YFX-Exporter)](https://github.com/yuufyu/YFX-Exporter/blob/main/LICENSE)
[![Blender Version](https://img.shields.io/badge/Blender-4.0.2-blue)](https://www.blender.org/)

## 概要
FBXエクスポートのためのプラグインで、モディファイアの適用やオブジェクトのマージなどを非破壊的に行います。

## 機能
ユーザーが「Export FBX」ボタンを押すと、アドオンは現在のシーンをコピーし、バックグラウンドでエクスポート処理を行います。モディファイアの適用やオブジェクトのマージはエクスポートされるFBXファイルにのみ反映され、現在のシーンは変更されません。エクスポート時に実行される処理は以下の通りです。

- **Apply Constraint:** 現在のシーンに表示されているObject Constraintを適用します。

- **Convert to Mesh:** Curve、Surface、TextオブジェクトをMeshに変換します。（注意: Curve、Surface、Textオブジェクトに付与されているモディファイアは削除されます。）

- **Apply Modifier:** 現在のシーンに表示されているMeshオブジェクトに付与されているモディファイアを適用します。シェイプキーが設定されているMeshオブジェクトにもモディファイアが適用可能です。ビューポート表示が設定されていないモディファイアは削除されます。

- **Merge Mesh:** 指定した「Merge Collection」の階層内のすべてのオブジェクトをマージします。マージ後のオブジェクトはコレクションの名前に置換されます。

- **Apply Transform(\*1):** マージしたオブジェクトのTransformを適用します。適用したオブジェクトの原点はワールド座標原点に設定されます。

- **Separate Shapekey(\*1):** 指定したシェイプキーを分割元シェイプキーとして設定できます。分割元のシェイプキーはオブジェクトの原点を通るX軸方向で分割されます。分割後のシェイプキーは分割元のシェイプキーの直下に追加され、指定した名前が付けられます。分割元のシェイプキーを削除することもできます。

- **Sort Shapekey(\*1):** Merge Meshでマージ後のオブジェクトに付与されているシェイプキーの並び順を指定できます。

- **Delete Unused Vertex Group(\*1):** Meshオブジェクトの不要な頂点グループを削除します。Armatureモディファイアの変形ボーンに含まれない名前の頂点グループやウェイトが0の頂点グループが不要と見なされます。

- **Export FBX:** 現在のシーンに表示されているモデルをFBX形式でエクスポートします。

(*1) 各Merge Collectionごとに設定される機能です。

## インストール
1. [Code > Download ZIP](https://github.com/yuufyu/YFX-Exporter/archive/refs/heads/main.zip) ページからプラグインのZIPファイルをダウンロードします。
2. Blenderを開き、Edit > Preferences > Add-onsに移動します。
3. "Install"をクリックし、ダウンロードしたZIPファイルを選択します。
4. "YFX Exporter"アドオンを有効にします。

## 使い方
"View 3D > SidePanel > YFX > YFX Exporter"  
ビューポート3D画面のサイドパネルの「YFX」タブからエクスポート処理の開始と設定ができます。

## 既知の問題
「Merge Collection」内にAuto Smoothが有効なMeshオブジェクトが存在する場合、エクスポート後に法線が変わる可能性があります。

## ライセンス
このプラグインはGNU General Public License（GPL）バージョン3の下でライセンスされています。詳細については[LICENSE](https://github.com/yuufyu/YFX-Exporter/blob/main/LICENSE)ファイルを参照してください。

## 作者
yuufyu

## フィードバックと貢献
フィードバックや貢献は歓迎です！質問や提案があれば、お気軽にissueを開いたりpull requestを送信したりしてください。
