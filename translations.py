import bpy

translation_dict = {
    "en_US": {
        (
            "*",
            "'%s' belongs to multiple collections. The object's appearance may change after export",
        ): "'%s' belongs to multiple collections. The object's appearance may change after export",
        ("*", "Invalid FBX output path"): "Invalid FBX output path",
        (
            "*",
            "'%s' has a shapekey with a modifier changing vertex count based on shape",
        ): "'%s' has a shapekey with a modifier changing vertex count based on shape",
        (
            "*",
            "Armature modifier in '%s' should be set at the bottom",
        ): "Armature modifier in '%s' should be set at the bottom",
        (
            "*",
            "Transform in Armature (%s) is not reset",
        ): "Transform in Armature (%s) is not reset",
        (
            "*",
            "'%s''s GeometryNode may not be exportable",
        ): "'%s''s GeometryNode may not be exportable",
        (
            "*",
            "Armature settings for objects in '%s' are not consistent. Some meshes may not follow bones after export",
        ): "Armature settings for objects in '%s' are not consistent. Some meshes may not follow bones after export",
        (
            "*",
            "Armature '%s' referenced by modifiers will not be exported as it's hidden",
        ): "Armature '%s' referenced by modifiers will not be exported as it's hidden",
        (
            "*",
            "'%s' with Auto Smooth set may have normals changed after export",
        ): "'%s' with Auto Smooth set may have normals changed after export",
        (
            "*",
            "Object '%s' without an Armature modifier is present",
        ): "Object '%s' without an Armature modifier is present",
        (
            "*",
            "Shapekeys of Text, Surface, and Curve will be deleted",
        ): "Shapekeys of Text, Surface, and Curve will be deleted",
        (
            "*",
            "Child collection '%s' settings are ignored as the parent collection is set as the merge target",
        ): "Child collection '%s' settings are ignored as the parent collection is set as the merge target",
        ("*", "Check Model"): "Check Model",
        ("*", "FBX settings"): "FBX settings",
        ("*", "Merge Collections"): "Merge Collections",
        ("*", "Collection Settings"): "Collection Settings",
        ("*", "Shapekey Settings"): "Shapekey Settings",
        ("*", "Update Shapekey List"): "Update Shapekey List",
        (
            "*",
            "Update shapekey list in collection",
        ): "Update shapekey list in collection",
        ("*", "Separate Shapekeys L/R"): "Separate Shapekeys L/R",
        (
            "*",
            "Split Shapekeys Left and Right Centered at the Object's Origin",
        ): "Split Shapekeys Left and Right Centered at the Object's Origin",
        ("*", "Delete Source Shapekey"): "Delete Source Shapekey",
        (
            "*",
            "Deletes the source shapekey used for splitting",
        ): "Deletes the source shapekey used for splitting",
        ("*", "Name of the shapekey on the left"): "Name of the shapekey on the left",
        ("*", "Name of the shapekey on the right"): "Name of the shapekey on the right",
        ("*", "(Warning!)Main Process Export"): "(Warning!)Main Process Export",
        (
            "*",
            "(Warning!)When enabling this option, the export process in the main process will make potentially destructive changes to the current Blender file",
        ): "(Warning!)When enabling this option, the export process in the main process will make potentially destructive changes to the current Blender file",
        (
            "*",
            "Deletes vertex groups not assigned to deform bones",
        ): "Deletes vertex groups not assigned to deform bones",
        ("*", "FBX exported successfully!"): "FBX exported successfully!",
        (
            "*",
            "A validation check on the models in the scene, ensuring their exportability",
        ): "A validation check on the models in the scene, ensuring their exportability",
        (
            "*",
            "[Validation Successful] All models in the scene have passed the exportability check successfully",
        ): "[Validation Successful] All models in the scene have passed the exportability check successfully",
    },
    "ja_JP": {
        (
            "*",
            "'%s' belongs to multiple collections. The object's appearance may change after export",
        ): "'%s'が複数のコレクションに所属しています。出力後、オブジェクトの見た目が変わる場合があります",
        ("*", "Invalid FBX output path"): "不正なFBX出力パスです",
        (
            "*",
            "'%s' has a shapekey with a modifier changing vertex count based on shape",
        ): "シェイプキーが存在する'%s'に形状で頂点数が変わるモディファイアが設定されています",
        (
            "*",
            "Armature modifier in '%s' should be set at the bottom",
        ): "'%s'のArmatureモディファイアは一番下に設定してください",
        (
            "*",
            "Transform in Armature (%s) is not reset",
        ): "Armature(%s)のTransformがリセットされていません",
        (
            "*",
            "'%s''s GeometryNode may not be exportable",
        ): "'%s'のGeometryNodeはエクスポートできない場合があります",
        (
            "*",
            "Armature settings for objects in '%s' are not consistent. Some meshes may not follow bones after export",
        ): "'%s'に含まれるオブジェクトのArmatureの設定が統一されていません。出力後、一部のメッシュがボーンに追従しない場合があります",
        (
            "*",
            "Armature '%s' referenced by modifiers will not be exported as it's hidden",
        ): "モディファイアから参照しているArmature'%s'は非表示のため出力されません",
        (
            "*",
            "'%s' with Auto Smooth set may have normals changed after export",
        ): "自動スムース(Auto Smooth)が設定されている'%s'は、出力後に法線が変わる場合があります",
        (
            "*",
            "Object '%s' without an Armature modifier is present",
        ): "Armatureモディファイアが設定されていないオブジェクト'%s'があります",
        (
            "*",
            "Shapekeys of Text, Surface, and Curve will be deleted",
        ): "Text, Surfece, Curveのシェイプキーは削除されます",
        (
            "*",
            "Child collection '%s' settings are ignored as the parent collection is set as the merge target",
        ): "親コレクションをマージ対象に設定しているため、子コレクションである'%s'の設定は無視されます",
        ("*", "Check Model"): "モデルのチェック",
        ("*", "FBX settings"): "FBX設定",
        ("*", "Merge Collections"): "マージコレクション",
        ("*", "Collection Settings"): "コレクション設定",
        ("*", "Shapekey Settings"): "シェイプキー設定",
        ("*", "Update Shapekey List"): "シェイプキー一覧を更新",
        ("*", "Update shapekey list in collection"): "コレクションに含まれるシェイプキー一覧を更新します",
        ("*", "Separate Shapekeys L/R"): "シェイプキーを左右に分割",
        (
            "*",
            "Split Shapekeys Left and Right Centered at the Object's Origin",
        ): "オブジェクトの原点を中心としてシェイプキーを左右に分割します",
        ("*", "Delete Source Shapekey"): "分割元のシェイプキーを削除",
        ("*", "Deletes the source shapekey used for splitting"): "分割元のシェイプキーを削除します",
        ("*", "Name of the shapekey on the left"): "左側に分割したシェイプキーの名前です",
        ("*", "Name of the shapekey on the right"): "右側に分割したシェイプキーの名前です",
        ("*", "(Warning!)Main Process Export"): "(警告)メインプロセスでエクスポート",
        (
            "*",
            "(Warning!)When enabling this option, the export process in the main process will make potentially destructive changes to the current Blender file",
        ): "(警告)メインプロセスでエクスポート処理を実施します。このオプションを有効にすると、現在のブレンダーファイルが破壊的に変更されます",
        (
            "*",
            "Deletes vertex groups not assigned to deform bones",
        ): "変形ボーンに割り当てられていない頂点グループを削除します",
        ("*", "FBX exported successfully!"): "FBXのエクスポートに成功!",
        (
            "*",
            "A validation check on the models in the scene, ensuring their exportability",
        ): "シーン上のモデルがエクスポート可能であるかを検証します",
        (
            "*",
            "[Validation Successful] All models in the scene have passed the exportability check successfully",
        ): "[検証成功] シーン上のモデルがエクスポート可能であることをチェックしました",
    },
}


def register() -> None:
    bpy.app.translations.register(__name__, translation_dict)


def unregister() -> None:
    bpy.app.translations.unregister(__name__)
