import random
import time

import bpy

####################
# ヘルパー関数


def purge_orphans():
    """
    すべの孤立したデータブロックの削除
    参照:https://youtu.be/3rNqVPtbhzc?t=149
    """

    if bpy.app.version >= (3, 0, 0):
        # Blender バージョン3.0以降でのみ実行
        bpy.ops.outliner.orphans_purge(
            do_local_ids=True, do_linked_ids=True, do_recursive=True
        )
    else:
        # Blender バージョン3.0未満でのみ実行
        # 削除する孤立したデータブロックがなくなるまで、
        # purge_orphans()を再帰的に呼び出す
        result = bpy.ops.outliner.orphans_purge()
        if result.pop() != "CANCELLED":
            purge_orphans()


def clean_scene():
    """
    すべてのオブジェクト、コレクション、マテリアル、パーティクル、
    テクスチャ、イメージ、カーブ、メッシュ、アクション、ノード、
    ワールドをシーンから削除する
    参照:https://youtu.be/3rNqVPtbhzc
    """

    # アクティブなオブジェクトが編集モードになっていないことを確認する
    if bpy.context.active_object and bpy.context.active_object.mode == "EDIT":
        bpy.ops.object.editmode_toggle()

    # オブジェクトがビューポート非表示、選択無効化されていないかの確認
    for obj in bpy.data.objects:
        obj.hide_set(False)
        obj.hide_select = False
        obj.hide_viewport = False

    # すべてのオブジェクトを選択して削除
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()

    # すべてのコレクションを見つけて削除
    collection_names = [col.name for col in bpy.data.collections]
    for name in collection_names:
        bpy.data.collections.remove(bpy.data.collections[name])

    # ワールドシェーダーを変更する場合
    # ワールドオブジェクトを削除して再作成する
    world_names = [world.name for world in bpy.data.worlds]
    for name in world_names:
        bpy.data.worlds.remove(bpy.data.worlds[name])
    # 新しいワールドデータブロックを作成
    bpy.ops.world.new()
    bpy.context.scene.world = bpy.data.worlds["World"]

    purge_orphans()


def active_object():
    """
    現在アクティブなオブジェクトを返す
    """

    return bpy.context.active_object


def time_seed():
    """
    時間に基づいてランダムシードを設定
    シードをクリップボードにコピー
    """

    seed = time.time()
    print(f"seed:{seed}")
    random.seed(seed)

    # シード値をクリップボードに追加
    bpy.context.window_manager.clipboard = str(seed)

    return seed


# アニメーションを線形補間に設定する関数
def set_fcurve_extrapolation_to_linear():
    for fc in bpy.context.active_object.animation_data.action.fcurves:
        fc.extrapolation = "LINEAR"


# ループアニメーションを作成する関数
def create_data_animation_loop(
    obj,
    data_path,
    start_value,
    mid_value,
    start_frame,
    loop_length,
    linear_extrapolation=True,
):
    """
    データ プロパティ ループを作成するには、次の操作が必要
    1. プロパティを初期値に設定し、ループの先頭にキーフレームを追加
    2. プロパティを中間値に設定し、ループの途中にキーフレームを追加
    3. プロパティを初期値に設定し、ループの最後にキーフレームを追加
    """

    # 開始値を設定する
    setattr(obj, data_path, start_value)
    # 開始時にキーフレームを追加
    obj.keyframe_insert(data_path, frame=start_frame)

    # 中間の値を設定する
    setattr(obj, data_path, mid_value)
    # 中間地点にキーフレームを追加
    mid_frame = start_frame + (loop_length) / 2
    obj.keyframe_insert(data_path, frame=mid_frame)

    # 終了値を設定する
    setattr(obj, data_path, start_value)
    # 最終キーフレームを追加
    end_frame = start_frame + loop_length
    obj.keyframe_insert(data_path, frame=end_frame)

    if linear_extrapolation:
        set_fcurve_extrapolation_to_linear()


def set_scene_props(fps, frame_count):
    """
    シーンのプロパティを設定する
    """

    scene = bpy.context.scene
    scene.frame_end = frame_count

    # ワールドの背景を黒に設定する
    world = bpy.data.worlds["World"]
    if "Background" in world.node_tree.nodes:
        world.node_tree.nodes["Background"].inputs[0].default_value = (0, 0, 0, 1)

    scene.render.fps = fps

    scene.frame_current = 1
    scene.frame_start = 1


# シーンを設定する関数
def scene_setup():
    fps = 30
    loop_seconds = 12
    frame_count = fps * loop_seconds

    seed = 0
    if seed:
        random.seed(seed)
    else:
        time_seed()

    clean_scene()

    set_scene_props(fps, frame_count)


####################


# ジオメトリノードを接続する関数
def link_nodes_by_mesh_socket(node_tree, from_node, to_node):
    node_tree.links.new(from_node.outputs["Mesh"], to_node.inputs["Mesh"])


def create_node(
    node_tree, type_name, node_x_location, node_location_step_x=0, node_y_location=0
):
    """
    指定されたタイプのノードを作成し、X 軸上のノードの位置を設定、更新
    ノード オブジェクトと、次のノードの X 軸上の次の位置を返す
    """
    node_obj = node_tree.nodes.new(type=type_name)
    node_obj.location.x = node_x_location
    node_obj.location.y = node_y_location
    node_x_location += node_location_step_x

    return node_obj, node_x_location


# ランダム値ノード作成関数
def create_random_bool_value_node(node_tree, node_x_location, node_y_location):

    # ランダム値ノード作成
    separate_geo_random_value_node, node_x_location = create_node(
        node_tree,
        "FunctionNodeRandomValue",
        node_x_location,
        node_y_location=node_y_location,
    )
    target_output_type = "BOOLEAN"
    separate_geo_random_value_node.data_type = target_output_type

    # ランダム値ノードのアウトプットソケットのタイプを確認する（簡潔コード）
    random_value_node_output_lookup = {
        socket.type: socket
        for socket in separate_geo_random_value_node.outputs.values()
    }

    # 複数行で確認するコード
    # sockets = dict()
    # for socket in separate_geo_random_value_node.outputs.values():
    #     sockets[socket.type] = socket

    import pprint

    pprint.pprint(random_value_node_output_lookup)

    # ランダム値ノードのアウトプットソケットを指定
    target_output_socket = random_value_node_output_lookup[target_output_type]

    return target_output_socket


# ジオメトリ分離ノード作成関数
def create_separate_geo_node(node_tree, node_x_location, node_location_step_x):

    # ランダム値ノードの作成
    random_value_node_output_socket = create_random_bool_value_node(
        node_tree, node_x_location, node_y_location=-200
    )

    # ジオメトリ分離ノードの作成
    separate_geometry_node, node_x_location = create_node(
        node_tree,
        "GeometryNodeSeparateGeometry",
        node_x_location,
        node_location_step_x,
    )
    separate_geometry_node.domain = "FACE"

    # ランダム値ノードをジオメトリ分離ノードに接続
    to_node = separate_geometry_node
    node_tree.links.new(random_value_node_output_socket, to_node.inputs["Selection"])

    return separate_geometry_node, node_x_location


# 要素スケールノード作成関数
def create_scale_element_geo_node(
    node_tree, geo_selection_node_output, node_x_location, node_y_location
):
    # ランダム値ノード呼び出し
    random_value_node_output_socket = create_random_bool_value_node(
        node_tree,
        node_x_location,
        node_y_location=node_y_location - 200,
    )

    # 要素スケールノードの作成
    scale_elements_node, node_x_location = create_node(
        node_tree,
        "GeometryNodeScaleElements",
        node_x_location,
        node_y_location=node_y_location,
    )
    scale_elements_node.inputs["Scale"].default_value = 0.8

    start_frame = random.randint(0, 150)

    # アニメーション作成
    create_data_animation_loop(
        scale_elements_node.inputs["Scale"],
        "default_value",
        start_value=0.0,
        mid_value=0.8,
        start_frame=start_frame,
        loop_length=90,
        linear_extrapolation=False,
    )

    # ランダム値ノードを要素スケールノードの選択へ接続
    to_node = scale_elements_node
    node_tree.links.new(random_value_node_output_socket, to_node.inputs["Selection"])

    # ランダム値ノードを要素スケールノードのジオメトリへ接続
    to_node = scale_elements_node
    node_tree.links.new(geo_selection_node_output, to_node.inputs["Geometry"])

    return scale_elements_node


# 面を分離し、大きさのアニメーション化を行なう関数
def separate_faces_and_animate_scale(node_tree, node_x_location, node_location_step_x):

    # ジオメトリ分離ノードの作成
    separate_geometry_node, node_x_location = create_separate_geo_node(
        node_tree,
        node_x_location,
        node_location_step_x,
    )

    # ジオメトリ分離ノードから要素スケールノードへ選択経由と反転経由で接続
    scale_elements_geo_nodes = []
    top_scale_elements_node = create_scale_element_geo_node(
        node_tree,
        separate_geometry_node.outputs["Selection"],
        node_x_location,
        node_y_location=200,
    )
    scale_elements_geo_nodes.append(top_scale_elements_node)

    bottom_scale_elements_node = create_scale_element_geo_node(
        node_tree,
        separate_geometry_node.outputs["Inverted"],
        node_x_location,
        node_y_location=-200,
    )
    scale_elements_geo_nodes.append(bottom_scale_elements_node)

    # Fカーブにサイクルモディファイアを追加
    for fcurve in node_tree.animation_data.action.fcurves.values():
        fcurve.modifiers.new(type="CYCLES")

    node_x_location += node_location_step_x

    # ジオメトリ結合ノードの作成
    join_geometry_node, node_x_location = create_node(
        node_tree, "GeometryNodeJoinGeometry", node_x_location, node_location_step_x
    )

    # 2つの要素スケールノードをジオメトリ結合ノードへ接続
    for node in scale_elements_geo_nodes:
        from_node = node
        to_node = join_geometry_node
        node_tree.links.new(from_node.outputs["Geometry"], to_node.inputs["Geometry"])

    return separate_geometry_node, join_geometry_node, node_x_location


def update_geo_node_tree(node_tree):
    """
    立方体メッシュ、細分化、三角化、辺分離、要素スケール
    ジオメトリノードをノードツリーに追加
    ノード参照:https://docs.blender.org/api/current/bpy.types.GeometryNode.html
    """

    out_node = node_tree.nodes["Group Output"]

    node_x_location = 0
    node_location_step_x = 300

    # 立方体メッシュノードの作成
    mesh_cube_node, node_x_location = create_node(
        node_tree,
        "GeometryNodeMeshCube",
        node_x_location,
        node_location_step_x,
    )

    # 細分化ノードの作成
    subdivide_mesh_node, node_x_location = create_node(
        node_tree,
        "GeometryNodeSubdivideMesh",
        node_x_location,
        node_location_step_x,
    )
    subdivide_mesh_node.inputs["Level"].default_value = 3

    # 三角化ノードの作成
    triangulate_node, node_x_location = create_node(
        node_tree,
        "GeometryNodeTriangulate",
        node_x_location,
        node_location_step_x,
    )

    # 辺分離ノードの作成
    split_edges_node, node_x_location = create_node(
        node_tree,
        "GeometryNodeSplitEdges",
        node_x_location,
        node_location_step_x,
    )

    # 要素スケールノード、ジオメトリ結合ノードの配置
    separate_geometry_node, join_geometry_node, node_x_location = (
        separate_faces_and_animate_scale(
            node_tree, node_x_location, node_location_step_x
        )
    )

    # 各ノードからグループ出力までのリンク接続
    out_node.location.x = node_x_location

    link_nodes_by_mesh_socket(
        node_tree, from_node=mesh_cube_node, to_node=subdivide_mesh_node
    )
    link_nodes_by_mesh_socket(
        node_tree, from_node=subdivide_mesh_node, to_node=triangulate_node
    )
    link_nodes_by_mesh_socket(
        node_tree, from_node=triangulate_node, to_node=split_edges_node
    )

    from_node = split_edges_node
    to_node = separate_geometry_node
    node_tree.links.new(from_node.outputs["Mesh"], to_node.inputs["Geometry"])

    from_node = join_geometry_node
    to_node = out_node
    node_tree.links.new(from_node.outputs["Geometry"], to_node.inputs["Geometry"])


# ジオメトリノードを作成する関数
def create_centerpiece():
    bpy.ops.mesh.primitive_plane_add()

    bpy.ops.node.new_geometry_nodes_modifier()

    node_tree = bpy.data.node_groups["Geometry Nodes"]

    update_geo_node_tree(node_tree)

    bpy.ops.object.modifier_add(type="SOLIDIFY")

    # 最後にジオメトリノード モディファイアをアクティブ モードにする
    bpy.context.active_object.modifiers["GeometryNodes"].is_active = True


def main():
    """
    細分化し、三角化された面で構成される立方体の
    アニメーション化されたジオメトリノードを生成する
    Python コード
    """

    scene_setup()
    create_centerpiece()


if __name__ == "__main__":
    main()
